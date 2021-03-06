##--------------------------------------------------------------
# AuShadha Views for Visit Details and modification.
# Author: Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# License : GNU - GPL Version 3
# Date: 27-12-2012
##---------------------------------------------------------------


# General Django Imports----------------------------------

from django.shortcuts                import render_to_response
from django.http                     import Http404, HttpResponse, HttpResponseRedirect
from django.template                 import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth.models      import User
#from django.views.decorators.csrf   import csrf_exempt
from django.contrib.auth.views       import logout
from django.contrib.auth.decorators  import login_required
from django.forms.models             import modelformset_factory
from django.forms.formsets           import formset_factory
from django.core.paginator           import Paginator
from django.utils                    import simplejson

# General Module imports-----------------------------------
from datetime                        import datetime, date, time



# Application Specific Model Imports-----------------------

from aushadha_users.models            import AuShadhaUser
from clinic.models                   import Clinic, Staff
from visit.models                    import *
from patient.models                  import PatientDetail, PatientDemographicsData
from admission.models                import Admission
from physician.models                import PhysicianDetail
from inv_and_imaging.models          import LabInvestigationRegistry, ImagingInvestigationRegistry

#from complaints_and_history.models                  import *
#from phyexam.models                  import PhyExam, RegExam
#from detail_exam.models              import *

#TOTAL_COMPLAINTS_FORM = 1
#VisitComplaintsFormset = modelformset_factory(VisitComplaints, VisitComplaintsForm, extra  = TOTAL_COMPLAINTS_FORM +2, max_num = 10)

# views start here;;

@login_required
def visit_list(request):
  if request.user:
    user = request.user
    if request.method == "GET":
      visit_obj = VisitDetail.objects.all().order_by('visit_date')
      variable = RequestContext(request, {'user':user,
                  'visit_obj':visit_obj,
                  })
      return render_to_response('visit/visit_list.html',variable)
    else:
      raise Http404("Bad Request:: " + str(request.method) + " ")
  else:
    return HttpResponseRedirect('/AuShadha/login/')

@login_required
def visit_home(request,id = 'id'):
  pass

