##--------------------------------------------------------------
# Views for Patient contact and details display and modification.
# Author: Dr.Easwar T.R , All Rights reserved with Dr.Easwar T.R.
# Date: 26-09-2010
##---------------------------------------------------------------

#import wx
import os, sys

# General Django Imports----------------------------------

from django.shortcuts                import render_to_response
from django.http                     import Http404, HttpResponse, HttpResponseRedirect
from django.template                 import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth.models      import User


from django.views.decorators.csrf   import csrf_exempt
from django.views.decorators.cache  import never_cache
from django.views.decorators.csrf   import csrf_protect
from django.views.decorators.debug  import sensitive_post_parameters

from django.core.paginator           import Paginator

from django.utils                    import simplejson
from django.core                     import serializers
from django.core.serializers         import json    
from django.core.serializers.json    import DjangoJSONEncoder

from django.contrib.auth.views       import login, logout
from django.contrib.auth.decorators  import login_required
from django.contrib.auth             import REDIRECT_FIELD_NAME
from django.contrib.auth.forms       import AuthenticationForm
from django.template.response        import TemplateResponse
from django.contrib.sites.models     import get_current_site
import urlparse

# General Module imports-----------------------------------
from datetime import datetime, date, time



# Application Specific Model Imports-----------------------
from patient.models   import *
from admission.models import *
#from discharge.models import *
#from visit.models     import *

import AuShadha.settings as settings

#Views start here -----------------------------------------

from patient.views import *

################################################################################

@login_required
def patient_family_history_add(request,id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_family_history_obj       = PatientFamilyHistory(patient_detail = patient_detail_obj)
        patient_family_history_add_form  = PatientFamilyHistoryForm(instance = patient_family_history_obj)
        variable                = RequestContext(request, 
        																					{"user" 									:	user,
        																					 "patient_detail_obj"			:	patient_detail_obj ,
        																					 "patient_family_history_add_form" :	patient_family_history_add_form, 
																									 "patient_family_history_obj" 		  :	patient_family_history_obj ,
																									})
#      except TypeError or ValueError or AttributeError:
#        raise Http404("BadRequest")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
      return render_to_response('patient/family_history/add.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                      = int(id)
        patient_detail_obj      = PatientDetail.objects.get(pk =id)
        patient_family_history_obj       = PatientFamilyHistory(patient_detail = patient_detail_obj)
        patient_family_history_add_form  = PatientFamilyHistoryForm(request.POST,instance = patient_family_history_obj)
        if patient_family_history_add_form.is_valid():
          family_history_obj          = patient_family_history_add_form.save()
          success        = True
          error_message  = "FamilyHistory Data Added Successfully"
          addData        = {
                            "id"                : family_history_obj.id,
                            "family_member"     : family_history_obj.family_member,
                            "age"     : family_history_obj.age,
                            "deceased"          : family_history_obj.deceased,
                            "age_at_onset"      : family_history_obj.age_at_onset,
                            "disease"           : family_history_obj.disease,
                            "edit"              : family_history_obj.get_edit_url(),
                            "del"               : family_history_obj.get_del_url()
          }
          data           = {'success'      : success, 
                            'error_message': error_message,
                            "form_errors"  : None,
                            "addData"      : addData
          }
          json           = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success       = False
          error_message = "Error Occured. FamilyHistory data could not be added."
          form_errors   = ''
          for error in patient_family_history_add_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = { 'success'      : success, 
                   'error_message': error_message,
                   'form_errors'  : form_errors
                 }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))
  else:
    raise Http404("You need to Login")

@login_required
def patient_family_history_edit(request,id):
  if request.user:
    user = request.user
    if request.method =="GET" and request.is_ajax():
      try:
        id                            = int(id)
        patient_family_history_obj         = PatientFamilyHistory.objects.get(pk = id)
        patient_family_history_edit_form   = PatientFamilyHistoryForm(instance = patient_family_history_obj)
        variable                      = RequestContext(request, 
        																					{"user" 									      :	user,
        																					 "patient_detail_obj"			      :	patient_family_history_obj.patient_detail ,
        																					 "patient_family_history_edit_form"  :	patient_family_history_edit_form, 
																									 "patient_family_history_obj" 		    :	patient_family_history_obj ,
																									})
      except TypeError or ValueError or AttributeError:
        raise Http404("BadRequest")
      except PatientFamilyHistory.DoesNotExist:
        raise Http404("BadRequest: Patient Data Does Not Exist")
      return render_to_response('patient/family_history/edit.html',variable)
    elif request.method == 'POST' and request.is_ajax():
      try:
        id                            = int(id)
        patient_family_history_obj         = PatientFamilyHistory.objects.get(pk = id)
        patient_family_history_edit_form   = PatientFamilyHistoryForm(request.POST,instance = patient_family_history_obj)
        if patient_family_history_edit_form.is_valid():
          family_history_obj           = patient_family_history_edit_form.save()
          success                 = True
          error_message           = "FamilyHistory Data Edited Successfully"
          addData        = {
                            "id"                : family_history_obj.id,
                            "family_member"     : family_history_obj.family_member,
                            "age"     : family_history_obj.age,
                            "deceased"          : family_history_obj.deceased,
                            "age_at_onset"      : family_history_obj.age_at_onset,
                            "disease"           : family_history_obj.disease,
                            "edit"              : family_history_obj.get_edit_url(),
                            "del"               : family_history_obj.get_del_url()
          }
          data                    = {
                                    'success'      : success, 
                                    'error_message': error_message,
                                    "form_errors"  : None,
                                    "addData"      : addData
                                    }
          json           = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
        else:
          success       = False
          error_message = "Error Occured. FamilyHistory data could not be added."
          form_errors   = ''
          for error in patient_family_history_edit_form.errors:
            form_errors += '<p>' + error +'</p>'
          data = { 'success'      : success, 
                   'error_message': error_message,
                   'form_errors'  : form_errors
                 }
          json = simplejson.dumps(data)
          return HttpResponse(json, content_type = 'application/json')
      except ValueError or AttributeError or TypeError:
        raise Http404("BadRequest: Server Error")
      except PatientDetail.DoesNotExist:
        raise Http404("BadRequest: Requested Patient DoesNotExist")
    else:
      raise Http404("BadRequest: Unsupported Request Method. AJAX status is:: " + unicode(request.is_ajax()))
  else:
    raise Http404("You need to Login")

@login_required
def patient_family_history_del(request,id):
  user = request.user
  if request.user and user.is_superuser:
    if request.method =="GET":
       try:
          id                      = int(id)
          patient_family_history_obj   = PatientFamilyHistory.objects.get(pk = id)
          patient_detail_obj      = patient_family_history_obj.patient_detail
       except TypeError or ValueError or AttributeError:
          raise Http404("BadRequest")
       except PatientFamilyHistory.DoesNotExist:
          raise Http404("BadRequest: Patient family_history Data Does Not Exist")
       patient_family_history_obj.delete()
       success        = True
       error_message  = "family_history Data Deleted Successfully"
       data           = {'success': success, 'error_message': error_message}
       json           = simplejson.dumps(data)
       return HttpResponse(json, content_type = 'application/json')
    else:
      raise Http404("BadRequest: Unsupported Request Method")
  else:
    raise Http404("Server Error: No Permission to delete.")

