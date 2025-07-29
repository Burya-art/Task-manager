from django import forms

from tasks.models import Project, Task


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name',
                'maxlength': 200,
            }),
        }
        labels = {
            'name': 'Project Name',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name.strip()) < 3:
            raise forms.ValidationError('Project name must contain at least 3 characters')
        return name.strip()


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'status', 'priority', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task name',
                'maxlength': 200,
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'name': 'Task Name',
            'status': 'Status',
            'priority': 'Priority',
            'deadline': 'Deadline',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name.strip()) < 3:
            raise forms.ValidationError('Task name must contain at least 3 characters')
        return name.strip()
