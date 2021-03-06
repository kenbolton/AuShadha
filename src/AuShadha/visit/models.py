##################################
# Models for AuShadha OPD Visits.
# Copyright Dr. Easwar TR 25/12/2012
# LICENSE : GNU-GPL Version 3
##################################

#Django Specific Imports
from django.db import models
from django.forms import ModelForm, ModelChoiceField, Textarea, TextInput

#General Imports
from datetime import datetime, date, time

#Application model imports
from aushadha_base_models.models import AuShadhaBaseModel

from patient.models import PatientDetail
from clinic.models import Clinic, Staff
from admission.models import Admission
from inv_and_imaging.models import ImagingInvestigationRegistry, LabInvestigationRegistry

#from staff.models import Staff
#from nurse.models import NurseDetail



CONSULT_NATURE_CHOICES = (
                            ('initial','Intial'),
                            ('fu'     ,'Follow-Up'),
                            ('na'     ,'Non-Appointment'),
                            ('emer'   ,'Emergency'),
                            ('pre_op' ,'Pre-OP Counsel'),
                            ('post_op','Post-OP Review'),
                          )

CONSULT_STATUS_CHOICES =(
                        ('waiting'                 , 'Waiting'),
                        ('examining'               , 'Examining'),
                        ('review_awaited'          , 'Review Awaited'),
                        ('inv_awaited'             , 'Investigations Awaited'),
                        ('consults_awaited'        , 'Consults Awaited'),
                        ('admission'               , 'Admission'),
                        ('discharged'              , 'Discharged'),
                        ('no_show'                 , 'No Show'),
                      )

# Models start here..

class VisitDetail(AuShadhaBaseModel):

  __model_label__ = "detail"
  
  patient_detail   = models.ForeignKey('patient.PatientDetail')
  visit_date       = models.DateTimeField(auto_now = False, default = datetime.now())
  op_surgeon       = models.ForeignKey('clinic.Staff')
  referring_doctor = models.CharField(max_length = 30, default = "Self")
  consult_nature   = models.CharField(max_length = 30, choices = CONSULT_NATURE_CHOICES)
  status           = models.CharField(max_length = 30, choices = CONSULT_STATUS_CHOICES)
  is_active        = models.BooleanField(default = True, editable = False)
  remarks          = models.TextField(max_length = 200,
                                      default    = "NAD",
                                      help_text  = "limit to 200 words"
                                     )

  class Meta:
    verbose_name        = "Visit Details"
    verbose_name_plural = "Visit Details"

  def __unicode__(self):
    return '%s: %s: %s' %(self.patient_detail, self.visit_date.date().isoformat(),self.op_surgeon)

  def get_absolute_url(self):
    return '/AuShadha/visit/detail/%d/' %(self.id)

  def visit_nature(self):
    return unicode(self.consult_nature)

  def visit_nature_change(self, nature):
    try:
      self.consult_nature = unicode(nature)
    except (TypeError, NameError, ValueError):
      print "ERROR:: Invalid CONSULT_NATURE_CHOICE supplied.."
      return False
    if consult_nature in ['initial','fu', 'na','emer','pre_op','post_op']:
        self.save()
        return unicode(self.consult_nature)
    else:
      print "ERROR:: Invalid Consult Nature Change Requested.."
      return False

  def visit_status(self):
    return unicode(self.status)

  def visit_status_change(self, status):
    try:
      self.status = unicode(status)
    except (TypeError, NameError, ValueError):
      print "ERROR:: Invalid CONSULT_STATUS_CHOICE supplied.."
      return False
    if status in ['discharged','admission','review_awaited','inv_awaited','consults_awaited']:
      if self.status == 'discharged' or \
         self.status == 'admission':
         self._close_visit()
      else:
        self.is_active = True
        self.save()
      return unicode(self.status)
    else:
      print "ERROR:: Invalid Consult Status Change Requested.."
      return False

  def _close_visit(self):
    self.is_active = False
    self.save()

  def save(self, *args, **kwargs):
    self.__model_label__ = 'detail'
    #if self.op_surgeon.clinic_staff_role == 'doctor':
    if not self.status == 'no_show' or self.status == 'discharged' or self.status == 'admission':
      self.is_active = False
    else:
      self.is_active = True
    super(VisitDetail, self).save(*args, **kwargs)
    #else:
      #raise Exception("User is not a Provider. Only Doctors can save Visits. ")



