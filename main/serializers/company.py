from main.models.company import (
    BusinessCompanyReg,
    CompanyOfficialDetails,
    Encumbrance,
    ShareCapital,
    Shares,
)
from rest_framework import serializers


class EncumbranceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "pk",
            "date_of_evidence",
            "description_of_evidence",
            "secured_amounts",
        )
        model = Encumbrance


class ShareCapitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareCapital
        fields = ("pk", "number_of_shares", "nominal_value", "name")


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shares
        fields = (
            "pk",
            "first_name",
            "second_name",
            "third_name",
            "id_type",
            "id_number",
            "number_of_shares",
            "address",
            "description",
            "nationality",
        )


class CompanyOfficialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyOfficialDetails
        fields = ("pk", "role", "name")


class BusinessCompanyRegSerializer(serializers.ModelSerializer):
    share_capital = ShareCapitalSerializer(many=True)
    partners = ShareSerializer(many=True)
    encumbrances = EncumbranceSerializer(many=True)
    officials = CompanyOfficialSerializer(many=True, default=[])

    class Meta:
        model = BusinessCompanyReg
        fields = (
            "pk",
            "business_name",
            "status",
            "kra_pin",
            "registration_number",
            "registration_date",
            "objective",
            "member_count",
            "physical_address",
            "postal_address",
            "branches",
            "email",
            "phone_number",
            "request_ref_number",
            "verified",
            "encumbrances",
            "share_capital",
            "partners",
            "officials",
            "type",
        )
