from django.db import models
from django.utils import timezone

class TestPlan(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('not_start', 'not_start'),
        ('in_progress', 'in Progress'),
        ('completed', 'completed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='not_start')

    def __str__(self):
        return self.name
    


class TestCase(models.Model):

    STATUS_CHOICES = [
        ('not_tested', 'Не проверен'),
        ('passed', 'Пройден'),
        ('failed', 'Провален'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    steps = models.TextField()
    expected_result = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_tested')

    def __str__(self):
        return self.name
    

class Checklist(models.Model):

    STATUS_CHOICES = [
        ('not_tested', 'Не проверен'),
        ('passed', 'Пройден'),
        ('failed', 'Провален'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_tested')
    def __str__(self):
        return self.name
    

class AutoTest(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    test_file = models.FileField(upload_to='test_files/')
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_run_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('passed', 'Успешно'),
        ('failed', 'Провален'),
        ('not_run', 'Не запущен'),
    ], default='not_run')

    def __str__(self):
        return self.name
    

class Bug(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Низкий'),
        ('Medium', 'Средний'),
        ('High', 'Высокий'),
    ]
    
    summary = models.CharField(max_length=255)
    description = models.TextField()
    jira_id = models.CharField(max_length=20)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.summary