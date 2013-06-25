from django.contrib import admin
from manager.models import Poll

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
    (None,	{'fields':['uid']}),
    (None,	{'fields':['asset_code']}),
    (None,	{'fields':['asset_category']}),
    (None,	{'fields':['region']}),
    (None,	{'fields':['unit']}),
    (None,	{'fields':['location']}),
    (None,  {'fields':['floor']}),
    (None,  {'fields':['username']}),
    (None,  {'fields':['empcode']}),
    (None,  {'fields':['designation']}),
    (None,  {'fields':['department']}),
    (None,	{'fields':['machinename']}),
    (None,	{'fields':['role']}),
    (None,	{'fields':['model_name']}),
    (None,	{'fields':['s_no']}),
    (None,	{'fields':['processor']}),
    (None,	{'fields':['hdd']}),
    (None,	{'fields':['ram']}),
    (None,	{'fields':['os']}),
    (None,	{'fields':['warr_amc']}),
    (None,	{'fields':['warr_vend']}),
    (None,	{'fields':['warr_start_date']}),
    (None,	{'fields':['warr_exp_date']}),
    (None,	{'fields':['company']}),
    (None,	{'fields':['po_details']}),
    (None,  {'fields':['working']}),
    ]
    list_display = ('id','uid', 'asset_code','asset_category','region','unit','location','floor','username','empcode','designation','department','machinename','role','model_name','s_no','processor','hdd','ram','os','warr_amc','warr_vend','warr_start_date','warr_exp_date','company','po_details','working','ram_change_date','hdd_change_date')
    search_fields = ['machinename']

admin.site.register(Poll, PollAdmin)