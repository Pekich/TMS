from django import forms
from .models import TestCase, Checklist, TestPlan, Bug
from .models import AutoTest

class AutoTestForm(forms.ModelForm):
    class Meta:
        model = AutoTest
        fields = ['name', 'description', 'test_file']

    def __init__(self, *args, **kwargs):
        super(AutoTestForm, self).__init__(*args, **kwargs)
        self.fields['test_file'].widget = forms.FileInput(attrs={'class': 'custom-file-input'})

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['name', 'description', 'steps', 'expected_result']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'steps': forms.Textarea(attrs={'class': 'form-control'}),
            'expected_result': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['name','description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class TestPlanForm(forms.ModelForm):
    class Meta:
        model = TestPlan
        fields = ['name', 'description', 'start_date', 'end_date', 'priority']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }


class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['summary', 'description', 'priority']