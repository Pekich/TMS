from django.urls import path
from .views import home,statistics,bug_detail,bug_edit,delete_bug,runall_autotests,create_bug,bug_list,auto_test_list,auto_test_delete,auto_test_detail,auto_test_create,auto_test_edit,run_auto_test,update_testplanstatus,edit_testplan,delete_testplan,testplan_details,test_plans,create_testplan,create_checklist,delete_Checklist,edit_checklist, update_checkstatus,checklist_details, checklist_list,tests,manual_tests,test_case_create,test_case_details,test_case_delete,edit_test_case,update_status

app_name = 'testing'

urlpatterns = [
    
    path('', home, name='home'),
    path('tests/', tests, name='tests'),
    path('manual_tests/', manual_tests, name='manual_tests'),
    #path('test_plans/', test_plans, name='test_plans'),
    path('manual_tests/create/', test_case_create, name='create_test_case'),
    path('test-case-details/<int:id>/', test_case_details, name='test_case_details'),
    path('delete_test_case/<int:case_id>/', test_case_delete, name='delete_test_case'),
    path('test_case/<int:case_id>/edit/', edit_test_case, name='edit_test_case'), 
    path('update_status/<int:case_id>/', update_status, name='update_status'),

    path('check_list/create/', create_checklist, name='create_checklist'),
    path('check_list/', checklist_list, name='check_list'),
    path('checklist_details/<int:id>/', checklist_details, name='checklist_details'),
    path('delete_checklist/<int:checklist_id>/', delete_Checklist, name='delete_Checklist'),
    path('check_list/<int:checklist_id>/edit/', edit_checklist, name='edit_checklist'), 
    path('update_checkstatus/<int:checklist_id>/', update_checkstatus, name='update_checkstatus'),

    path('test_plans/create/', create_testplan, name='testplan_create'),
    path('test_plans/', test_plans, name='test_plans'),
    path('testplan_details/<int:id>/', testplan_details, name='testplan_details'),
    path('delete_testplan/<int:testplan_id>/', delete_testplan, name='delete_testplan'),
    path('test_plans/<int:testplan_id>/edit/', edit_testplan, name='edit_testplan'), 
    path('update_testplanstatus/<int:testplan_id>/', update_testplanstatus, name='update_testplanstatus'),


    path('auto_tests/', auto_test_list, name='auto_test_list'),
    path('auto_tests/<int:pk>/', auto_test_detail, name='auto_test_detail'),
    path('auto_tests/new/', auto_test_create, name='auto_test_create'),
    path('auto_tests/<int:pk>/edit/', auto_test_edit, name='auto_test_edit'),
    path('auto_tests/<int:pk>/run/', run_auto_test, name='run_auto_test'),
    path('<int:pk>/delete/', auto_test_delete, name='auto_test_delete'),
    path('run_all/', runall_autotests, name='runall_autotests'),

    path('create_bug/', create_bug, name='create_bug'),
    path('bug_list/', bug_list, name='bug_list'),
    path('delete_bug/<int:bug_id>/', delete_bug, name='delete_bug'),
    path('bug_detail/<int:pk>/', bug_detail, name='bug_detail'),
    path('bug/<int:bug_id>/edit/', bug_edit, name='bug_edit'), 

     path('statistics/', statistics, name='statistics'),
]
