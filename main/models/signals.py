from main.models.company import BusinessCompanyReg
from main.models.psmt import PSMTRequest, Package 
from main.models.psmt_request_modules import PelPsmtRequestModules
from django.db.models.signals import pre_save
from django.utils.timezone import now


def psmt_request_presave(sender, instance: PSMTRequest, **kwargs):
    if (
        instance.status == "11"
        or instance.status == "11"
        and not instance.verified_date
    ):
        instance.verified_date = now()
        instance.verified_by = "SELF"


def handle_business_presave(sender, instance: BusinessCompanyReg, **kwargs):
    type = instance.type
    mapping = {
        "business": "34",
        "company": "31",
        "cbo": "38",
        "trust": "39",
        "society": "36",
        "sacco": "35",
        "ngo": "33",
        "llp": "37",
        "clg": "40",
        "international": "41",
    }

    try:
        package_id = mapping.get(type, 0)
        package: Package = Package.objects.get(pk=int(package_id))

        request: PSMTRequest = instance.request_ref_number
        request.package = package
        request.request_package = package.pk
        request.request_plan = package.package_name
        request.save()

    except Exception as e:
        print(e)


pre_save.connect(psmt_request_presave, sender=PSMTRequest)
pre_save.connect(handle_business_presave, sender=BusinessCompanyReg)