class VisitComplaint(AuShadhaBaseModel):
  __model_label__ = "complaint"

  complaint     = models.CharField(max_length = 30, help_text= 'limit to 30 words')
  duration      = models.CharField(max_length = 30, help_text= 'limit to 30 words')
  visit_detail  = models.ForeignKey(VisitDetail)
  created_at    = models.DateTimeField(auto_now_add = True, editable = False)

  def __unicode__(self):
    return '%s : %s' %(self.complaint, self.duration)

  def save(self, *args, **kwargs):
    self.__model_label__ = 'complaint'
    super(VisitComplaint, self).save(*args, **kwargs)

  #def get_edit_url(self):
    #return '/AuShadha/visit/complaint/edit/%s/' %(self.id)

  #def get_del_url(self):
    #return '/AuShadha/visit/complaint/del/%s/' %(self.id)

  class Meta:
    verbose_name        = "Presenting Complaint"
    verbose_name_plural = "Presenting Complaint"
    ordering    = ('visit_detail', 'created_at', 'complaint')


class VisitHPI(AuShadhaBaseModel):
  __model_label__ = "hpi"

  hpi           = models.TextField('History of Presenting Illness', max_length = 1000, help_text = 'limit to 1000 words')
  visit_detail  = models.ForeignKey(VisitDetail)
  created_at    = models.DateTimeField(auto_now_add = True, editable = False)

  def __unicode__(self):
    return '%s' %(self.hpi)

  def save(self, *args, **kwargs):
    self.__model_label__ = 'hpi'
    super(VisitHPI, self).save(*args, **kwargs)

  #def get_edit_url(self):
    #return '/AuShadha/visit/hpi/edit/%s/' %(self.id)

  #def get_del_url(self):
    #return '/AuShadha/visit/hpi/del/%s/' %(self.id)

  class Meta:
    unique_together   = ('hpi', 'visit_detail')
    verbose_name    = "History of Presenting Illness"
    verbose_name_plural = "History of Presenting Illness"
    ordering    = ('visit_detail', 'created_at', 'hpi')


class VisitPastHistory(AuShadhaBaseModel):

  __model_label__ = "past_history"

  past_history     = models.TextField('Past History ', max_length = 1000, help_text = 'limit to 1000 words')
  visit_detail   = models.ForeignKey(VisitDetail)
  created_at     = models.DateTimeField(auto_now_add = True, editable = False)

  def __unicode__(self):
    return '%s' %(self.past_history)

  def save(self, *args, **kwargs):
    self.__model_label__ = 'past_history'
    super(VisitPastHistory, self).save(*args, **kwargs)

  #def get_edit_url(self):
    #return '/AuShadha/visit/past_history/edit/%s/' %(self.id)

  #def get_del_url(self):
    #return '/AuShadha/visit/past_history/del/%s/' %(self.id)

  class Meta:
    unique_together   = ('past_history', 'visit_detail')
    verbose_name    = "Past History"
    verbose_name_plural     = "Past History"
    ordering    = ('visit_detail', 'created_at', 'past_history')


class VisitImaging(AuShadhaBaseModel):

  __model_label__ = "imaging"

  modality   = models.ForeignKey('inv_and_imaging.ImagingInvestigationRegistry')
  finding    = models.TextField('Finding', max_length = 1000, help_text = 'limit to 1000 words')
  visit_detail = models.ForeignKey(VisitDetail)
  created_at   = models.DateTimeField(auto_now_add = True, editable = True)

  def __unicode__(self):
    return '''%s: %s \n(%s)''' %(self.modality, self.finding, self.created_at.date().isoformat() )

  def __trimmed_unicode__(self):
    return '''%s: %s ... \n(%s)''' %(self.modality, self.finding[0:5], self.created_at.date().isoformat() )

  def save(self, *args, **kwargs):
    self.__model_label__ = 'imaging'
    super(VisitImaging, self).save(*args, **kwargs)

  #def get_add_url(self):
    #return '/AuShadha/visit/imaging/add/%s/' %(self.id)

  #def get_edit_url(self):
    #return '/AuShadha/visit/imaging/edit/%s/' %(self.id)

  #def get_del_url(self):
    #return '/AuShadha/visit/imaging/del/%s/' %(self.id)

  class Meta:
    verbose_name    = "Imaging Studies"
    verbose_name_plural     = "Imaging Studies"
    ordering    = ('visit_detail', 'created_at', 'modality')



