from django.db import models


class BusinessCompanyReg(models.Model):
    company_reg_id = models.AutoField(primary_key=True, unique=True, editable=False)
    business_name = models.CharField(
        max_length=255,
        db_column="company_name",
    )

    status = models.CharField(max_length=255, default="11")
    kra_pin = models.CharField(max_length=255, blank=True, null=True)
    registration_number = models.CharField(
        max_length=255, blank=False, null=True, unique=True
    )
    registration_date = models.CharField(max_length=255, blank=False, null=True)

    objective = models.CharField(
        max_length=255,
        default="-",
        blank=True,
        null=True,
        help_text="Added specifically for NGO and Society",
    )
    member_count = models.CharField(
        max_length=255,
        default="-",
        null=True,
        blank=True,
        help_text="Added specifically for NGO",
    )

    physical_address = models.CharField(max_length=255, db_column="address")
    postal_address = models.CharField(
        max_length=255,
        null=True,
        blank=False,
    )
    branches = models.TextField(blank=True, null=True, db_column="offices")

    email = models.CharField(
        max_length=355, null=True, blank=True, db_column="email_address"
    )
    phone_number = models.CharField(max_length=255, db_column="mobile_number")
    verified = models.BooleanField(blank=False, null=True)

    request_ref_number = models.OneToOneField(
        "main.PSMTRequest",
        models.CASCADE,
        blank=True,
        null=True,
        db_column="search_id",
        to_field="request_ref_number",
        related_name="business",
    )

    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "pel_company_registration"
        ordering = ["-pk"]
        managed = False


class Encumbrance(models.Model):
    search_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, default="11")
    description_of_evidence = models.TextField(
        max_length=255, null=True, blank=True, db_column="description"
    )
    date_of_evidence = models.CharField(
        max_length=255, null=True, blank=True, db_column="date"
    )
    #
    verified_by = models.CharField(max_length=255, blank=True, null=True)
    review_notes = models.TextField(blank=True, null=True)
    review_status = models.CharField(
        max_length=255, blank=True, null=True, help_text="APPROVED or REJECTED"
    )
    verified_date = models.DateTimeField()
    secured_amounts = models.CharField(
        max_length=255, blank=True, null=True, db_column="amount_secured"
    )
    #
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    business = models.ForeignKey(
        "main.BusinessCompanyReg",
        models.CASCADE,
        db_column="business",
        related_name="encumbrances",
    )

    class Meta:
        db_table = "pel_company_encumbrances"
        managed = False


class EncumbrancePersonsEntitled(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    encumbrance = models.ForeignKey(
        "main.Encumbrance", models.CASCADE, related_name="persons_entitled", null=True
    )

    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)

    class Meta:
        db_table = "pel_company_persons_entitled"


class ShareCapital(models.Model):
    """
    {'name': 'ORDINARY', 'number_of_shares': 1000, 'nominal_value': 100.0}
    """

    business = models.ForeignKey(
        "main.BusinessCompanyReg",
        models.CASCADE,
        blank=True,
        null=True,
        related_name="share_capital",
    )
    number_of_shares = models.CharField(max_length=255, blank=False, null=True)
    nominal_value = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "pel_company_share_capital"

    pass


class Shares(models.Model):
    shares_id = models.AutoField(primary_key=True, unique=True)
    business = models.ForeignKey(
        "main.BusinessCompanyReg",
        models.CASCADE,
        blank=True,
        null=True,
        db_column="business",
        related_name="partners",
    )

    first_name = models.CharField(max_length=255, blank=False, null=True)
    second_name = models.CharField(max_length=255, blank=False, null=True)
    third_name = models.CharField(max_length=255, blank=False, null=True)

    status = models.CharField(max_length=255, default="11")
    share_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="name from external data, share_type in the db",
    )
    id_type = models.CharField(max_length=255, blank=True, null=True)
    #
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(
        max_length=255, blank=True, null=True, db_column="citizenship"
    )
    #
    id_number = models.CharField(max_length=255, blank=True, null=True)
    number_of_shares = models.CharField(
        max_length=255, blank=True, null=True, db_column="shares_number"
    )
    percentage = models.CharField(max_length=255, blank=True, null=True)
    #
    data_source = models.CharField(max_length=255, blank=True, null=True)
    review_notes = models.TextField(blank=True, null=True)
    review_status = models.CharField(
        max_length=255, blank=True, null=True, help_text="APPROVED or REJECTED"
    )

    #
    added_by = models.CharField(max_length=255, blank=True, null=True)
    verified_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "pel_company_shares_data"
        managed = False


class CompanyOfficialDetails(models.Model):
    role = models.CharField(max_length=255, blank=True, null=True)
    business = models.ForeignKey(
        "main.BusinessCompanyReg",
        models.CASCADE,
        related_name="officials",
        db_column="company_id",
    )
    name = models.CharField(max_length=255, blank=False, null=True)

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateField(auto_now=True, editable=False)

    class Meta:
        db_table = "pel_company_official_details"