################################################################################
@login_required
def render_visit_tree(request,id = None):
  if request.method=="GET" and request.is_ajax():
    if id:
      patient_id = int(id)
    else:
      try:
        patient_id = int(request.GET.get('patient_id'))
        pat_obj = PatientDetail.objects.get(pk = patient_id)
      except(AttributeError, NameError, KeyError, TypeError,ValueError):
        raise Http404("ERROR! Bad Request Parameters")
      except(AttributeError, NameError, KeyError, TypeError,ValueError):
        raise Http404("ERROR! Requested Patient Data Does not exist")

      adm_obj               = Admission.objects.filter(patient_detail = pat_obj)
      visit_obj             = VisitDetail.objects.filter(patient_detail = pat_obj)

      demographics_obj      = PatientDemographicsData.objects.filter(patient_detail = pat_obj)
      social_history_obj    = PatientSocialHistory.objects.filter(patient_detail = pat_obj)
      family_history_obj    = PatientFamilylHistory.objects.filter(patient_detail = pat_obj)
      medical_history_obj   = PatientMedicalHistory.objects.filter(patient_detail = pat_obj)
      surgical_history_obj  = PatientSurgicalHistory.objects.filter(patient_detail = pat_obj)

      medication_list_obj   = PatientMedicationList.objects.filter(patient_detail = pat_obj)
      allergy_obj           = PatientAllergies.objects.filter(patient_detail = pat_obj)

      pat_inv_obj        = VisitInv.objects.filter(visit_detail__patient_detail = pat_obj)
      pat_imaging_obj    = VisitImaging.objects.filter(visit_detail__patient_detail = pat_obj)

      data = {
         "identifier": "id"   ,
         "label"     : "name" ,
         "items"     : [None,
												{"name"  : "Visits"    , "type":"application", "id":"VISITS",
													"len"   : len(visit_obj),
													"addUrl": pat_obj.get_patient_visit_add_url(),
													'children':[
																		{"name"  : "SOAP Notes" , "type":"application", "id":"SOAP_NOTES" ,
																		"len"   : 1,
																		"addUrl": None,
																		},

																		#{"name"  : "Diagnosis" , "type":"application", "id":"DIAG" ,
																		#"len"   : 1,
																		#"addUrl": None,
																		#},

																		{"name"  : "Advice" , "type":"application","id":"ADVICE" ,
																		"len"   : 1,
																		"addUrl": None,
																		},

																		{"name"  : "Procedure" , "type":"application", "id":"PROC" ,
																		"len"   : 1,
																		"addUrl": None,
																		},

																		#{"name"  : "Investigation" , "type":"application", "id":"INV" ,
																		#"len"   : 1,
																		#"addUrl": None,
																		#},
																		#{"name"  : "Imaging"      , "type":"application", "id":"IMAG" ,
																		#"len"   : 1,
																		#"addUrl": None,
																		#},

																		#{"name"  : "Calendar" , "type":"application", "id":"CAL" ,
																		#"len"   : 1,
																		#"addUrl": None,
																		#},

																		#{"name"  : "Media" , "type":"application", "id":"MEDIA" ,
																		#"len"   : 1,
																		#"addUrl": None,
																		#},

																		{"name"  : "Documents" , "type":"application", "id":"DOCS" ,
																		"len"   : 1,
																		"addUrl": None,
																		}
													]
												}
                    ],
      }

      if pat_obj.has_active_admission() =='0':
				data['items'][0] = {"name"  : "New OPD Visit" ,
				                    "type"  : "application"   ,
				                    "id"    : "NEW_OPD_VISIT" ,
													  "len"   : len(visit_obj)  ,
													  "addUrl": pat_obj.get_patient_visit_add_url()
                           }
      if visit_obj:
        data['items'][1]['children'] = []
        children_list  = data['items'][1]['children']
        sub_dict = {"name":"", "type":"visit", "id":"","editUrl":"","delUrl":""}
        for visit in visit_obj:
          dict_to_append = sub_dict.copy()
          dict_to_append['name']    = visit.visit_date.date().isoformat() + "("+ visit.op_surgeon.__unicode__() +")"
          dict_to_append['id']      = "VISIT_"+ unicode(visit.id)
          dict_to_append['absoluteUrl'] = visit.get_absolute_url()
          dict_to_append['editUrl']     = visit.get_edit_url()
          dict_to_append['editUrl']     = visit.get_edit_url()
          dict_to_append['delUrl']      = visit.get_del_url()
          children_list.append(dict_to_append)

      #if visit_obj:
        #data['items'][1]['children'] = []
        #children_list  = data['items'][1]['children']
        #for visit in visit_obj:
          #dict_to_append = {"name":"", "type":"visit", "id":"","editUrl":"","delUrl":""}
          #dict_to_append['name']    = visit.visit_date.date().isoformat() + "("+ visit.op_surgeon.__unicode__() +")"
          #dict_to_append['id']      = "VISIT_"+ unicode(visit.id)
          #dict_to_append['absoluteUrl'] = visit.get_absolute_url()
          #dict_to_append['editUrl']     = visit.get_edit_url()
          #dict_to_append['delUrl']      = visit.get_del_url()
          #children_list.append(dict_to_append)
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = "application/json")
  else:
     raise Http404("Bad Request")

@login_required
def render_visit_list(request):
    '''
    View for Generating Visit List
    Takes on Request Object as argument.
    '''
    user = request.user
    keys = ["sort( date_of_visit)", "sort(-date_of_visit)","sort(+date_of_visit)",
            "sort( op_surgeon)", "sort(-op_surgeon)", "sort(+op_surgeon)",
            ]
    key_sort_map = {
    "sort(+date_of_visit)": "visit_date",
    "sort( date_of_visit)": "visit_date",
    "sort(-date_of_visit)": "-visit_date",
    "sort(+op_surgeon)"       : "op_surgeon",
    "sort( op_surgeon)"       : "op_surgeon",
    "sort(-op_surgeon)"       : "-op_surgeon",
    }
    for key in request.GET:
      if key in keys:
        sort = key_sort_map[key]
        all_visits = VisitDetail.objects.all().order_by(sort)
      else:
        all_visits = VisitDetail.objects.all().order_by('visit_date')
    data         = []
    for visit in all_visits:
      data_to_append = {}
      data_to_append['id']         = visit.id
      data_to_append['date_of_visit']   = visit.visit_date.strftime("%d/%m/%Y %H:%M:%S")
      data_to_append['surgeon']   = visit.op_surgeon.__unicode__()
      data_to_append['patient_hospital_id']   = visit.patient_detail.patient_hospital_id
      data_to_append['patient']    = visit.patient_detail.__unicode__()
      data_to_append['age']        = visit.patient_detail.age
      data_to_append['sex']        = visit.patient_detail.sex
      data_to_append['active']     = visit.is_active
      #data_to_append['home']       = visit.get_visit_main_window_url()
      data_to_append['del']       = visit.get_visit_main_window_url()
      data_to_append['edit']       = visit.get_visit_main_window_url()
      data.append(data_to_append)
    json = simplejson.dumps(data)
    print json
    return HttpResponse(json, content_type = "application/json")

