from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    """Form for creating and updating courses"""
    class Meta:
        model = Course
        fields = ['code', 'title', 'description', 'instructor', 'credits', 
                  'level', 'capacity', 'status', 'start_date', 'end_date']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Code'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'instructor': forms.Select(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CourseFilterForm(forms.Form):
    """Form for filtering courses"""
    LEVEL_CHOICES = [('', '--- All Levels ---')] + list(Course.LEVEL_CHOICES)
    STATUS_CHOICES = [('', '--- All Status ---')] + list(Course.STATUS_CHOICES)
    
    level = forms.ChoiceField(choices=LEVEL_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    search = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search courses...'}))
