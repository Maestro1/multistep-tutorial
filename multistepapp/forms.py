from django import forms
from multistepapp.models import Appl,AcademicInstitution
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.forms import modelformset_factory

class ApplicantDetailsForm(forms.ModelForm):
	class Meta:
		model = Appl
		fields = ('name','age')


class AcademicQualificationForm(forms.ModelForm):
	institution = forms.CharField(max_length=100, label='Name of institution',
		widget=forms.TextInput(attrs={'class': "form-control"}))

	date_from = forms.DateField(
		widget=forms.TextInput(
			attrs={'type':'date'}
			)

		)

	date_to = forms.DateField(
		widget=forms.TextInput(
			attrs={'type':'date'}
			)

		)

	course_duration = forms.CharField(max_length=100, label='Course duration',
		widget=forms.Select(choices=Course_duration))

	achievements = forms.FileField(label='Upload Certificate/ achievements awarded',help_text='max. 42 megabytes')




	class Meta:
		model = AcademicInstitution
		fields =('institution','date_from','date_to','course_duration','achievements')

AcademicQualificationFormSet = inlineformset_factory(Member,AcademicInstitution,form=AcademicQualificationForm,fields=['institution','date_from','date_to','course_duration','achievements'],extra=1,can_delete=True)
   