################################################################################

@login_required
def visit_detail_list(request, id):
  print "Listing Visit Detail for patient with ID: " + str(id)
  user = request.user
  if request.method == "GET" and request.is_ajax():
    try:
      id = int(id)
      patient_detail_obj = PatientDetail.objects.get(pk = id)
      visit_detail_obj   = VisitDetail.objects.filter(patient_detail = patient_detail_obj).order_by('visit_date')
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (PatientDetail.DoesNotExist):
      raise Http404("Requested Patient Does not exist.")
    visit_form_list = []
    if visit_detail_obj:
      error_message = None
      for visit in visit_detail_obj:
#        visit_list = []
        visit_form_list.append([VisitDetailForm(instance = visit), visit])
#        visit_form_list.append(visit_list)
    else:
      error_message = "No Visits Recorded"
    variable = RequestContext(request, {'user'               : user              ,
                                        'visit_detail_obj'   : visit_detail_obj  ,
                                        'visit_form_list'    : visit_form_list   ,
                                        'patient_detail_obj' : patient_detail_obj,
                                        'error_message'      : error_message
                                        })
    return render_to_response('visit/detail/list.html', variable)
  else:
    raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_detail_add(request, id):
  user = request.user
  if request.method == "GET" and request.is_ajax():
    try:
      id = int(id)
      patient_detail_obj  = PatientDetail.objects.get(pk = id)
      visit_detail_objs   = VisitDetail.objects.filter(patient_detail = patient_detail_obj).filter(is_active = True)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (PatientDetail.DoesNotExist):
      raise Http404("Requested Patient Does not exist.")
    error_message = None
    visit_detail_form = None
    visit_detail_obj      = None
    #if patient_detail_obj.has_active_visit():
      #error_message         = "There is an active visit. You cannot add visit.\nYou can however append a follow up visit"
    if patient_detail_obj.has_active_admission() != '0':
      error_message         = "There is an active Admission. You cannot add visit Now."
    else:
      visit_detail_obj = VisitDetail(patient_detail = patient_detail_obj)
      visit_detail_form = VisitDetailForm(instance = visit_detail_obj)
    variable = RequestContext(request, {'user'                  : user                  ,
                                        'visit_detail_obj'      : visit_detail_obj      ,
                                        'visit_detail_form'     : visit_detail_form ,
                                        'patient_detail_obj'    : patient_detail_obj    ,
                                        'error_message'         : error_message         ,
                                        })
    return render_to_response('visit/detail/add.html', variable)
  if request.method == "POST" and request.is_ajax():
    print "Received request to add visit..."
    try:
      id = int(id)
      patient_detail_obj  = PatientDetail.objects.get(pk = id)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (PatientDetail.DoesNotExist):
      raise Http404("Requested Patient Does not exist.")
    success       = False
    form_errors   = []
    error_message = None
#    if patient_detail_obj.has_active_visit():
#      error_message         = "There is an active visit. You cannot add visit.\nYou can however append a follow up visit"
    if patient_detail_obj.has_active_admission() != '0':
      error_message         = "There is an active Admission. You cannot add visit Now."
    else:
      visit_detail_obj = VisitDetail(patient_detail = patient_detail_obj)
      visit_detail_form = VisitDetailForm(request.POST, instance = visit_detail_obj)
      if visit_detail_form.is_valid():
        saved_visit   = visit_detail_form.save()
        success       = True
        error_message = "Visit Added Successfully"
        form_errors   = None
      else:
        success       = False
        error_message = "Error! Visit Could not be added"
        for error in visit_detail_form.errors:
          form_errors.append('<p>' + error +'<p>')
    data = { 'success'      : success      ,
             'error_message': error_message,
             'form_errors'  : form_errors
           }
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404(" Error ! Unsupported Request..")


