# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class PelPsmtRequestModules(models.Model):
    request_package_id = models.AutoField(primary_key=True)
    request_ref_number = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    package_id = models.CharField(max_length=255, blank=True, null=True)
    package_name = models.CharField(max_length=255, blank=True, null=True)
    module_name = models.CharField(max_length=255, blank=True, null=True)
    request_type = models.CharField(max_length=255, blank=True, null=True)
    request_id = models.CharField(max_length=255, blank=True, null=True)
    module_id = models.CharField(max_length=255, blank=True, null=True)
    parent_module_id = models.CharField(max_length=255, blank=True, null=True)
    module_cost_quote = models.CharField(max_length=255, blank=True, null=True)
    by_pass = models.DecimalField(max_digits=11, decimal_places=0, blank=True, null=True)
    valid = models.DecimalField(max_digits=11, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pel_psmt_request_modules'
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)