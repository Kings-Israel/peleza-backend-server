from authentication.serializers import UserMiniSerializer
from main.serializers.company import BusinessCompanyRegSerializer
from rest_framework import serializers
from main.models.psmt import Package, BgRequestModule, PSMTRequest


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ("package_name", "package_id")


class RequestModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BgRequestModule
        fields = (
            "module_name",
            "status",
            "module_id",
        )


class PSMTRequestSerializer(serializers.ModelSerializer):
    dataset_name = serializers.SerializerMethodField(read_only=False)
    package_name = serializers.RelatedField(read_only=True)
    request_package = serializers.CharField(required=False)
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = PSMTRequest
        fields = (
            "pk",
            "request_type",
            "request_package",
            "request_ref_number",
            "registration_number",
            "package_name",
            "request_date",
            "request_plan",
            "percentage",
            "status",
            "package_id",
            "negative",
            "comments",
            "verified_date",
            "client_id",
            "client_login_id",
            "bg_dataset_name",
            "company_name",
            "status_date",
            "company_type",
            "client_number",
            "dataset_incorporation_no",
            "dataset_kra_pin",
            "package_cost_currency",
            "parent_name",
            "dataset_name",
            "bg_dataset_idnumber",
            "bg_dataset_mobile",
            "bg_dataset_email",
            "client_name",
            "request_dataset_cat",
            "dataset_citizenship",
        )
        extra_kwargs = {
            "request_ref_number": {"read_only": True},
            "dataset_name": {"required": True},
        }

    def get_dataset_name(self, obj):
        return obj.bg_dataset_name

    def get_percentage(self, obj):
        modules = obj.modules.all()
        module_status = [
            (i.status) for i in modules if obj.status == "11" or obj.status == 11
        ]
        return (
            (len(module_status) / modules.count()) * 100
            if modules.count() != 0 and module_status
            else 0.00
        )


class PSMTRequestDetailSerializer(PSMTRequestSerializer):
    business = BusinessCompanyRegSerializer(many=False)

    class Meta(PSMTRequestSerializer.Meta):
        fields = (
            "pk",
            "company_name",
            "client_id",
            "client_name",
            "user_name",
            "request_type",
            "request_package",
            "request_ref_number",
            "dataset_name",
            "registration_number",
            "package_name",
            "package",
            "request_date",
            "request_plan",
            "percentage",
            "status",
            "business",
            "verified_date",
        )

        extra_kwargs = {
            "request_ref_number": {"read_only": True},
            "dataset_name": {"required": True},
        }


class PIDVARequestDetailSerializer(PSMTRequestDetailSerializer):
    business = BusinessCompanyRegSerializer(many=False, required=False)

    class Meta(PSMTRequestDetailSerializer.Meta):
        extra_kwargs = {
            "package": {"read_only": True},
            "business": {"read_only": True, "required": False},
        }

        fields = PSMTRequestDetailSerializer.Meta.fields + (
            "verified_date",
            "verified_by",
        )


from django.utils.timezone import now


class RequestSerializer(serializers.Serializer):
    registration_number = serializers.CharField(required=True)
    package_id = serializers.IntegerField(required=True)
    module_id = serializers.IntegerField(required=True)
    dataset_name = serializers.CharField(required=True)
    client_number = serializers.CharField(required=True)
    dataset_citizenship = serializers.CharField(required=True)
    request_date = serializers.CharField(default=now().strftime("%d %b %Y %H:%M"))