@login_required
def visit_detail_edit(request, id):
  user = request.user
  if request.method == "GET" and request.is_ajax():
    try:
      id = int(id)
      visit_detail_obj = VisitDetail.objects.get(pk = id)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitDetail.DoesNotExist):
      raise Http404("Requested Patient Does not exist.")
    error_message = None
    visit_detail_edit_form = VisitDetailForm(instance = visit_detail_obj)
    variable = RequestContext(request, {'user'                  : user                  ,
                                        'visit_detail_obj'      : visit_detail_obj      ,
                                        'visit_detail_form'     : visit_detail_form ,
                                        'patient_detail_obj'    : patient_detail_obj    ,
                                        'error_message'         : error_message         ,
                                        })
    return render_to_response('visit/detail/edit.html', variable)
  if request.method == "POST" and request.is_ajax():
    try:
      id = int(id)
      visit_detail_obj = VisitDetail.objects.get(pk = id)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitDetail.DoesNotExist):
      raise Http404("Requested Visit Does not exist.")
    success                = False
    form_errors            = []
    error_message          = None
    visit_detail_edit_form = VisitDetailForm(request.POST, instance = visit_detail_obj)
    if visit_detail_edit_form.is_valid():
      saved_visit   = visit_detail_edit_form.save()
      saved_visit.visit_status_change(unicode(saved_visit.status))
      success       = True
      error_message = "Visit Edited Successfully"
      form_errors   = None
    else:
      success       = False
      error_message = "Error! Visit Could not be edited"
      for error in visit_detail_edit_form.errors:
        form_errors.append('<p>' + error +'<p>')
    data = { 'success'      : success      ,
             'error_message': error_message,
             'form_errors': form_errors
           }
    json = simplejson.dumps(data)
    return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404(" Error ! Unsupported Request..")

@login_required
def visit_detail_del(request, id):
  user = request.user
  if request.method == "GET" and request.is_ajax():
    try:
      id = int(id)
      visit_detail_obj = VisitDetail.objects.get(pk = id)
    except (TypeError, NameError, ValueError, AttributeError, KeyError):
      raise Http404("Error ! Invalid Request Parameters. ")
    except (VisitDetail.DoesNotExist):
      raise Http404("Requested Patient Does not exist.")
    error_message = None
    if user.is_superuser:
      visit_detail_obj.delete()
      success = True
      error_message = "Successfully Deleted Visit."
    else:
      success = False
      error_message = "Insufficient Permission. Could not delete."
    data = {'success': success, 'error_message': error_message}
    if request.GET.get('redirect'):
      return HttpResponseRedirect('visit/list/')
    else:
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
  else:
    raise Http404(" Error ! Unsupported Request..")


################################################################################

@login_required
def visit_status_list(request,id):
  user = request.user
  try:
   id = int(id)
   visit_obj = VisitDetail.objects.get(pk = id)
  except (NameError, ValueError, AttributeError, KeyError):
   raise Http404("Bad Request:: Invalid Request Parameters")
  except (VisitDetail.DoesNotExist):
   raise Http404("Bad Request:: Requested VisitDetail Does Not Exist")
  if request.method=="GET" and request.is_ajax():
    pass
  elif request.method=="POST" and request.is_ajax():
    pass
  else:
    raise Http404(" Error ! Unsupported Request..")

@login_required
def visit_status_edit(request, id):
  user = request.user
  try:
   id = int(id)
   visit_obj = VisitDetail.objects.get(pk = id)
  except (NameError, ValueError, AttributeError, KeyError):
   raise Http404("Bad Request:: Invalid Request Parameters")
  except (VisitDetail.DoesNotExist):
   raise Http404("Bad Request:: Requested VisitDetail Does Not Exist")
  if request.method=="GET" and request.is_ajax():
    pass
  elif request.method=="POST" and request.is_ajax():
    pass
  else:
    raise Http404(" Error ! Unsupported Request..")

