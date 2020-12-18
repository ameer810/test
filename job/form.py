from django import forms

from .models import Apply, Job,Comments


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ['name', 'email', 'website', 'cv', 'cover_letter']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('owner', 'slug','favourite',)
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'
        exclude = ('user', 'job',)

