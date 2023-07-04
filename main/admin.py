from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PSMTRequest
from import_export.admin import ImportExportModelAdmin


@admin.register(PSMTRequest)
class psmtData(ImportExportModelAdmin):
    list_display = ('client_number', 'company_name', 'registration_number', 'dataset_citizenship', 'company_type')
