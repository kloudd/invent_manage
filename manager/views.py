# Create your views here.
from django.template import Context, loader
from django.core.urlresolvers import reverse
from manager.models import Poll, PollForm
from django.contrib import messages
from django.shortcuts import redirect
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponseRedirect
from datetime import datetime, date
import time
import json
import xlwt
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required



import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name:term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['machinename', 'ram',])

        found_entries = Poll.objects.filter(entry_query)
    else:
    	found_entries = Poll.objects.order_by('id')



    return render_to_response('manager/view2.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))

@staff_member_required
def index2(request):
	return render(request, 'manager/index2.html', locals())

@staff_member_required
def view(request):
	orderby = Poll.objects.order_by('id')
	return render(request, 'manager/view2.html', locals())

@staff_member_required
def add(request):
	form = PollForm()
	return render(request, 'manager/add2.html', locals())
# 	p = Poll(
# 		uid = 0
# 	    asset_code = "abc"
# 	    asset_category = "abc"
# 	    region = "abc"
# 	    unit = "abc"
# 	    location = "abc"
# 	    floor = "abc"
# 	    username = "abc"
# 	    empcode = "abc"
# 	    designation = "abc"
# 	    department = "abc"
# 	    machinename = "abc"
# 	    role = "abc"
# 	    model_name = "abc"
# 	    s_no = "abc"
# 	    processor = "abc"
# 	    hdd = "abc"
# 	    ram = "abc"
# 	    os = "abc"
# 	    warr_amc = "abc"
# 	    warr_vend = "abc"
# 	    warr_start_date = "abc"
# 	    warr_exp_date = "abc"
# 	    company = "abc"
# 	    po_details = "abc"
# )
@staff_member_required
def edit(request,id):
	obj = Poll.objects.get(id=id)
	if obj is not None:
		print "found object", obj
		return render(request, 'manager/edit2.html',locals())
	# placeholder error message
	print "did not find the obj"
	return render(request, 'manager/index2.html', locals())

@staff_member_required
def delete(request,id):
	obj = Poll.objects.get(id=id)
	if obj is not None:
		obj.delete()
		return HttpResponseRedirect("/manager/view/")
	# placeholder error message
	print "did not find the obj"
	return render(request, 'manager/index2.html', locals())

@staff_member_required
def handle_add(request):
	if request.method == 'POST':
		print request.POST
		uid = request.POST.get('uid')
		asset_code = request.POST.get('asset_code')
		asset_category = request.POST.get('asset_category')
		region = request.POST.get('region')
		unit = request.POST.get('unit')
		location = request.POST.get('location')
		floor = request.POST.get('floor')
		username = request.POST.get('username')
		empcode = request.POST.get('empcode')
		designation = request.POST.get('designation')
		department = request.POST.get('department')
		machinename = request.POST.get('machinename')
		role = request.POST.get('role')
		model_name = request.POST.get('model_name')
		s_no = request.POST.get('s_no')
		processor = request.POST.get('processor')
		hdd = request.POST.get('hdd')
		ram = request.POST.get('ram')
		os = request.POST.get('os')
		warr_amc = request.POST.get('warr_amc')
		warr_vend = request.POST.get('warr_vend')
		warr_start_date = request.POST.get('warr_start_date')
		warr_exp_date = request.POST.get('warr_exp_date')
		company = request.POST.get('company')
		po_details = request.POST.get('po_details')
		ram_change_date = datetime.now()
		hdd_change_date = datetime.now()
		working = 1
		# if uid & asset_code && asset_category && region && unit && location && floor && username && empcode &&designation && department && machinename && role && model_name && s_no && processor && hdd && ram && os && warr_amc && warr_vend && warr_start_date && warr_exp_date && company && po_details :
		flag=0
		if department=="" or role=="" or model_name=="" or asset_category=="" :
			flag=1

		orderby = Poll.objects.order_by('id')
		if orderby:
			for poll in orderby:
				if s_no==poll.s_no and s_no:
					flag=1
					print "alreadyinuse"
					return render(request, 'manager/inuse.html', locals())

		print uid
		p = Poll(uid=uid,
			asset_code = asset_code,
			asset_category = asset_category,
			region = region,
			unit = unit,
			location = location,
			floor = floor,
			username = username,
			empcode = empcode,
			designation = designation,
			department = department,
			machinename = machinename,
			role = role,
			model_name = model_name,
			s_no = s_no,
			processor = processor,
			hdd = hdd,
			ram = ram,
			os = os,
			warr_amc = warr_amc,
			warr_vend = warr_vend,
			warr_start_date = warr_start_date,
			warr_exp_date = warr_exp_date,
			company = company,
			po_details = po_details,
			working = working,
			ram_change_date = ram_change_date,
			hdd_change_date = hdd_change_date)
		if flag==0:
			p.save()
		
		print 'saving form'
		return HttpResponseRedirect("/manager/view/")
	# else:
		# return render(request, 'manager/notadded.html', locals())

	else:
		form = PollForm()
		return render(request, 'manager/add2.html', locals())

@staff_member_required
def contact_us(request):
	orderby = Poll.objects.order_by('id')
	count_working = 0
	count_not_working = 0
	total = 0
	if orderby:
		for poll in orderby:
			if poll.working == 1:
				count_working=count_working+1
				total = total + 1
			if poll.working == 0:
				count_not_working=count_not_working+1
				total = total + 1
	return render(request, 'manager/contact_us2.html', locals())

@csrf_exempt
def post_config(request):
	if request.method == 'POST':
		json_data = simplejson.loads(request.raw_post_data)
		print json_data
		try:
			flag = 0
			client_data = dict(json_data['client_data'])
			machinename = client_data['machinename']
			s_no = client_data['s_no']
			processor = client_data['processor']
			ram = client_data['ram']
			hdd = client_data['hdd']
			os = client_data['os']
			ram_change_date = datetime.now()
			hdd_change_date = datetime.now()
			orderby = Poll.objects.order_by('id')
			if orderby:
				for poll in orderby:
					if poll.s_no==s_no:
						poll.working = 1
						poll.machinename = machinename
						poll.processor = processor
						if poll.ram != ram:
							poll.ram_change_date = ram_change_date
						if poll.hdd != hdd:
							poll.hdd_change_date = hdd_change_date
						poll.ram = ram
						poll.hdd = hdd
						poll.os = os
						poll.save()
						flag=1
						break
			working = 1
			p = Poll(uid='',
			asset_code = '',
			asset_category = '',
			region = '',
			unit = '',
			location = '',
			floor = '',
			username = '',
			empcode = '',
			designation = '',
			department = '',
			machinename = machinename,
			role = '',
			model_name = '',
			s_no = s_no,
			processor = processor,
			hdd = hdd,
			ram = ram,
			os = os,
			warr_amc = '',
			warr_vend = '',
			warr_start_date = '',
			warr_exp_date = '',
			company = '',
			po_details = '',
			working = working,
			ram_change_date=ram_change_date,
			hdd_change_date=hdd_change_date)
			if flag==0:
				p.save() 
		except KeyError:
			return HttpResponseServerError("Malformed Data, missing key")
		return HttpResponse(client_data, content_type="application/json", status=200)

	else:
		return HttpResponse("Only JSON post accepted", status=404)


@staff_member_required
def exp(request):
	book = xlwt.Workbook(encoding='utf8')
	sheet = book.add_sheet('untitled')

	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

	orderby = Poll.objects.order_by('id')
	sheet.write(1,0,"ID",style=default_style)
	sheet.write(1,1,"UID",style=default_style)
	sheet.write(1,2,"ASSET CODE",style=default_style)
	sheet.write(1,3,"ASSET CATEGORY",style=default_style)
	sheet.write(1,4,"region",style=default_style)
	sheet.write(1,5,"unit",style=default_style)
	sheet.write(1,6,"LOCATION",style=default_style)
	sheet.write(1,7,"FLOOR",style=default_style)
	sheet.write(1,8,"username",style=default_style)
	sheet.write(1,9,"EMPCODE",style=default_style)
	sheet.write(1,10,"DESIGNATION",style=default_style)
	sheet.write(1,11,"DEPARTMENT",style=default_style)
	sheet.write(1,12,"MACHINE NAME",style=default_style)
	sheet.write(1,13,"ROLE",style=default_style)
	sheet.write(1,14,"MODEL NAME",style=default_style)
	sheet.write(1,15,"S NO",style=default_style)
	sheet.write(1,16,"PROCESSOR",style=default_style)
	sheet.write(1,17,"HDD",style=default_style)
	sheet.write(1,18,"RAM",style=default_style)
	sheet.write(1,19,"OS",style=default_style)
	sheet.write(1,20,"WARR AMC",style=default_style)
	sheet.write(1,21,"WARR VEND",style=default_style)
	sheet.write(1,22,"WARR START DATE",style=default_style)
	sheet.write(1,23,"WARR EXP DATE",style=default_style)
	sheet.write(1,24,"COMPANY",style=default_style)
	sheet.write(1,25,"PO DETAILS",style=default_style)
	sheet.write(1,26,"WORKING",style=default_style)

	if orderby:
		row=0
		for poll in orderby:
			
			if poll.working == 1:
				style = default_style
				sheet.write(row+2, 0, poll.id, style=style)
				sheet.write(row+2, 1, poll.uid, style=style)
				sheet.write(row+2, 2, poll.asset_code, style=style)
				sheet.write(row+2, 3, poll.asset_category, style=style)
				sheet.write(row+2, 4, poll.region, style=style)
				sheet.write(row+2, 5, poll.unit, style=style)
				sheet.write(row+2, 6, poll.location, style=style)
				sheet.write(row+2, 7, poll.floor, style=style)
				sheet.write(row+2, 8, poll.username, style=style)
				sheet.write(row+2, 9, poll.empcode, style=style)
				sheet.write(row+2, 10, poll.designation, style=style)
				sheet.write(row+2, 11, poll.department, style=style)
				sheet.write(row+2, 12, poll.machinename, style=style)
				sheet.write(row+2, 13, poll.role, style=style)
				sheet.write(row+2, 14, poll.model_name, style=style)
				sheet.write(row+2, 15, poll.s_no, style=style)
				sheet.write(row+2, 16, poll.processor, style=style)
				sheet.write(row+2, 17, poll.hdd, style=style)
				sheet.write(row+2, 18, poll.ram, style=style)
				sheet.write(row+2, 19, poll.os, style=style)
				sheet.write(row+2, 20, poll.warr_amc, style=style)
				sheet.write(row+2, 21, poll.warr_vend, style=style)
				sheet.write(row+2, 22, poll.warr_start_date, style=style)
				sheet.write(row+2, 23, poll.warr_exp_date, style=style)
				sheet.write(row+2, 24, poll.company, style=style)
				sheet.write(row+2, 25, poll.po_details, style=style)
				sheet.write(row+2, 26, poll.working, style=style)
				row = row+1




				

	# for row, rowdata in enumerate(values_list):
	#     for col, val in enumerate(rowdata):
	#         if isinstance(val, datetime):
	#             style = datetime_style
	#         elif isinstance(val, date):
	#             style = date_style
	#         else:
	#             style = default_style

	#         sheet.write(row+2, col, val, style=style)

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=example.xls'
	book.save(response)
	return response

@staff_member_required
def logout(request):
	return HttpResponseRedirect("/admin/logout/")

@staff_member_required
def adminpage(request):
	return HttpResponseRedirect("/admin/")

staff_member_required
def handle_edit(request):
	if request.method == 'POST':
		print request.POST
		id = request.POST.get('id')
		uid = request.POST.get('uid')
		asset_code = request.POST.get('asset_code')
		asset_category = request.POST.get('asset_category')
		region = request.POST.get('region')
		unit = request.POST.get('unit')
		location = request.POST.get('location')
		floor = request.POST.get('floor')
		username = request.POST.get('username')
		empcode = request.POST.get('empcode')
		designation = request.POST.get('designation')
		department = request.POST.get('department')
		machinename = request.POST.get('machinename')
		role = request.POST.get('role')
		model_name = request.POST.get('model_name')
		s_no = request.POST.get('s_no')
		processor = request.POST.get('processor')
		hdd = request.POST.get('hdd')
		ram = request.POST.get('ram')
		os = request.POST.get('os')
		warr_amc = request.POST.get('warr_amc')
		warr_vend = request.POST.get('warr_vend')
		warr_start_date = request.POST.get('warr_start_date')
		warr_exp_date = request.POST.get('warr_exp_date')
		company = request.POST.get('company')
		po_details = request.POST.get('po_details')
		working = request.POST.get('working')
		# if uid & asset_code && asset_category && region && unit && location && floor && username && empcode &&designation && department && machinename && role && model_name && s_no && processor && hdd && ram && os && warr_amc && warr_vend && warr_start_date && warr_exp_date && company && po_details :
		print uid

		obj = Poll.objects.get(id=id)
		if obj is not None:
			obj.uid=uid
			obj.asset_code = asset_code
			obj.asset_category = asset_category
			obj.region = region
			obj.unit = unit
			obj.location = location
			obj.floor = floor
			obj.username = username
			obj.empcode = empcode
			obj.designation = designation
			obj.department = department
			obj.machinename = machinename
			obj.role = role
			obj.model_name = model_name
			obj.s_no = s_no
			obj.processor = processor
			obj.hdd = hdd
			obj.ram = ram
			obj.os = os
			obj.warr_amc = warr_amc
			obj.warr_vend = warr_vend
			obj.warr_start_date = warr_start_date
			obj.warr_exp_date = warr_exp_date
			obj.company = company
			obj.po_details = po_details
			obj.working = working
			obj.save()
		return HttpResponseRedirect("/manager/view/")
	else:
		form = PollForm()
		return render(request, 'manager/add2.html', locals())

@staff_member_required
def add_offline_stock(request):
	form = PollForm()
	return render(request, 'manager/addofflinestock.html', locals())

@staff_member_required
def view_offline_stock(request):
	orderby = Poll.objects.order_by('id')
	return render(request, 'manager/viewofflinestock.html', locals())

@staff_member_required
def handle_offline_add(request):
	if request.method == 'POST':
		print request.POST
		model_name = request.POST.get('model_name')
		s_no = request.POST.get('s_no')
		processor = request.POST.get('processor')
		hdd = request.POST.get('hdd')
		ram = request.POST.get('ram')
		os = request.POST.get('os')
		working = 0
		hdd_change_date = datetime.now()
		ram_change_date = datetime.now()
		flag = 0
		if model_name=="" or s_no=="" or processor=="" or hdd=="" or ram=="" or os=="":
			flag=1
		orderby = Poll.objects.order_by('id')
		if orderby:
			for poll in orderby:
				if s_no==poll.s_no and s_no:
					flag=1
					print "alreadyinuse"
					return render(request, 'manager/inuse.html', locals())
		p = Poll(uid='',
			asset_code = '',
			asset_category = '',
			region = '',
			unit = '',
			location = '',
			floor = '',
			username = '',
			empcode = '',
			designation = '',
			department = '',
			machinename = '',
			role = '',
			model_name = model_name,
			s_no = s_no,
			processor = processor,
			hdd = hdd,
			ram = ram,
			os = os,
			warr_amc = '',
			warr_vend = '',
			warr_start_date = '',
			warr_exp_date = '',
			company = '',
			po_details = '',
			working = working,
			ram_change_date = ram_change_date,
			hdd_change_date = hdd_change_date)
		if flag == 0:
			p.save();
		print 'saving form'
		return HttpResponseRedirect("/manager/view_offline_stock/")
	# else:
		# return render(request, 'manager/notadded.html', locals())

	else:
		form = PollForm()
		return render(request, 'manager/addofflinestock.html', locals())


@staff_member_required
def handle_offline_edit(request):
	if request.method == 'POST':
		print request.POST
		id = request.POST.get('id')
		model_name = request.POST.get('model_name')
		s_no = request.POST.get('s_no')
		processor = request.POST.get('processor')
		hdd = request.POST.get('hdd')
		ram = request.POST.get('ram')
		os = request.POST.get('os')
		working = request.POST.get('working')
		obj = Poll.objects.get(id=id)
		if obj is not None:
			obj.uid=""
			obj.asset_code = ""
			obj.asset_category = ""
			obj.region = ""
			obj.unit = ""
			obj.location = ""
			obj.floor = ""
			obj.username = ""
			obj.empcode = ""
			obj.designation = ""
			obj.department = ""
			obj.machinename = ""
			obj.role = ""


			obj.model_name=model_name
			obj.s_no = s_no
			obj.processor = processor
			obj.hdd = hdd
			obj.ram = ram
			obj.os = os
			obj.working = working

			obj.warr_amc = ""
			obj.warr_vend = ""
			obj.warr_start_date = ""
			obj.warr_exp_date = ""
			obj.company = ""
			obj.po_details = ""


			obj.save()
			return HttpResponseRedirect("/manager/view_offline_stock/")
	else:
		form = PollForm()
		return render(request, 'manager/add2.html', locals())

@staff_member_required
def editoffline(request,id):
	obj = Poll.objects.get(id=id)
	if obj is not None:
		print "found object", obj
		return render(request, 'manager/editoffline.html',locals())
	# placeholder error message
	print "did not find the obj"
	return render(request, 'manager/index2.html', locals())


@staff_member_required
def deleteoffline(request,id):
	obj = Poll.objects.get(id=id)
	if obj is not None:
		obj.delete()
		return HttpResponseRedirect("/manager/view_offline_stock/")
	# placeholder error message
	print "did not find the obj"
	return render(request, 'manager/index2.html', locals())

@staff_member_required
def expoffline(request):
	book = xlwt.Workbook(encoding='utf8')
	sheet = book.add_sheet('untitled')

	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

	orderby = Poll.objects.order_by('id')
	sheet.write(1,0,"ID",style=default_style)
	sheet.write(1,1,"UID",style=default_style)
	sheet.write(1,2,"ASSET CODE",style=default_style)
	sheet.write(1,3,"ASSET CATEGORY",style=default_style)
	sheet.write(1,4,"region",style=default_style)
	sheet.write(1,5,"unit",style=default_style)
	sheet.write(1,6,"LOCATION",style=default_style)
	sheet.write(1,7,"FLOOR",style=default_style)
	sheet.write(1,8,"username",style=default_style)
	sheet.write(1,9,"EMPCODE",style=default_style)
	sheet.write(1,10,"DESIGNATION",style=default_style)
	sheet.write(1,11,"DEPARTMENT",style=default_style)
	sheet.write(1,12,"MACHINE NAME",style=default_style)
	sheet.write(1,13,"ROLE",style=default_style)
	sheet.write(1,14,"MODEL NAME",style=default_style)
	sheet.write(1,15,"S NO",style=default_style)
	sheet.write(1,16,"PROCESSOR",style=default_style)
	sheet.write(1,17,"HDD",style=default_style)
	sheet.write(1,18,"RAM",style=default_style)
	sheet.write(1,19,"OS",style=default_style)
	sheet.write(1,20,"WARR AMC",style=default_style)
	sheet.write(1,21,"WARR VEND",style=default_style)
	sheet.write(1,22,"WARR START DATE",style=default_style)
	sheet.write(1,23,"WARR EXP DATE",style=default_style)
	sheet.write(1,24,"COMPANY",style=default_style)
	sheet.write(1,25,"PO DETAILS",style=default_style)
	sheet.write(1,26,"WORKING",style=default_style)

	if orderby:
		row=0
		for poll in orderby:
			
			if poll.working == 0:
				style = default_style
				sheet.write(row+2, 0, poll.id, style=style)
				sheet.write(row+2, 1, poll.uid, style=style)
				sheet.write(row+2, 2, poll.asset_code, style=style)
				sheet.write(row+2, 3, poll.asset_category, style=style)
				sheet.write(row+2, 4, poll.region, style=style)
				sheet.write(row+2, 5, poll.unit, style=style)
				sheet.write(row+2, 6, poll.location, style=style)
				sheet.write(row+2, 7, poll.floor, style=style)
				sheet.write(row+2, 8, poll.username, style=style)
				sheet.write(row+2, 9, poll.empcode, style=style)
				sheet.write(row+2, 10, poll.designation, style=style)
				sheet.write(row+2, 11, poll.department, style=style)
				sheet.write(row+2, 12, poll.machinename, style=style)
				sheet.write(row+2, 13, poll.role, style=style)
				sheet.write(row+2, 14, poll.model_name, style=style)
				sheet.write(row+2, 15, poll.s_no, style=style)
				sheet.write(row+2, 16, poll.processor, style=style)
				sheet.write(row+2, 17, poll.hdd, style=style)
				sheet.write(row+2, 18, poll.ram, style=style)
				sheet.write(row+2, 19, poll.os, style=style)
				sheet.write(row+2, 20, poll.warr_amc, style=style)
				sheet.write(row+2, 21, poll.warr_vend, style=style)
				sheet.write(row+2, 22, poll.warr_start_date, style=style)
				sheet.write(row+2, 23, poll.warr_exp_date, style=style)
				sheet.write(row+2, 24, poll.company, style=style)
				sheet.write(row+2, 25, poll.po_details, style=style)
				sheet.write(row+2, 26, poll.working, style=style)
				row = row+1




				

	# for row, rowdata in enumerate(values_list):
	#     for col, val in enumerate(rowdata):
	#         if isinstance(val, datetime):
	#             style = datetime_style
	#         elif isinstance(val, date):
	#             style = date_style
	#         else:
	#             style = default_style

	#         sheet.write(row+2, col, val, style=style)

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=example.xls'
	book.save(response)
	return response

@staff_member_required
def expfull(request):
	book = xlwt.Workbook(encoding='utf8')
	sheet = book.add_sheet('untitled')

	default_style = xlwt.Style.default_style
	datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
	date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

	orderby = Poll.objects.order_by('id')
	sheet.write(1,0,"ID",style=default_style)
	sheet.write(1,1,"UID",style=default_style)
	sheet.write(1,2,"ASSET CODE",style=default_style)
	sheet.write(1,3,"ASSET CATEGORY",style=default_style)
	sheet.write(1,4,"region",style=default_style)
	sheet.write(1,5,"unit",style=default_style)
	sheet.write(1,6,"LOCATION",style=default_style)
	sheet.write(1,7,"FLOOR",style=default_style)
	sheet.write(1,8,"username",style=default_style)
	sheet.write(1,9,"EMPCODE",style=default_style)
	sheet.write(1,10,"DESIGNATION",style=default_style)
	sheet.write(1,11,"DEPARTMENT",style=default_style)
	sheet.write(1,12,"MACHINE NAME",style=default_style)
	sheet.write(1,13,"ROLE",style=default_style)
	sheet.write(1,14,"MODEL NAME",style=default_style)
	sheet.write(1,15,"S NO",style=default_style)
	sheet.write(1,16,"PROCESSOR",style=default_style)
	sheet.write(1,17,"HDD",style=default_style)
	sheet.write(1,18,"RAM",style=default_style)
	sheet.write(1,19,"OS",style=default_style)
	sheet.write(1,20,"WARR AMC",style=default_style)
	sheet.write(1,21,"WARR VEND",style=default_style)
	sheet.write(1,22,"WARR START DATE",style=default_style)
	sheet.write(1,23,"WARR EXP DATE",style=default_style)
	sheet.write(1,24,"COMPANY",style=default_style)
	sheet.write(1,25,"PO DETAILS",style=default_style)
	sheet.write(1,26,"WORKING",style=default_style)

	if orderby:
		row=0
		for poll in orderby:
			style = default_style
			sheet.write(row+2, 0, poll.id, style=style)
			sheet.write(row+2, 1, poll.uid, style=style)
			sheet.write(row+2, 2, poll.asset_code, style=style)
			sheet.write(row+2, 3, poll.asset_category, style=style)
			sheet.write(row+2, 4, poll.region, style=style)
			sheet.write(row+2, 5, poll.unit, style=style)
			sheet.write(row+2, 6, poll.location, style=style)
			sheet.write(row+2, 7, poll.floor, style=style)
			sheet.write(row+2, 8, poll.username, style=style)
			sheet.write(row+2, 9, poll.empcode, style=style)
			sheet.write(row+2, 10, poll.designation, style=style)
			sheet.write(row+2, 11, poll.department, style=style)
			sheet.write(row+2, 12, poll.machinename, style=style)
			sheet.write(row+2, 13, poll.role, style=style)
			sheet.write(row+2, 14, poll.model_name, style=style)
			sheet.write(row+2, 15, poll.s_no, style=style)
			sheet.write(row+2, 16, poll.processor, style=style)
			sheet.write(row+2, 17, poll.hdd, style=style)
			sheet.write(row+2, 18, poll.ram, style=style)
			sheet.write(row+2, 19, poll.os, style=style)
			sheet.write(row+2, 20, poll.warr_amc, style=style)
			sheet.write(row+2, 21, poll.warr_vend, style=style)
			sheet.write(row+2, 22, poll.warr_start_date, style=style)
			sheet.write(row+2, 23, poll.warr_exp_date, style=style)
			sheet.write(row+2, 24, poll.company, style=style)
			sheet.write(row+2, 25, poll.po_details, style=style)
			sheet.write(row+2, 26, poll.working, style=style)
			row = row+1




				

	# for row, rowdata in enumerate(values_list):
	#     for col, val in enumerate(rowdata):
	#         if isinstance(val, datetime):
	#             style = datetime_style
	#         elif isinstance(val, date):
	#             style = date_style
	#         else:
	#             style = default_style

	#         sheet.write(row+2, col, val, style=style)

	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=example.xls'
	book.save(response)
	return response


def searchoffline(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        
        entry_query = get_query(query_string, ['model_name', 'ram',])

        found_entries = Poll.objects.filter(entry_query)
    else:
    	found_entries = Poll.objects.order_by('id')
    return render_to_response('manager/viewofflinestock.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))