################################################################################

@login_required
def visit_nature_list(request,id):
  user = request.user
  try:
   id = int(id)
   visit_obj = VisitDetail.objects.get(pk = id)
  except (NameError, ValueError, AttributeError, KeyError):
   raise Http404("Bad Request:: Invalid Request Parameters")
  except (VisitDetail.DoesNotExist):
   raise Http404("Bad Request:: Requested VisitDetail Does Not Exist")
  if request.method=="GET" and request.is_ajax():
    pass
  elif request.method=="POST" and request.is_ajax():
    pass
  else:
    raise Http404(" Error ! Unsupported Request..")

@login_required
def visit_nature_edit(request, id):
  user = request.user
  try:
   id        = int(id)
   visit_obj = VisitDetail.objects.get(pk = id)
  except (NameError, ValueError, AttributeError, KeyError):
   raise Http404("Bad Request:: Invalid Request Parameters")
  except (VisitDetail.DoesNotExist):
   raise Http404("Bad Request:: Requested VisitDetail Does Not Exist")
  if request.method=="GET" and request.is_ajax():
    pass
  elif request.method=="POST" and request.is_ajax():
    pass
  else:
    raise Http404(" Error ! Unsupported Request..")

################################################################################

@login_required
def visit_close(request, id):
  user = request.user
  if user.is_staff:
    try:
     id        = int(id)
     visit_obj = VisitDetail.objects.get(pk = id)
    except (NameError, ValueError, AttributeError, KeyError):
     raise Http404("Bad Request:: Invalid Request Parameters")
    except (VisitDetail.DoesNotExist):
     raise Http404("Bad Request:: Requested VisitDetail Does Not Exist")
    if request.method=="GET" and request.is_ajax():
      visit_obj.visit_status_change('discharged')
      success       = True
      error_message = "Visit Closed Successfully"
      data = {"success": success, 'error_message': error_message}
      json = simplejson.dumps(data)
      return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404(" Error ! Unsupported Request..")
  else:
    raise Http404(" Error ! Permission Denied..")

################################################################################





################################################################################


