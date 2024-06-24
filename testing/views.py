from django.shortcuts import render, redirect, get_object_or_404
from .models import TestPlan
from .forms import TestCaseForm,ChecklistForm, TestPlanForm,BugForm
from .models import TestCase,Checklist, TestPlan,Bug
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import AutoTest
from .forms import AutoTestForm
import subprocess
import datetime
import os
from jira import JIRA
from django.conf import settings
import logging




def auto_test_delete(request, pk):
    auto_test = get_object_or_404(AutoTest, pk=pk)
    auto_test.delete()
    return redirect('testing:auto_test_list')

def home(request):
    return render(request, 'testing/home.html')

def checklist_list(request):
    checklists = Checklist.objects.all()
    return render(request, 'testing/check_list.html', {'checklists': checklists})

def create_checklist(request):
    checklists = Checklist.objects.all()
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        if form.is_valid():
            form.save()
            form = ChecklistForm()  # Очистка формы для нового ввода
            return redirect('/testing/check_list/')
    else:
        form = ChecklistForm()
    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            checklist = checklist.order_by('id')
        elif id_sort == 'desc':
            checklist = checklist.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            checklist = checklist.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            checklist = checklist.filter(status=status)

    return render(request, 'testing/checklist_create.html', {'form2': form, 'checklists': checklists})


def manual_tests(request):
    cases = TestCase.objects.all()

    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            cases = cases.order_by('id')
        elif id_sort == 'desc':
            cases = cases.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            cases = cases.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            cases = cases.filter(status=status)

    return render(request, 'testing/manual_tests.html', {'cases': cases})


def tests(request):
    return render(request, 'testing/sidebar.html', {'title': 'Тест-планы'})


def test_case_create(req):
    if req.method == 'POST':
        modelform_case = TestCaseForm(req.POST)
        if modelform_case.is_valid():
            modelform_case.save()
            modelform_case = TestCaseForm()  
    else:
        modelform_case = TestCaseForm()
    cases = TestCase.objects.all().order_by('id')
  
    return render(req, 'testing/create_test_case.html', {'form': modelform_case, 'cases': cases})

def test_case_delete(req, id_case):
    case = get_object_or_404(TestCase, id=id_case)
    if req.method == 'POST':
        case.delete()
        return redirect('testing:manual_tests') 
    return render(req, 'testing/delete_test_case.html', {'case': case})

def delete_Checklist(request, checklist_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)
    if request.method == 'POST':
        checklist.delete()
        return redirect('testing:check_list')
    return render(request, 'testing/delete_checklist.html', {'checklist': checklist})

def edit_test_case(request, case_id):
    case = get_object_or_404(TestCase, id=case_id)
    cases = TestCase.objects.all()
    if request.method == 'POST':
        form = TestCaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect(reverse('testing:test_case_details', kwargs={'id': case.id}))  
    else:
        form = TestCaseForm(instance=case)
    return render(request, 'testing/edit_test_case.html', {'form': form, 'case': case,'cases': cases})

def edit_checklist(request, checklist_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)
    checklists = Checklist.objects.all()
    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            checklists = checklists.order_by('id')
        elif id_sort == 'desc':
            checklists = checklists.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            checklists = checklists.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            checklists = checklists.filter(status=status)
    if request.method == 'POST':
        form = ChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            return redirect(reverse('testing:checklist_details', kwargs={'id': checklist.id}))  # Используем reverse для генерации URL
    else:
        form = ChecklistForm(instance=checklist)
    return render(request, 'testing/checklist_edit.html', {'form2': form, 'checklist': checklist,'checklists': checklists})

def test_case_details(request, id):
    case = get_object_or_404(TestCase, pk=id)
    cases = TestCase.objects.all()
    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            cases = cases.order_by('id')
        elif id_sort == 'desc':
            cases = cases.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            cases = cases.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            cases = cases.filter(status=status)
    return render(request, 'testing/test_case_details.html', {'case': case, 'cases': cases})

def checklist_details(request, id):
    checklist = get_object_or_404(Checklist, pk=id)
    checklists = Checklist.objects.all()
    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            checklists = checklists.order_by('id')
        elif id_sort == 'desc':
            checklists = checklists.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            checklists = checklists.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            checklists = checklists.filter(status=status)
    return render(request, 'testing/checklist_details.html', {'checklist': checklist, 'checklists': checklists})


