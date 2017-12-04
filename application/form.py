from django import forms

class AppDetailsForm(forms.Form):

    app_detail_basic_appname = forms.CharField(required=True)
    # app_detail_basic_replicas = forms.IntegerField(required=True,
    #                                             error_messages={'required': "此欄必填"})
    # app_detail_custom_port = forms.IntegerField(required=True,error_messages={'required': "此欄必填"})
    #
    # app_detail_account_app_login = forms.CharField(required=True,error_messages={'required': "此欄必填"})
    # app_detail_account_app_password = forms.CharField(required=True,error_messages={'required': "此欄必填"})
    # app_detail_account_app_retype_password = forms.CharField(required=True,error_messages={'required': "此欄必填"})
    #
    # app_detail_app_capacity = forms.IntegerField(required=True,error_messages={'required': "此欄必填"})
    #
    # app_detail_account_db_name = forms.CharField(required=True,error_messages={'required': "此欄必填"})
    # app_detail_db_capacity = forms.IntegerField(required=True,error_messages={'required': "此欄必填"})
    #
    # app_detail_resource_cpu_request = forms.IntegerField(required=True,error_messages={'required': "此欄必填"})
    # app_detail_resource_ram_request = forms.IntegerField(required=True,error_messages={'required': "此欄必填"})
    #
    # app_detail_ingress_vhost = forms.CharField(required=True,error_messages={'required': "此欄必填"})