#@login_required
#def visit_action(request,action = 'add', id = 'id'):
#  if request.user:
#    user = request.user
#    if action == "add":
#      if request.method == "GET":
# try:
#   id = int(id)
#   pat_obj = PatientDetail.objects.get(pk = id)
# except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
#   raise Http404("Bad Request: Raised ValueError / TypeError / PatientDetail DoesNotExist")
# visit_objs    = VisitDetail.objects.filter(patient_detail = pat_obj)
# adm_obj       = Admission.objects.filter(patient_detail = pat_obj).filter(admission_closed = False)
# active_visits = []
# if visit_objs:
#   for visits in visit_objs:
#     active_visits = VisitStatus.objects.filter(visit_detail = visits).filter(is_active = True)
# if active_visits:
#   error_message = "Patient has an active Visit. You cannot add further visits for the same patient"
#   #variable     = RequestContext(request, {'user':user, 'error_message':error_message})
#   return HttpResponse(error_message)
# elif adm_obj:
#   error_message = "Patient has an active Admission. You cannot add OPD notes for the same patient"
#   return HttpResponse(error_message)
# else:
#   visit_detail_obj      = VisitDetail(patient_detail = pat_obj)
#   visit_status_obj      = VisitStatus(visit_detail = visit_detail_obj)
#   visit_complaint_obj   = VisitComplaints(visit_detail = visit_detail_obj)
#   visit_nature_obj      = VisitNature(visit_detail = visit_detail_obj)
#
#   visit_detail_form           = VisitDetailForm(instance = visit_detail_obj)
#   visit_nature_form           = VisitNatureForm(instance = visit_nature_obj)
#   visit_status_form           = VisitStatusForm(instance = visit_status_obj)
#   visit_complaint_form        = VisitComplaintsForm(instance = visit_complaint_obj)
#
#   action = '/visit/add/'+str(pat_obj.id) +'/'
#   method = 'post'
#   button = 'Add Visit'
#   variable = RequestContext(request, {'user':user,
#               'pat_obj':pat_obj,
#               'active':active_visits,
#               'visit_detail_obj':visit_detail_obj,
#               'visit_status_obj':visit_status_obj,
#               'visit_nature_obj':visit_nature_obj,
#               'visit_complaint_obj':visit_complaint_obj,
#
#               'visit_detail_form':visit_detail_form,
#               'visit_nature_form':visit_nature_form,
#               'visit_status_form':visit_status_form,
#               'visit_complaint_form':visit_complaint_form,
#
#               'action':action,
#               'method':method,
#               'button':button,
#               })
#   return render_to_response('visit/visit_actions.html', variable)
#
#      elif request.method == "POST":
# try:
#   id = int(id)
#   pat_obj = PatientDetail.objects.get(pk = id)
# except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
#   raise Http404("Bad Request: Raised ValueError / TypeError / PatientDetail DoesNotExist")
# adm_obj = Admission.objects.filter(patient_detail = pat_obj).filter(admission_closed = False)
# if adm_obj:
#   error_message = "Patient has an active Admission.\nYou cannot add OPD notes for the same patient"
#   return HttpResponseRedirect('/phy_exam/home/'+str(adm_obj.id)+'/')
# else:
#   visit_detail_obj    = VisitDetail(patient_detail = pat_obj)
#   visit_status_obj    = VisitStatus(visit_detail = visit_detail_obj)
#   #visit_complaint_obj    = VisitComplaints(visit_detail = visit_detail_obj)
#   visit_nature_obj    = VisitNature(visit_detail = visit_detail_obj)
#
#   visit_detail_form         = VisitDetailForm(request.POST, instance = visit_detail_obj)
#   visit_nature_form           = VisitNatureForm(request.POST,instance = visit_nature_obj)
#   visit_status_form           = VisitStatusForm(request.POST,instance = visit_status_obj)
#   #visit_complaint_form        = VisitComplaintsForm(request.POST,instance = visit_complaint_obj)
#
#   if visit_detail_form.is_valid()and visit_nature_form.is_valid()and visit_status_form.is_valid():
#      visit_detail_obj  = visit_detail_form.save()
#      visit_detail_obj.patient_detail = pat_obj
#      visit_detail_obj.save()
#
#      #visit_nature_form.cleaned_data['visit_detail'] = visit_detail_obj
#      visit_nature_obj.visit_detail = visit_detail_obj
#      visit_nature_obj = visit_nature_form.save()
#      visit_nature_obj.save()

#      #visit_status_form.cleaned_data['visit_detail'] = visit_detail_obj
#      visit_status_obj.visit_detail = visit_detail_obj
#      visit_status_obj = visit_status_form.save()

#      if visit_status_form.cleaned_data['status'] == 'admission' or visit_status_form.cleaned_data['status'] =='discharge':
#        visit_status_obj.is_active = 'False'
#      else:
#        visit_status_obj.is_active = 'True'
#      visit_status_obj.save()

#      error_message        = "Visit Details saved Successfully"
#      visit_complaints_formset = VisitComplaintsFormset(queryset = VisitComplaints.objects.filter(visit_detail = visit_detail_obj))
#      action               = 'visit/complaints/add/'+str(visit_detail_obj.id)+'/'
#      method               = 'post'
#      button               = 'Add Complaints'
#      variable             = RequestContext(request, {'user':user,
#            'visit_detail_obj':visit_detail_obj,
#            'visit_complaints_formset':visit_complaints_formset,
#            'method':method,
#            'action':action,
#            'button':button,
#            'error_message':error_message
#            })
#      return render_to_response('visit/visit_complaints.html', variable)
#      #return HttpResponseRedirect('/visit/list/')
#   else:
#     action   = '/visit/add/'+str(pat_obj.id) +'/'
#     method   = 'post'
#     button   = 'Resubmit'
#     variable = RequestContext(request, {'user':user,
#           'pat_obj':pat_obj,
#
#           'visit_detail_obj':visit_detail_obj,
#           'visit_status_obj':visit_status_obj,
#           'visit_nature_obj':visit_nature_obj,
#           #'visit_complaint_obj':visit_complaint_obj,
#
#           'visit_detail_form':visit_detail_form,
#           'visit_nature_form':visit_nature_form,
#           'visit_status_form':visit_status_form,
#           #'visit_complaint_formset':visit_complaint_formset,

