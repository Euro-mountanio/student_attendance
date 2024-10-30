# myapp/forms.py
from django import forms
from .models import Student_record

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student_record
        fields = ['person_id', 'first_name', 'last_name', 'program_of_study', 'year_of_study']

    # Optionally, you can add form customization
    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['person_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['program_of_study'].widget.attrs.update({'class': 'form-control'})
        self.fields['year_of_study'].widget.attrs.update({'class': 'form-control'})