class VisitInv(AuShadhaBaseModel):

  __model_label__ = "inv"

  investigation   = models.ForeignKey('inv_and_imaging.LabInvestigationRegistry')
  value       = models.CharField('Findings', max_length = 30)
  visit_detail  = models.ForeignKey(VisitDetail)
  created_at    = models.DateTimeField(auto_now_add = True, editable = True)

  def __unicode__(self):
    return "%s: %s \n(%s)" %(self.investigation, self.value, self.created_at.date().isoformat())

  #def get_edit_url(self):
    #return '/AuShadha/visit/inv/edit/%s/' %(self.id)

  #def get_del_url(self):
    #return '/AuShadha/visit/inv/del/%s/' %(self.id)

  def save(self, *args, **kwargs):
    self.__model_label__ = 'inv'
    super(VisitInv, self).save(*args, **kwargs)

  class Meta:
    verbose_name         = "Lab Investigation"
    verbose_name_plural    = "Lab Investigation"
    ordering         = ('visit_detail', 'created_at', 'investigation')










## ModelForm start here..

class VisitDetailForm(ModelForm):
  op_surgeon = ModelChoiceField(queryset = Staff.objects.filter(clinic_staff_role ='doctor'))

  class Meta:
    model   = VisitDetail
    exclude = ('patient_detail','parent_clinic')

  def __init__(self, *args, **kwargs):
      super(VisitDetailForm, self).__init__(*args, **kwargs)
      text_fields = [{"field"         : 'visit_date',
                      'max_length'    :  100         ,
                      "data-dojo-type": "dijit.form.DateTextBox",
                      "data-dojo-props": r"'required' :true"
                      },
                    {"field"            : 'op_surgeon',
                      'max_length'      :  100         ,
                    "data-dojo-type"    : "dijit.form.Select",
                      "data-dojo-props" : r"'required' : true"
                    },
                      {"field"         : 'referring_doctor',
                      'max_length'    :  100         ,
                      "data-dojo-type": "dijit.form.ValidationTextBox",
                      "data-dojo-props": r"'required' :false"
                      },
                    {"field"          : 'consult_nature',
                      'max_length'    :  100         ,
                      "data-dojo-type": "dijit.form.Select",
                      "data-dojo-props": r"'required' :true"
                      },
                    {"field"          : 'status',
                      'max_length'    :  100         ,
                      "data-dojo-type": "dijit.form.Select",
                      "data-dojo-props": r"'required' :true"
                      },
                    {"field"         : 'remarks',
                      'max_length'    :  150         ,
                      "data-dojo-type": "dijit.form.Textarea",
                      "data-dojo-props": r"'required' :false,placeHolder:'Other Notes...'"
                      }
            ]
      for field in text_fields:
        print(self.fields[field['field']].widget);
        self.fields[field['field']].widget.attrs['data-dojo-type'] = field['data-dojo-type']
        self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
        self.fields[field['field']].widget.attrs['max_length'] = field['max_length']


class VisitComplaintForm(ModelForm):

  class Meta:
    model = VisitComplaint
    exclude = ('parent_clinic','visit_detail')

  def __init__(self, *args, **kwargs):
    super(VisitComplaintForm, self).__init__(*args, **kwargs)
    text_fields = [

                  {"field"           : 'complaint',
                    'max_length'     :  '100'         ,
                    "data-dojo-type" : "dijit.form.ValidationTextBox",
                    "data-dojo-id"   : "visit_complaint_complaint",
                    "data-dojo-props": r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
                    },
                    {"field"         : 'duration',
                    'max_length'     :  '100'         ,
                    "data-dojo-type" : "dijit.form.FilteringSelect",
                    "data-dojo-id"   : "visit_complaint_duration",
                    "data-dojo-props": r" name: 'duration',searchAttr:'id',store:complaintDurationsStore,required:'true', autoComplete:'false'"
                    },
    ]

    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['data-dojo-id'] = field['data-dojo-id']
      self.fields[field['field']].widget.attrs['max_length']      = field['max_length']