#           'action':action,
#           'method':method,
#           'button':button,
#           })
#     return render_to_response('visit/visit_actions.html', variable)
#      else:
# return Http404("Bad Request")
#    elif action == 'edit':
#      pass
#    elif action == 'del':
#      pass
#    else:
#      raise Http404("Unknown Action:: " +str(action))
#  else:
#    return HttpResponseRedirect('/login/')

#@login_required
#def visit_complaints(request, id):
#  global TOTAL_COMPLAINTS_FORM
#  if request.user:
#    user = request.user
#    if request.method == 'POST':
#      try:
# id = int(id)
# visit_detail_obj = VisitDetail.objects.get(pk = id)
#      except (TypeError, ValueError, AttributeError, VisitDetail.DoesNotExist):
# raise Http404("Error !!:: Type / AttributeError / ValueError/ DoesNotExist Error ")
#      visit_complaints_obj  = VisitComplaints(visit_detail = visit_detail_obj)
#      visit_complaints_formset = VisitComplaintsFormset(request.POST)
#      if visit_complaints_formset.is_valid():
#        instances = visit_complaints_formset.save(commit = False)
#        for instance in instances:
#     instance.visit_detail = visit_detail_obj
#     instance.save()
#        if 'add_more_complaints' in request.POST:
#   TOTAL_COMPLAINTS_FORM  = int(request.POST['form-TOTAL_FORMS'])+1
#   visit_complaints_formset = VisitComplaintsFormset(queryset = VisitComplaints.objects.filter(visit_detail = visit_detail_obj))
#   action               = 'visit/complaints/add/'+str(visit_detail_obj.id)+'/'
#   method               = 'post'
#   button               = 'Add Complaints'
#   error_message = "Complaints have been saved.\nYou can add "+ str(10-TOTAL_COMPLAINTS_FORM) +" more complaints."
#   max_forms_reached = False
#   if TOTAL_COMPLAINTS_FORM == 10:
#         error_message = "Cannot add more complaints"
#         max_forms_reached = True
#   variable = RequestContext(request, {'user':user,
#                 'visit_detail_obj':visit_detail_obj,
#                 'visit_complaints_formset':visit_complaints_formset,
#                 'action':action,
#                 'button':button,
#                 'method':method,
#                 'error_message':error_message,
#                 'max_forms_reached':max_forms_reached,
#                 })
#   return render_to_response('visit/visit_complaints.html', variable)
# else:
#   return HttpResponseRedirect('/visit/list')
#      else:
# visit_action(request, action = 'add', id = id)

@login_required
def visit_home(request, id = id):
  if request.user:
    user = request.user
    try:
      id = int(id)
      visit_obj = VisitDetail.objects.get(pk = id)
    except(ValueError, AttributeError, TypeError, VisitDetail.DoesNotExist):
      raise Http404('Error!!:: AttributeError/ ValueError/ TypeError/ DoesNotExist')
    pat_detail_obj       = visit_obj.patient_detail
#    visit_status_obj     = VisitStatus.objects.filter(visit_detail = visit_obj)
#    visit_nature_obj     = VisitNature.objects.filter(visit_detail = visit_obj)
#    visit_complaints_obj = VisitComplaints.objects.filter(visit_detail = visit_obj)
    #phy_exam_obj      = PhyExam.objects.filter(visit_detail = visit_obj)
    #reg_exam_obj      = RegExam.objects.filter(visit_detail = visit_obj)
    if request.method == 'GET':
      variable = RequestContext(request, {'user':user,
            'pat_detail_obj':pat_detail_obj,
            'visit_obj':visit_obj,
#           'visit_status_obj':visit_status_obj,
#           'visit_nature_obj':visit_nature_obj,
#           'visit_complaints_obj':visit_complaints_obj,
            #'phy_exam_obj':phy_exam_obj,
            #'reg_exam_obj':reg_exam_obj,
            })
      return render_to_response('visit/visit_home.html', variable)
    elif request.method == 'POST':
      pass
    else:
      raise Http404("Bad Request.." + str(request.method))
  else:
    return HttpResponseRedirect('/login')




