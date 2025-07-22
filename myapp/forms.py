from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UploadedFile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ["file"]

class QuestionForm(forms.Form):
    question = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ask your question here...'}),
        label=''
    )
    file_id = forms.ModelChoiceField(
        queryset=UploadedFile.objects.none(),
        label="Select Uploaded File",
        empty_label="Choose a file",
        to_field_name='id'
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(QuestionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['file_id'].queryset = UploadedFile.objects.filter(user=user).order_by('-upload_date')
