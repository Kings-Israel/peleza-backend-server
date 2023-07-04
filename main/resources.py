from import_export import resources
from .models import PSMTRequest


class PSMTRequestResource(resources.ModelResource):
    class meta:
        model = PSMTRequest
