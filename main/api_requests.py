import json
from main.worker_threads import MailerThread
from main.models.company import (
    BusinessCompanyReg,
    Encumbrance,
    EncumbrancePersonsEntitled,
    # EncumbranceSecuredAmounts,
    ShareCapital,
    Shares,
)

from django.conf import settings
from main.models.psmt import BgRequestModule, Module, PSMTRequest, Package
from django.http.request import HttpRequest
from utils.functions import build_url
import requests, time, threading
from decouple import config
from rest_framework.validators import ValidationError
from django.utils.timezone import now


base_url = config("ECITIZEN_API", "http://localhost:8000")
external_packages = settings.EXTERNAL_API_PACKAGES


class HelperFunctions:
    def flatten_shares(self, partners=[]):
        output = []

        for _partner in partners:
            _shares = _partner.pop("shares", [])
            # shares = _shares[0] if _shares else {}

            number_of_shares = ",".join(
                [
                    (
                        "%s:%s"
                        % (share.pop("name", "-"), share.pop("number_of_shares", "-"))
                    )
                    for share in _shares
                ]
            )

            if _partner.get("name", False):
                (
                    _partner["first_name"],
                    _partner["second_name"],
                    _partner["third_name"],
                ) = self.split_full_name(_partner.pop("name", ""))
            else:
                _partner.pop("name", False)

            partner = {**_partner, "number_of_shares": number_of_shares}

            if partner:
                output.append(partner)
            json.dump(output, open("main/res.json", "w"))
        return output

    def split_full_name(self, full_name=""):

        # must return an array of 3 items, first_name, second_name, third_name
        # example CEPHAS K. TOO ---> ['CEPHAS', 'K.', 'TOO']
        names_array: list = full_name.split(" ")

        # pop out first_name from the names array
        first_name = names_array.pop(0) if len(names_array) else ""
        # pop out second_name from the names array
        second_name = names_array.pop(0) if len(names_array) else ""
        # join the rest of the names as third name
        third_name = " ".join(names_array) if len(names_array) else ""

        return [first_name, second_name, third_name]