class VisitHPIForm(ModelForm):

  class Meta:
    model = VisitHPI
    exclude = ('visit_detail','parent_clinic')

  def __init__(self, *args, **kwargs):
    super(VisitHPIForm, self).__init__(*args, **kwargs)
    text_fields = [
                    {"field"          : 'hpi',
                    'max_length'      : '1000'         ,
                    "data-dojo-type"  : "dijit.form.SimpleTextarea",
                    "data-dojo-id"    : "visit_hpi",
                    "data-dojo-props" : r"'required' : 'true' ,'regExp':'[a-zA-Z /-_:0-9#]+','invalidMessage' : 'Invalid Character'"
                    },
    ]

    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['data-dojo-id'] = field['data-dojo-id']
      self.fields[field['field']].widget.attrs['max_length']      = field['max_length']

class VisitPastHistoryForm(ModelForm):

  class Meta:
    model = VisitPastHistory
    exclude = ('parent_clinic','visit_detail')

  def __init__(self, *args, **kwargs):
    super(VisitPastHistoryForm, self).__init__(*args, **kwargs)
    text_fields = [
                    {"field"          : 'past_history',
                    'max_length'      :  '1000'         ,
                    "data-dojo-type"  : "dijit.form.SimpleTextarea",
                    "data-dojo-id"    : "visit_past_history",
                    "data-dojo-props" : r"'required' : 'true' ,'regExp':'[a-zA-Z /-_:0-9#]+','invalidMessage' : 'Invalid Character'"
                    },
        ]

    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['data-dojo-id']    = field['data-dojo-id']
      self.fields[field['field']].widget.attrs['max_length']      = field['max_length']


class VisitImagingForm(ModelForm):
  class Meta:
    model = VisitImaging
    exclude = ('parent_clinic','visit_detail')

  def __init__(self, *args, **kwargs):
    super(VisitImagingForm, self).__init__(*args, **kwargs)
    text_fields = [
                    {"field"          : 'modality',
                    'max_length'      :  '100'         ,
                    "data-dojo-type"  : "dijit.form.Select",
                    "data-dojo-id"    : "visit_imaging_imaging",
                    "data-dojo-props" : r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
                    },
                    {"field"          : 'finding',
                    'max_length'      :  '1000'         ,
                    "data-dojo-type"  : "dijit.form.SimpleTextarea",
                    "data-dojo-id"    : "visit_imaging_finding",
                    "data-dojo-props" : r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
                    },

                  ]

    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['data-dojo-id'] = field['data-dojo-id']
      self.fields[field['field']].widget.attrs['max_length']      = field['max_length']




class VisitInvForm(ModelForm):
  class Meta:
    model = VisitInv
    exclude = ('visit_detail','parent_clinic')
  def __init__(self, *args, **kwargs):
    super(VisitInvForm, self).__init__(*args, **kwargs)
    text_fields = [{"field"           : 'investigation',
                    'max_length'      :  '100'         ,
                    "data-dojo-type"  : "dijit.form.Select",
                    "data-dojo-id"    : "visit_investigation_investigation",
                    "data-dojo-props" : r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
                    },
                    {"field"          : 'value',
                    'max_length'      :  '100'         ,
                    "data-dojo-type"  : "dijit.form.ValidationTextBox",
                    "data-dojo-id"    : "visit_investigation_value",
                    "data-dojo-props" : r"'required' : 'true' ,'regExp':'[a-zA-Z /-:0-9#]+','invalidMessage' : 'Invalid Character'"
                    },

                  ]

    for field in text_fields:
      print(self.fields[field['field']].widget);
      self.fields[field['field']].widget.attrs['data-dojo-type']  = field['data-dojo-type']
      self.fields[field['field']].widget.attrs['data-dojo-props'] = field['data-dojo-props']
      self.fields[field['field']].widget.attrs['data-dojo-id'] = field['data-dojo-id']
      self.fields[field['field']].widget.attrs['max_length']      = field['max_length']
