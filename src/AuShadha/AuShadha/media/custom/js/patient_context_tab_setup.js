function patientContextTabSetup(){
require(
  ["dijit/registry",
   "dojo/parser",
   "dijit/layout/BorderContainer",
   "dijit/layout/TabContainer",
   "dojox/layout/ContentPane",
   "dijit/form/Button",
   "dojo/dom",
   "dojo/dom-construct",
   "dojo/dom-style",
   "dojo/ready",
   "dojo/_base/array"
  ],
  function(registry,parser, BorderContainer,
           TabContainer, ContentPane, Button,
           dom, domConstruct, domStyle, ready,array
  ){
ready( function(){
      console.log("Starting script patient_context_tab_setup");
      if (registry.byId("patientContextContainer")){
        return; 
      }
      else
      {

      domConstruct.destroy('frontPageSearchPatientAuShadhaLogo');
      domStyle.set(dom.byId('searchPatientContainerDiv'),{top           : "0px",
                                                          left          : "0px",
                                                          height        : "50px", 
                                                          width         : "auto",
                                                          background    : "none",
                                                          border        : "none",
                                                          'boxShadow'   : "none",
                                                          "borderRadius": "none",
                                                          'fontSize'    : "inherit",
                                                          "padding"     : "0px 0px 10px 0px;",
                                                            overflow:'hidden',
                                                          "margin"      : "0px 0px 10px 0px;"
                                                        });
      domStyle.set(dom.byId('searchTitle'),{top:"0px",left:"0px"});
      registry.byId('addPatientButton').set('iconClass',"addPatientIcon_16");
      domStyle.set(dom.byId('simplePatientFilteringSearch'),{top:"0px",
                                                            left:"0px",
                                                            overflow:'hidden',
                                                            height        : "50px", 
                                                            width         : "auto",
                                                            background    : "none",
                                                            border        : "none",
                                                            'boxShadow'   : "none",
                                                            "borderRadius": "none",
                                                            'fontSize'    : "inherit",
                                                            "padding"     : "0px 0px 10px 0px;",
                                                            "margin"      : "0px 0px 10px 0px;"
                                                            });

      registry.byId('addPatientButton').set("style", {"fontSize": "12px"} );
      registry.byId('filteringSelectPatSearch').set("style",{width: "400px", left: "5%", "fontSize":"12px"} );


      domConstruct.create('div',
                          {id: "patientContextTabs"}, 
                          "patientContextContainer", 
                          "first"
      );
      domConstruct.create('div', 
                          {id: "patientContactTab"}, 
                         "patientContextTabs", 
                         "first"
      );
        domConstruct.create('div', 
                            {id: "contact_list"}, 
                            "patientContactTab", 
                            "first"
        );
        domConstruct.create('div', 
                            {id: "phone_list"}, 
                            "patientContactTab", 
                            "last"
        );

      domConstruct.create('div', 
                          {id: "patientHistoryTab"}, 
                          "patientContextTabs", 
                          "last"
      );

        domConstruct.create('div', 
                            {id: "patientHistoryTabs"}, 
                            "patientHistoryTab", 
                            "first"
        );
          domConstruct.create('div', 
                              {id: "patientDemographicsTab"}, 
                              "patientHistoryTabs", 
                              "first"
          );
            domConstruct.create('div', 
                                {id: "demographics_add_or_edit_form"}, 
                                "patientDemographicsTab", 
                                "first"
            );
            domConstruct.create('div', 
                                {id: "guardian_list"}, 
                                "patientDemographicsTab",
                                "last"
            );
          domConstruct.create('div', 
                              {id: "patientSocialHistoryTab"}, 
                              "patientHistoryTabs", 
                              "first"
          );
          domConstruct.create('div', 
                              {id: "patientFamilyHistoryTab"}, 
                              "patientHistoryTabs", 
                              "last"
          );
            domConstruct.create('div', 
                                {id: "family_history_list"}, 
                                "patientFamilyHistoryTab", 
                                "first"
            );
          domConstruct.create('div', 
                              {id: "patientMedicalAndSurgicalHistoryTab"}, 
                              "patientHistoryTabs", 
                              "last"
          );
/*
            domConstruct.create('div', 
                                {id: "medical_and_surgical_history_list"}, 
                                "patientMedicalAndSurgicalHistoryTab", 
                                "first"
            );
*/
            domConstruct.create('div',
                                {id: "medical_history_list"},
                                "patientMedicalAndSurgicalHistoryTab",
                                "first"
            );
            domConstruct.create('div',
                                {id: "surgical_history_list"},
                                "patientMedicalAndSurgicalHistoryTab",
                                "last"
             );

    domConstruct.create('div',
                          {id: "patientPreventiveHealthTab"}, 
                          "patientContextTabs", 
                          "last"
      );
        domConstruct.create('div', 
                            {id: "patientPreventiveTabs"}, 
                            "patientPreventiveHealthTab", 
                            "first"
        );
          domConstruct.create('div', 
                              {id: "patientNeonatalAndPaediatricExamTab"}, 
                              "patientPreventiveTabs", 
                              "first"
          );
            domConstruct.create('div', 
                                {id: "neonatal_and_paediatric_exam_list"}, 
                                "patientNeonatalAndPaediatricExamTab", 
                                "first"
            );
          domConstruct.create('div', 
                              {id: "patientImmunisationTab"}, 
                              "patientPreventiveTabs", 
                              "last"
          );
            domConstruct.create('div', 
                                {id: "immunisation_list"}, 
                                "patientImmunisationTab", 
                                "first"
            );
          domConstruct.create('div', 
                              {id: "patientObstetricsPreventivesTab"}, 
                              "patientPreventiveTabs", 
                              "last"
          );

            domConstruct.create('div', 
                                {id: "obstetric_history_detail"}, 
                                "patientObstetricsPreventivesTab", 
                                "first"
            );
/*
            domConstruct.create('div', 
                                {id: "obstetric_history_form"}, 
                                "obstetrics_history_detail", 
                                "after"
            );
*/

          domConstruct.create('div', 
                              {id: "patientGynaecologyPreventivesTab"}, 
                              "patientPreventiveTabs", 
                              "last"
          );
            domConstruct.create('div', 
                                {id: "gynaecology_preventives_list"}, 
                                "patientGynaecologyPreventivesTab", 
                                "first"
            );
          domConstruct.create('div', 
                              {id: "patientMedicalPreventivesTab"}, 
                              "patientPreventiveTabs", 
                              "last"
          );
            domConstruct.create('div', 
                                {id: "medical_preventives_list"}, 
                                "patientMedicalPreventivesTab", 
                                "first"
            );

      domConstruct.create('div', 
                          {id: "patientMedicationListAndAllergiesTab"}, 
                          "patientContextTabs", 
                          "last"
      );
          domConstruct.create('div', 
                              {id: "medication_list"}, 
                              "patientMedicationListAndAllergiesTab", 
                              "first"
          );
          domConstruct.create('div', 
                              {id: "allergy_list"}, 
                              "medication_list", 
                              "after"
          );

      domConstruct.create('div', 
                          {id: "patientAdmissionAndVisitsTab"}, 
                          "patientContextTabs", 
                          "last"
      );
          domConstruct.create('div', 
                              {id: "admission_list"}, 
                              "patientAdmissionAndVisitsTab", 
                              "first"
          );
          domConstruct.create('div', 
                              {id: "visit_list"}, 
                              "admission_list", 
                              "after"
          );

      domConstruct.create('div', 
                          {id: "patientMediaTab"}, 
                          "patientContextTabs", 
                          "last"
      );
          domConstruct.create('div', 
                              {id: "patient_media_list"}, 
                              "patientMediaTab", "first"
          );


      var mainContainer = new ContentPane({id : "patientContextContainer",
                                          region  : "bottom",
                                          style :"min-height: 550px; overflow:auto;"
                                          },
                                          "patientContextContainer"
      );

      var tabs = new TabContainer({ id: "patientContextTabs",
                                    tabPosition:"top",
                                    tabStrip:true,
                                    style : "min-height: 550px;overflow:auto;"
                                   },
                                   "patientContextTabs"
      );

      mainContainer.addChild(tabs);

      var contactTab = new ContentPane({id:"patientContactTab",
                                         title:"Contact"
                                        },
                                        "patientContactTab"
      );
      tabs.addChild(contactTab);
      var historyTab = new ContentPane({id:"patientHistoryTab",
                                         title:"History"
                                        },
                                        "patientHistoryTab"
      );
      tabs.addChild(historyTab);
        var historyTabs = new TabContainer({id:"patientHistoryTabs",
                                            tabPosition:"top",
                                            tabStrip:true,
                                            style : "min-height: 550px;overflow:auto;"        
                                          },
                                          "patientHistoryTabs"
        );
        historyTab.addChild(historyTabs);
          var demographicsTab = new ContentPane({id:"patientDemographicsTab",
                                             title:"Demographics"
                                            },
                                            "patientDemographicsTab"
          );
          historyTabs.addChild(demographicsTab);
            var demographicsAddOrEditForm = new ContentPane({id:"demographics_add_or_edit_form"
                                              },
                                              "demographics_add_or_edit_form"
            );
            demographicsTab.addChild(demographicsAddOrEditForm);
          var socialHistoryTab = new ContentPane({id:"patientSocialHistoryTab",
                                             title:"Social"
                                            },
                                            "patientSocialHistoryTab"
          );
          historyTabs.addChild(socialHistoryTab);
          var familyHistoryTab = new ContentPane({id:"patientFamilyHistoryTab",
                                             title:"Family"
                                            },
                                            "patientFamilyHistoryTab"
          );
          historyTabs.addChild(familyHistoryTab);
          var medicalAndSurgicalHistoryTab = new ContentPane({id:"patientMedicalAndSurgicalHistoryTab",
                                             title:"Medical & Surgical"
                                            },
                                            "patientMedicalAndSurgicalHistoryTab"
          );
          historyTabs.addChild(medicalAndSurgicalHistoryTab);
/*
            var medicalHistoryTab = new ContentPane({id:"medical_history_list"
                                                    },
                                                    "medical_history_list"
                                                    );
            medicalAndSurgicalHistoryTab.addChild(medicalHistoryTab);

            var surgicalHistoryTab = new ContentPane({id:"surgical_history_list"
                                                    },
                                                    "surgical_history_list"
                                                    );
            medicalAndSurgicalHistoryTab.addChild(surgicalHistoryTab);
*/

      var preventiveHealthTab = new ContentPane({id:"patientPreventiveHealthTab",
                                                 title:"Preventive Health"
                                                },
                                                "patientPreventiveHealthTab"
      );
      tabs.addChild(preventiveHealthTab);
        var preventiveHealthTabs = new TabContainer({id:"patientPreventivesTabs",
                                                      tabPosition:"top",
                                                      tabStrip:true,
                                                      style : "min-height: 550px;overflow:auto;"
                                                  },
                                                  "patientPreventiveTabs"
        );
        preventiveHealthTab.addChild(preventiveHealthTabs);
          var patientNeonatalAndPaediatricTab = new ContentPane({id:"patientNeonatalAndPaediatricExamTab",
                                                       title:"Neonatal & Paediatric",
                                                       disabled: true
                                                      },
                                                      "patientNeonatalAndPaediatricExamTab"
                                                      );
          preventiveHealthTabs.addChild(patientNeonatalAndPaediatricTab);
          var patientImmunisationTab = new ContentPane({id:"patientImmunisationTab",
                                                     title:"Immunisation"
                                                    },
                                                    "patientImmunisationTab"
                                                    );
          preventiveHealthTabs.addChild(patientImmunisationTab);

          var patientObstetricsPreventivesTab = new ContentPane({id:"patientObstetricsPreventivesTab",
                                                       title:"Obstetrics"
                                                      },
                                                      "patientObstetricsPreventivesTab"
                                                      );
          preventiveHealthTabs.addChild(patientObstetricsPreventivesTab);


            var patientObstetricsHistoryDetail = new ContentPane({id:"obstetric_history_detail",
                                                        },
                                                        "obstetric_history_detail"
                                                        );
            patientObstetricsPreventivesTab.addChild(patientObstetricsHistoryDetail);
/*
            var patientObstetricsHistoryForm = new ContentPane({id:"obstetric_history_form",
                                                        },
                                                        "obstetric_history_form"
                                                        );
            patientObstetricsPreventivesTab.addChild(patientObstetricsHistoryForm);
*/

          var patientGynaecologyPreventivesTab = new ContentPane({id:"patientGynaecologyPreventivesTab",
                                                       title:"Gynaecology"
                                                      },
                                                      "patientGynaecologyPreventivesTab"
                                                      );
          preventiveHealthTabs.addChild(patientGynaecologyPreventivesTab);
          var patientMedicalPreventivesTab      = new ContentPane({id:"patientMedicalPreventivesTab",
                                                       title:"Medical & Surgical",
                                                       disabled: true
                                                      },
                                                      "patientMedicalPreventivesTab"
                                                      );
          preventiveHealthTabs.addChild(patientMedicalPreventivesTab);

      var medicationAndAllergiesTab = new ContentPane({id:"patientMedicationListAndAllergiesTab",
                                                       title:"Medications & Allergies"
                                                      },
                                                      "patientMedicationListAndAllergiesTab"
                                                      );
      tabs.addChild(medicationAndAllergiesTab);
      var admissionAndVisitTab      = new ContentPane({id:"patientAdmissionAndVisitsTab",
                                                       title:"Admissions & Visits"
                                                      },
                                                      "patientAdmissionAndVisitsTab"
                                                      );
      tabs.addChild(admissionAndVisitTab);
      var mediaTab                 = new ContentPane({id:"patientMediaTab",
                                                       title:"Media"
                                                      },
                                                      "patientMediaTab"
                                                      );
      tabs.addChild(mediaTab);

     mainContainer.startup();
     tabs.startup();
     historyTabs.startup();
     preventiveHealthTabs.startup();

     console.log("All tabs initialized...");

     registry.byId("centerMainPane").resize();


//{% if perms.patient.add_patientcontact %}
    var addContactButton =  new Button({
                                  label: "Add",
                                  title: "Add New Contact Details",
                                  iconClass: "addPatientContactIcon_16",
                                  onClick: function(){
                                            require(["dojo/_base/xhr", "dojo/_base/array"],
                                            function(xhr, array){
                                                xhr.get({
                                                        url: "{%url contact_json %}"+
                                                             "?patient_id="+ 
                                                             dom.byId("selected_patient_id_info").innerHTML +
                                                             "&action=add",
                                                        load: function(html){
                                                                      var myDialog = dijit.byId("editPatientDialog");
                                                                      myDialog.set('content', html);
                                                                      myDialog.set('title', "Add Postal Address Information");
                                                                      myDialog.show();
                                                              }
                                                 });
                                            });
                                 }
                              }, 
                              domConstruct.create('button',
                                                  {type : "button",
                                                   id   : "addContactButton"
                                                  },
                                                  "contact_list",
                                                  "before"
                              )
    );
//{% endif %}


//{% if perms.patient.add_patientphone %}
	  var addPhoneButton =  new Button({
                                    label: "Add",
                                    title: "Add New Phone Numbers",
                                    iconClass: "addPatientPhoneIcon_16",
                                    onClick: function(){
                                           require(
                                            ["dojo/_base/xhr", "dojo/_base/array"],
                                            function(xhr, array){
                                              xhr.get({
                                                url: "{%url phone_json %}"+"?patient_id="+ 
                                                       dom.byId("selected_patient_id_info").innerHTML +
                                                      "&action=add",
                                                load: function(html){
                                                             var myDialog = dijit.byId("editPatientDialog");
                                                             myDialog.set('content', html);
                                                             myDialog.set('title', "Add Phone Numbers");
                                                             myDialog.show();
                                                       }
                                             });
                                           })
                                    }
                         }, 
                         domConstruct.create('button',
                                            {type :"button",
                                             id   :"addPhoneButton"
                                            },
                                            "phone_list",
                                            "before"
                         )
  );
//{% endif %}

//{%if perms.patient.add_patientguardian %}
    var addGuardianButton =  new Button({
                                        label: "Add",
                                        title:"Add Guardian Details",
                                        iconClass: "dijitIconNewTask",
                                        onClick: function(){
                                               require(
                                                ["dojo/_base/xhr", "dojo/_base/array"],
                                                function(xhr, array){
                                                  xhr.get({
                                                    url: "{%url guardian_json %}"+"?patient_id="+ 
                                                          dom.byId("selected_patient_id_info").innerHTML +
                                                          "&action=add",
                                                    load: function(html){
                                                             var myDialog = dijit.byId("editPatientDialog");
                                                             myDialog.set('content', html);
                                                             myDialog.set('title', "Add Guardian Information ");
                                                             myDialog.show();
                                                          }
                                                 });
                                               })
                                        }
                         }, 
                         domConstruct.create('button',
                                              {type : "button",
                                               id   : "addGuardianButton"
                                              },
                                              "guardian_list",
                                              "before")
    );
//{% endif %}

//{% if perms.admission.add_admissiondetail %}
	  var addAdmissionButton =  new Button({
                                        label: "Add",
                                        title:"Add New Admission",
                                        iconClass: "dijitIconNewTask",
                                        onClick: function(){
                                               require(
                                                ["dojo/_base/xhr", "dojo/_base/array"],
                                                function(xhr, array){
                                                  //var gridRow    = grid.selection.getSelected();
                                                  //var id = grid.store.getValue(gridRow[0], 'id');
                                                  xhr.get({
                                                    url: "{%url admission_json %}"+
                                                          "?patient_id="+ 
                                                          dom.byId("selected_patient_id_info").innerHTML +
                                                          "&action=add",
                                                    load: function(html){
                                                               var myDialog = dijit.byId("editPatientDialog");
                                                               myDialog.set('content', html);
                                                               myDialog.set('title', 
                                                                            "Record New Admission to the Clinic ");
                                                               myDialog.show();
                                                          }
                                                 });
                                               })
                                        }
                                      }, 
                                      domConstruct.create('button',
                                                          {type : "button",
                                                           id   : "addAdmissionButton"
                                                          },
                                                          "admission_list",
                                                          "before"
                                      )
);
//{% endif %}

//{% if perms.visit.add_visitdetail %}
	  var addVisitButton =  new Button({
                                    label: "Add",
                                    title: "Add New OPD Visit",
                                    iconClass: "dijitIconNewTask",
                                    onClick: function(){
                                           require(
                                            ["dojo/_base/xhr", "dojo/_base/array"],
                                            function(xhr, array){
                                              xhr.get({
                                                url: "{%url visit_json %}"+
                                                     "?patient_id="+ 
                                                     dom.byId("selected_patient_id_info").innerHTML +
                                                     "&action=add",
                                                load: function(html){
                                                           var myDialog = dijit.byId("editPatientDialog");
                                                           myDialog.set('content', html);
                                                           myDialog.set('title', " Record New Out Patient Visit ");
                                                           myDialog.show();
                                                      }
                                             });
                                           })
                                    }
                         }, 
                         domConstruct.create('button',
                                              {type : "button",
                                               id   : "addVisitButton"
                                              },
                                              "visit_list",
                                              "before"
                         )
  );
//{% endif %}

//{% comment %}
//{% if perms.patient %}
	  var addDemographicsButton =  new Button({
                                          label: "Add",
                                          title: "Add Demographics Data",
                                          iconClass: "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url demographics_json %}"+ 
                                                           "?patient_id=" + 
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record Demographics Information");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                         }, 
                          domConstruct.create('button',
                                              {type : "button",
                                               id   : "addDemographicsButton"
                                              },
                                              "demographics_add_or_edit_form",
                                              "before"
                          )
);
//{% endif %}
//{%endcomment%}

//{% if perms.patient %}
	  var addAllergyButton =  new Button({
                                      label: "Add",
                                      title: "Add Allergy Details",
                                      iconClass: "dijitIconNewTask",
                                      onClick: function(){
                                             require(
                                              ["dojo/_base/xhr", "dojo/_base/array"],
                                              function(xhr, array){
                                                xhr.get({
                                                  url: "{% url allergies_json %}"+
                                                       "?patient_id="+ 
                                                       dom.byId("selected_patient_id_info").innerHTML +
                                                       "&action=add",
                                                  load: function(html){
                                                             var myDialog = dijit.byId("editPatientDialog");
                                                             myDialog.set('content', html);
                                                             myDialog.set('title', "Record New Allergy Details");
                                                             myDialog.show();
                                                        }
                                               });
                                             })
                                      }
                         }, 
                        domConstruct.create('button',
                                            {type : "button",
                                             id   : "addAllergyButton"
                                            },
                                            "allergy_list",
                                            "before"
                        )
);
//{% endif %}

//{% if perms.patient %}
	  var addPatientImmunisationButton =  new Button({
                                          label: "Add",
                                          title: "Add Immunisation Details",
                                          iconClass: "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url immunisation_json %}"+
                                                           "?patient_id="+ 
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record New Immunisation Details");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                                       }, 
                                      domConstruct.create('button',
                                                          {type : "button",
                                                           id   : "addPatientImmunisationButton"
                                                          },
                                                          "immunisation_list",
                                                          "before"
                                      )
);
//{% endif %}

//{% if perms.patient %}
	  var addPatientFamilyHistoryButton =  new Button({
                                          label       : "Add",
                                          title       : "Add Family History Details",
                                          iconClass   : "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url family_history_json %}"+
                                                           "?patient_id="+ 
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record New Family History Details");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                         }, 
                         domConstruct.create('button',
                                            {type : "button",
                                             id   : "addPatientFamilyHistoryButton"
                                            },
                                            "family_history_list",
                                            "before"
                         )
);


//{% endif %}

//{% if perms.patient %}
    var addPatientMedicalHistoryButton =  new Button({
                                          label       : "Add",
                                          title       : "Add Medical History Details",
                                          iconClass   : "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url medical_history_json %}"+
                                                           "?patient_id="+
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record New Medical History Details");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                         },
                         domConstruct.create('button',
                                            {type : "button",
                                             id   : "addPatientMedicalHistoryButton"
                                            },
                                            "medical_history_list",
                                            "before"
                         )
);


//{% endif %}

//{% if perms.patient %}
    var addPatientSurgicalHistoryButton =  new Button({
                                          label       : "Add",
                                          title       : "Add Surgical History Details",
                                          iconClass   : "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url surgical_history_json %}"+
                                                           "?patient_id="+
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record New Surgical History Details");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                         },
                         domConstruct.create('button',
                                            {type : "button",
                                             id   : "addPatientSurgicalHistoryButton"
                                            },
                                            "surgical_history_list",
                                            "before"
                         )
);

//{% endif %}


//{% if perms.patient %}
	  var addPatientMedicationListButton =  new Button({
                                          label: "Add",
                                          title : "Add New Medication List",
                                          iconClass: "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "{%url medication_list_json%}"+
                                                           "?patient_id="+ 
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Record Medication Details");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                         }, 
                        domConstruct.create('button',
                                            {type : "button",
                                             id   : "addPatientMedicationListButton"
                                            },
                                            "medication_list",
                                            "before"
                        )
);
//{% endif %}


//{% if perms.patient %}
	  var addPatientMediaButton =  new Button({
                                          label: "Add",
                                          title : "Add Patient Media Attachements",
                                          iconClass: "dijitIconNewTask",
                                          onClick: function(){
                                                 require(
                                                  ["dojo/_base/xhr", "dojo/_base/array"],
                                                  function(xhr, array){
                                                    xhr.get({
                                                      url: "/AuShadha/pat/media/"+
                                                           "?patient_id="+ 
                                                           dom.byId("selected_patient_id_info").innerHTML +
                                                           "&action=add",
                                                      load: function(html){
                                                                 var myDialog = dijit.byId("editPatientDialog");
                                                                 myDialog.set('content', html);
                                                                 myDialog.set('title', "Add Patient Media");
                                                                 myDialog.show();
                                                            }
                                                   });
                                                 })
                                          }
                                  }, 
                                  domConstruct.create('button',
                                                      {type : "button",
                                                       id   : "addPatientMediaButton"
                                                      },
                                                      "patientMediaTab",
                                                      "first"
                                  )
);
//{% endif %}

    }
    console.log("Finished running script patient_context_tab_setup");
   });
  });

}

//patientContextTabSetup();