class RequestHandler(threading.Thread, HelperFunctions):
    def __init__(self, request: HttpRequest, request_ref_number) -> None:
        super().__init__()
        self.request = request
        self.request_ref_number = request_ref_number
        self.data = data = request.data
        self.package_id = data.get("package_id", None)
        self.module_id = data.get("module_id", None)
        self.retries = 0

        self.api_request = {}

    def get(self):
        exception = None
        try:
            self.api_request = api_request = requests.post(
                build_url(base_url, "/api/business/search/"),
                json={"registration_number": self.data.get("registration_number")},
            )

            # if api_request.status_code >= 400 and api_request.status_code != 404:
            if api_request.status_code >= 400:
                self.retries = 4
                raise ValueError(
                    "Got an invalid %s status code from extenal server. Request data was %s, Response Data was%s"
                    % (
                        api_request.status_code,
                        api_request.request.body,
                        api_request.content.decode("utf-8"),
                    )
                )

        except Exception as e:
            self.retries = self.retries + 1
            exception = e
        finally:
            if exception and self.retries <= 3:
                time.sleep(4)
                self.get()
            elif exception:
                self.create_instance()
            else:
                instance: PSMTRequest = self.create_instance(silent=True)
                self.update_db(instance)
        # on successful get, save the data to the database
        return self.api_request

    def run(self) -> None:
        self.post_init()
        if self.package_id in external_packages:
            self.get()
        else:
            self.create_instance()

    def post_init(self):
        try:
            self.module_id = int(self.module_id)
        except:
            self.module_id = self.module_id
        try:
            self.package_id = int(self.package_id)
        except:
            self.package_id = self.package_id

    def create_instance(self, silent=False):
        request = self.request
        company = request.user.company

        company_code = company.company_code

        self.company_code = company_code
        request_ref_number = self.request_ref_number

        package_id = request.data.get("package_id")
        module_id = request.data.get("module_id")
        registration_number = request.data.get("registration_number")
        dataset_name = request.data.get("dataset_name")
        errors = {}

        try:
            module = Module.objects.get(module_id=module_id, status=11)
        except:
            errors["package"] = "Module Does not Exist!"

        try:
            package = Package.objects.get(package_id=package_id, package_status=11)
        except:
            errors["package"] = "Package Does not Exist!"

        # CHECK IF THERE ARE ANY ERRORS,
        # IF THERE ARE ANY, RAISE A VALIDATION ERROR
        if errors:
            raise ValidationError(errors)
        #print(" == ** saving individual data **  package.package_name is " )
        #print(package.package_name )
        data = {
            "request_ref_number": request_ref_number,
            "company_name": company.company_name,
            "client_number":request.data.get("client_number"),
            "client_name": request.user.name,
            "bg_dataset_name": dataset_name,
            "client_name": request.user.name,
            "user_name": request.user.email,
            "client_id": request.user.pk,
            "client_login_id": company_code,
            "file_tracker": request_ref_number,
            "request_credit_charged": package.package_cost,
            "package_cost": package.package_cost,
            "package_id": package.pk,
            "request_package": package.pk,
            "request_plan": request.data.get("req_plan"),  
            "request_type": "company",
            "registration_number": str(registration_number).replace("\t", "").strip(),
            "status": "00",
        }

        instance = PSMTRequest.objects.create(**data)

        BgRequestModule.objects.create(
            request_id=request_ref_number,
            client_id=company.pk,
            request_ref_number=instance,
            parent_module_id=package.pk,
            module_cost_quote=module.module_cost,
            package_name=package.package_name,
            module_id=module.module_id,
            module_name=module.module_name,
            package_id=package.pk,
            request_type="company",
        )

        if not silent:
            mailer = MailerThread()
            mailer.company_name = instance.company_name
            mailer.dataset_name = instance.bg_dataset_name
            mailer.request_id = instance.pk
            mailer.start()

        return instance

    def update_db(self, request_instance):
        request_ref_number = request_instance.request_ref_number
        # get the data
        data = self.api_request.json()

        import json

        json.dump(data, open("responses.json", "w"))

        shares = self.flatten_shares(data.pop("partners", []))
        encumberances = data.pop("encumberances", [])
        share_capital = data.pop("share_capital", [])

        business = BusinessCompanyReg.objects.create(
            request_ref_number=request_instance,
            registration_number=request_instance.registration_number,
            registration_date=data.get("registration_date", ""),
            objective=data.get("objective", ""),
            physical_address=data.get("physical_address", ""),
            postal_address=data.get("postal_address", ""),
            email=data.get("email", ""),
            phone_number=data.get("phone_number", ""),
            branches=data.get("branches", ""),
            business_name=data.get("business_name", ""),
            kra_pin=data.get("kra_pin", ""),
        )

        try:
            for _share in shares:
                Shares.objects.create(
                    **_share,
                    business=business,
                    percentage=_share.get("number_of_shares", None),
                    data_source="BRS",
                    review_status="APPROVED",
                )
        except Exception as e:
            print(e)

        for _enc in encumberances:
            persons_entitled = _enc.pop("persons_entitled", [])
            secured_amounts = _enc.pop("secured_amounts", [])
            #
            _secured_amounts = ", ".join(
                [("%s %s" % (i.currency, i.amount)) for i in secured_amounts]
            )
            _persons_entitled = ", ".join([(i.name) for i in secured_amounts])

            enc = Encumbrance.objects.create(
                **_enc,
                review_status="APPROVED",
                verified_by="SELF",
                search_id=request_ref_number,
                business=business,
                secured_amounts=_secured_amounts,
            )

        for _share_capital in share_capital:
            try:
                share_capital_ = ShareCapital(**_share_capital, business=business)
                share_capital_.save()
            except Exception as e:
                print(e)

        # save the data to the database

        # update the module status and the request status to 11
        BgRequestModule.objects.filter(request_ref_number=request_ref_number).update(
            status="11"
        )
        request_instance.status = "11"
        request_instance.verified_date = now()
        request_instance.save()

        # SEND MAIL
        mailer = MailerThread()
        mailer.instance = request_instance
        mailer.start()
