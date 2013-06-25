from django.db import models
from django .forms import ModelForm

class Poll(models.Model):
    uid = models.CharField(max_length=10, null=True)
    asset_code = models.CharField(max_length=200, null=True)
    asset_category = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=200, null=True)
    unit = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    floor = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    empcode = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)
    machinename = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=200, null=True)
    model_name = models.CharField(max_length=200, null=True)
    s_no = models.CharField(max_length=200)
    processor = models.CharField(max_length=200)
    hdd = models.CharField(max_length=200)
    ram = models.CharField(max_length=200)
    os = models.CharField(max_length=200)
    warr_amc = models.CharField(max_length=200, null=True)
    warr_vend = models.CharField(max_length=200, null=True)
    warr_start_date = models.CharField(max_length=200, null=True)
    warr_exp_date = models.CharField(max_length=200, null=True)
    company = models.CharField(max_length=200, null=True)
    po_details = models.CharField(max_length=200, null=True)
    working = models.IntegerField(max_length=10)
    ram_change_date = models.DateTimeField('date published')
    hdd_change_date = models.DateTimeField('date published')



class PollForm(ModelForm):
    class Meta:
        model = Poll
        # fields = ['uid','asset_code','asset_category','state',
        # 'hub','location','floor','server','empcode','designation',
        # 'department','username','role','model_name','s_no','processor',
        # 'hdd','ram','os','warr_amc','warr_vend','warr_start_date'
        # 'warr_exp_date','company','po_details'
        # ]