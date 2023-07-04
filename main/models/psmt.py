from django.db import models
import uuid


class PSMTRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    client_number = models.CharField(max_length=200, blank=True, null=True)
    company_name = models.CharField(max_length=255, null=True)
    registration_number = models.CharField(max_length=200, blank=True, null=True)
    dataset_citizenship = models.CharField(max_length=255, null=True)
    company_type = models.CharField(max_length=255, null=True)
    request_plan = models.CharField(max_length=255, null=True)
    bg_dataset_name = models.CharField(max_length=255, null=True)
    request_ref_number = models.CharField(
        max_length=255, unique=True, default=uuid.uuid4
    )
    status = models.CharField(max_length=255, null=True, default="33")
    request_payment_ref = models.CharField(max_length=255, null=True)
    client_id = models.CharField(max_length=255, null=True)
    request_date = models.DateTimeField(auto_now_add=True)
    request_terms = models.CharField(max_length=255, null=True)
    package_cost = models.CharField(max_length=255, null=True)
    request_dataset_cat = models.CharField(max_length=255, null=True)
    client_name = models.CharField(max_length=255, null=True)
    dataset_kra_pin = models.CharField(max_length=255, null=True)
    dataset_incorporation_no = models.CharField(max_length=255, null=True)
    bg_dataset_email = models.CharField(max_length=255, null=True)
    bg_dataset_mobile = models.CharField(max_length=255, null=True)
    bg_dataset_idnumber = models.CharField(max_length=20, null=True)
    user_id = models.CharField(max_length=255, null=True)
    user_name = models.CharField(max_length=255, null=True)
    user_lock = models.CharField(max_length=255, null=True)
    notify_by = models.CharField(max_length=255, null=True)
    notify_date = models.DateTimeField(null=True)
    user_lock_date = models.DateTimeField(max_length=255, null=True)
    file_tracker = models.CharField(max_length=255, null=True)
    comments = models.CharField(max_length=255, null=True)
    request_package = models.CharField(max_length=255, null=True)
    dataset_name = models.CharField(max_length=255, null=True)
    report_file = models.CharField(max_length=255, null=True)
    parent_name = models.CharField(max_length=255, null=True)
    request_type = models.CharField(
        max_length=255,
        null=True,
        choices=(("individual", "INDIVIDUAL"), ("company", "COMPANY")),
        blank=False,
    )
    dataset_photo = models.CharField(max_length=255, null=True)
    client_login_id = models.CharField(max_length=255, null=True)
    progress_calculator = models.CharField(max_length=255, null=True)
    verified_date = models.DateTimeField(max_length=255, null=True)
    quotation_by = models.CharField(max_length=255, null=True)
    quotation_date = models.DateTimeField(null=True)
    assigned_by = models.CharField(max_length=255, null=True)
    assigned_date = models.DateTimeField(null=True)
    status_date = models.DateTimeField(auto_now=True)
    request_quotation_ref = models.CharField(max_length=255, null=True)
    request_credit_charged = models.CharField(max_length=255, null=True)
    package_cost_currency = models.CharField(max_length=255, null=True)
    verification_status = models.CharField(max_length=255, null=True, default="00")
    verified_by = models.CharField(max_length=255, null=True)
    adverse_status = models.CharField(max_length=255, null=True)
    final_notify = models.BooleanField(default=False)
    #
    package = models.ForeignKey("main.Package", models.CASCADE, db_constraint=True)
    negative = models.BooleanField(
        max_length=200, default=False, db_column="callback_url"
    )


    class Meta:
        db_table = "pel_psmt_request"
        managed = False
        ordering = ["-pk", "bg_dataset_name"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class Module(models.Model):

    module_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=255, null=True, unique=True)
    status = models.CharField(max_length=255, null=True, default="11")
    module_date_added = models.DateField(auto_now_add=True)
    module_added_by = models.CharField(max_length=255, null=True)
    module_verified_by = models.CharField(max_length=255, null=True)
    module_code = models.CharField(max_length=255, null=True)
    module_parent = models.CharField(max_length=255, null=True)
    module_cost = models.CharField(max_length=255, null=True)
    cost_review = models.CharField(max_length=255, null=True)
    module_role = models.CharField(max_length=255, null=True)
    module_cost_currency = models.CharField(max_length=255, null=True)
    module_credits = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "pel_module"
        managed = False

    def __str__(self):
        return self.module_name


class PackageModule(models.Model):
    modulepackage_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=255, default="00")
    added_by = models.CharField(max_length=255, null=True)
    added_date = models.DateField(auto_now_add=True)
    verified_by = models.CharField(max_length=255, null=True)
    verified_date = models.CharField(max_length=255, null=True)
    package_id = models.CharField(max_length=255, null=True)
    package_name = models.CharField(max_length=255, null=True)
    module_id = models.CharField(max_length=255, null=True)
    module_cost = models.CharField(max_length=255, null=True)
    cost_currency = models.CharField(max_length=255, null=True)
    cost_review = models.CharField(max_length=255, null=True)
    package_data_type = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.module_name

    class Meta:
        db_table = "pel_packages_module"
        managed = False


class BgRequestModule(models.Model):
    request_package_id = models.AutoField(primary_key=True)
    request_ref_number = models.ForeignKey(
        "main.PSMTRequest",
        models.CASCADE,
        to_field="request_ref_number",
        related_name="modules",
        related_query_name="modules",
        db_column="request_ref_number",
        null=True,
    )
    status = models.CharField(max_length=255, null=True, default="00")
    client_id = models.CharField(max_length=255, null=True)
    package_id = models.CharField(max_length=255, null=True)
    package_name = models.CharField(max_length=255, null=True)
    module_name = models.CharField(max_length=255, null=True)
    request_type = models.CharField(max_length=255, null=True)
    request_id = models.CharField(max_length=255, null=True)
    module_id = models.CharField(max_length=255, null=True)
    parent_module_id = models.CharField(max_length=255, null=True)
    module_cost_quote = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "pel_psmt_request_modules"
        managed = False


class Package(models.Model):
    package_id = models.AutoField(
        primary_key=True,
    )
    package_name = models.CharField(max_length=255, null=False)
    package_cost = models.CharField(max_length=255, null=True)
    package_status = models.CharField(max_length=255, null=False, default="22")
    package_added_by = models.CharField(max_length=255, null=True)
    package_added_date = models.CharField(max_length=255, null=True)
    package_data = models.CharField(max_length=255, null=True)
    package_verified_by = models.CharField(max_length=255, null=True)
    package_verified_date = models.CharField(max_length=255, null=True)
    dataset_id = models.CharField(max_length=255, null=True)
    package_currency = models.CharField(max_length=255, null=True)
    package_min = models.CharField(max_length=255, null=True)
    package_max = models.CharField(max_length=255, null=True)
    package_credits = models.CharField(max_length=255, null=True)
    package_general = models.CharField(max_length=255, null=True, default=0)
    package_cost_discount = models.CharField(max_length=255, null=True)
    package_credits_discount = models.CharField(max_length=255, null=True)
    package_data_type = models.CharField(max_length=255, null=True)

    @property
    def modules(self):
        return PackageModule.objects.filter(
            package_id=self.package_id, status="11"
        ).all()

    class Meta:
        db_table = "pel_package"
        managed = False