def update_status(request, case_id):
    case = get_object_or_404(TestCase, id=case_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(TestCase.STATUS_CHOICES):
            case.status = status
            case.save()
    return redirect('testing:test_case_details', id=case_id)

def update_checkstatus(request, checklist_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Checklist.STATUS_CHOICES):
            checklist.status = status
            checklist.save()
    return redirect('testing:checklist_details', id=checklist_id)


#testplan

def test_plans(request):
    testplans = TestPlan.objects.all()
    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            testplans = testplans.order_by('id')
        elif id_sort == 'desc':
            testplans = testplans.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            testplans = testplans.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            testplans = testplans.filter(status=status)
    return render(request, 'testing/test_plans.html', {'testplans': testplans})

def create_testplan(request):
    testplans = TestPlan.objects.all()
    if request.method == 'POST':
        form = TestPlanForm(request.POST)
        if form.is_valid():
            form.save()
            form = TestPlanForm()  # Очистка формы для нового ввода
            return redirect('/testing/test_plans/')
    else:
        form = TestPlanForm()

    return render(request, 'testing/testplan_create.html', {'form3': form, 'testplans': testplans})

def edit_testplan(request, testplan_id):
    testplan = get_object_or_404(TestPlan, id=testplan_id)
    testplans = TestPlan.objects.all()
    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            testplans = testplans.order_by('id')
        elif id_sort == 'desc':
            testplans = testplans.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            testplans = testplans.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            testplans = testplans.filter(status=status)
    if request.method == 'POST':
        form = TestPlanForm(request.POST, instance=testplan)
        if form.is_valid():
            form.save()
            return redirect(reverse('testing:testplan_details', kwargs={'id': testplan.id}))  # Используем reverse для генерации URL
    else:
        form = TestPlanForm(instance=testplan)
    return render(request, 'testing/testplan_edit.html', {'form3': form, 'testplan': testplan,'testplans': testplans})


def testplan_details(request, id):
    testplan = get_object_or_404(TestPlan, pk=id)
    testplans = TestPlan.objects.all()
    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            testplans = testplans.order_by('id')
        elif id_sort == 'desc':
            testplans = testplans.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            testplans = testplans.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            testplans = testplans.filter(status=status)
    return render(request, 'testing/testplan_details.html', {'testplan': testplan, 'testplans': testplans})

def update_testplanstatus(request, testplan_id):
    testplan = get_object_or_404(TestPlan, id=testplan_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(TestPlan.STATUS_CHOICES):
            testplan.status = status
            testplan.save()
    return redirect('testing:testplan_details', id=testplan_id)

def delete_testplan(request, testplan_id):
    testplan = get_object_or_404(TestPlan, id=testplan_id)
    if request.method == 'POST':
        testplan.delete()
        return redirect('testing:test_plans')  
    return render(request, 'testing/delete_testplan.html', {'testplan': testplan})


def auto_test_list(request):
    auto_test = AutoTest.objects.all()
    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            auto_tests = auto_tests.order_by('id')
        elif id_sort == 'desc':
            auto_tests = auto_tests.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            auto_tests = auto_tests.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            auto_tests = auto_tests.filter(status=status)
    return render(request, 'testing/auto_test_list.html', {'auto_test': auto_test})

def auto_test_detail(request, pk):
    auto_test = get_object_or_404(AutoTest, pk=pk)
    auto_tests = AutoTest.objects.all()
    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            auto_tests = auto_tests.order_by('id')
        elif id_sort == 'desc':
            auto_tests = auto_tests.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            auto_tests = auto_tests.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            auto_tests = auto_tests.filter(status=status)
    return render(request, 'testing/auto_test_detail.html', {'auto_tests': auto_tests, 'auto_test': auto_test})

def auto_test_create(request):
    auto_tests = AutoTest.objects.all()
    if request.method == 'POST':
        form = AutoTestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('testing:auto_test_list')
    else:
        form = AutoTestForm()

    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            auto_tests = auto_tests.order_by('id')
        elif id_sort == 'desc':
            auto_tests = auto_tests.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            auto_tests = auto_tests.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            auto_tests = auto_tests.filter(status=status)
    return render(request, 'testing/auto_test_form.html', {'form3': form,'auto_tests': auto_tests})

def auto_test_edit(request, pk):
    auto_test = get_object_or_404(AutoTest, pk=pk)
    auto_tests = AutoTest.objects.all()
    if request.method == 'POST':
        form = AutoTestForm(request.POST, request.FILES, instance=auto_test)
        if form.is_valid():
            form.save()
            return redirect('testing:auto_test_list')
    else:
        form = AutoTestForm(instance=auto_test)
    
    filter_type = request.GET.get('filter')
    if filter_type == 'id-sort':
        id_sort = request.GET.get('id-sort')
        if id_sort == 'asc':
            auto_tests = auto_tests.order_by('id')
        elif id_sort == 'desc':
            auto_tests = auto_tests.order_by('-id')
    elif filter_type == 'name':
        name = request.GET.get('name')
        if name:
            auto_tests = auto_tests.filter(name__icontains=name)
    elif filter_type == 'status':
        status = request.GET.get('status')
        if status:
            auto_tests = auto_tests.filter(status=status)

    return render(request, 'testing/auto_test_edit.html', {'form3': form, 'auto_tests': auto_tests, 'auto_test': auto_test})

def run_auto_test(request, pk):
    auto_test = get_object_or_404(AutoTest, pk=pk)
    auto_test.status = 'running'
    auto_test.save()


    test_file_path = auto_test.test_file.path


    if not os.path.exists(test_file_path):
        auto_test.status = 'failed'
        auto_test.save()
        return redirect('testing:auto_test_list')

    result = subprocess.run(['python', test_file_path], capture_output=True, text=True)

    auto_test.last_run_date = datetime.datetime.now()
    if result.returncode != 0:
        auto_test.status = 'failed'
    else:
        auto_test.status = 'passed'
    auto_test.save()

    return redirect('testing:auto_test_list')


def runall_autotests(request):
    auto_tests = AutoTest.objects.all()
    test_outputs = []
    for auto_test in auto_tests:
        auto_test.status = 'running'
        auto_test.save()


        test_file_path = auto_test.test_file.path

        if not os.path.exists(test_file_path):
            auto_test.status = 'failed'
            auto_test.save()
            test_outputs.append(f'{auto_test.name}: Файл не существует')
            continue


        result = subprocess.run(['python', test_file_path], capture_output=True, text=True)


        auto_test.last_run_date = datetime.datetime.now()
        if result.returncode != 0:
            auto_test.status = 'failed'
        else:
            auto_test.status = 'passed'
        auto_test.save()

        test_outputs.append(f'{auto_test.name}: {result.stdout}')

    request.session['test_outputs'] = test_outputs

    return redirect('testing:auto_test_list')

logger = logging.getLogger(__name__)

def create_bug(request):
    existing_bugs = Bug.objects.all()
    
    if request.method == 'POST':
        bug_form = BugForm(request.POST)
        
        if bug_form.is_valid():
            cleaned_data = bug_form.cleaned_data
            summary = cleaned_data['summary']
            description = cleaned_data['description']
            priority = cleaned_data['priority']
            
            jira_client = JIRA(
                basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN),
                options={'server': settings.JIRA_SERVER}
            )
            
            issue_fields = {
                'project': {'key': settings.JIRA_PROJECT_KEY},
                'summary': summary,
                'description': description,
                'issuetype': {'name': 'Bug'},
                'priority': {'name': priority}
            }
            
            jira_client.create_issue(fields=issue_fields)
            return redirect('testing:bug_list')
    else:
        bug_form = BugForm()

    context = {
        'form': bug_form,
        'bugs': existing_bugs
    }
    
    return render(request, 'testing/create_bug.html', context)

def bug_list(request):
    bugs = Bug.objects.all()
    return render(request, 'testing/bug_list.html', {'bugs': bugs})


def delete_bug(request, bug_id):
    bug = get_object_or_404(Bug, id=bug_id)
    
    try:

        jira = JIRA(basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN), options={'server': settings.JIRA_SERVER})


        jira_issue = jira.issue(bug.jira_id)
        jira_issue.delete()

        logger.info(f"Bug with ID: {bug.jira_id} deleted in Jira")
        bug.delete()

        return redirect('testing:bug_list')
    except Exception as e:
        logger.error(f"Error deleting bug in Jira: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    

def bug_detail(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    bugs = Bug.objects.all()
    
    return render(request, 'testing/bug_detail.html', {'bugs': bugs, 'bug': bug})   


def auto_test_edit(request, pk):
    auto_test = get_object_or_404(AutoTest, pk=pk)
    auto_tests = AutoTest.objects.all()
    if request.method == 'POST':
        form = AutoTestForm(request.POST, request.FILES, instance=auto_test)
        if form.is_valid():
            form.save()
            return redirect('testing:auto_test_list')
    else:
        form = AutoTestForm(instance=auto_test)
    

    return render(request, 'testing/auto_test_edit.html', {'form3': form, 'auto_tests': auto_tests, 'auto_test': auto_test})


def bug_edit(request, bug_id):
    bug = get_object_or_404(Bug, id=bug_id)
    bugs = Bug.objects.all()
    if request.method == 'POST':
        form = BugForm(request.POST, instance=bug)
        if form.is_valid():     
                jira = JIRA(basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN), options={'server': settings.JIRA_SERVER})

        
                jira_issue = jira.issue(bug.jira_id)
                jira_issue.update(fields={
                    'summary': form.cleaned_data['summary'],
                    'description': form.cleaned_data['description'],
                    'priority': {'name': form.cleaned_data['priority']}
                })
                form.save()
                return redirect('testing:bug_list')

    else:
        form = BugForm(instance=bug)

    return render(request, 'testing/bug_edit.html', {'form4': form,'bugs': bugs, 'bug': bug})


def statistics(request):
    test_cases = TestCase.objects.all()
    checklists = Checklist.objects.all()
    autotests = AutoTest.objects.all()
    bug = Bug.objects.all()

    stats = {
        'test_cases': {
            'total': test_cases.count(),
            'passed': test_cases.filter(status='passed').count(),
            'failed': test_cases.filter(status='failed').count(),
        },
        'checklists': {
            'total': checklists.count(),
            'passed': checklists.filter(status='passed').count(),
            'failed': checklists.filter(status='failed').count(),
        },
        'autotests': {
            'total': autotests.count(),
            'passed': autotests.filter(status='passed').count(),
            'failed': autotests.filter(status='failed').count(),
        },
        'bug': {
            'total': bug.count(),
        }
    }

    return render(request, 'testing/statistics.html', {'stats': stats})