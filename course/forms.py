from django.contrib.auth.models import User
from django.forms import forms, Form
from django import forms
class RegistrationForm(forms.Form):
    username=forms.CharField(max_length=30,label="username",required=True,error_messages={'invalid':'Username should be unique'})
    email=forms.EmailField(label="emailid",required=True)
    password1=forms.CharField(max_length=30,widget=forms.PasswordInput(),label="password",required=True)
    password2=forms.CharField(max_length=30,widget=forms.PasswordInput(),label="password(again)",required=True)
    options=[('teacher','Teacher'),('student','Student')]
    role=forms.ChoiceField(widget=forms.RadioSelect(),label="Account Type",required=True,choices=options)
    def clean_username(self):
        u=self.cleaned_data['username']
        try:
            u=User.objects.get(username__exact=u)
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("Username Already Exists . Please Try another name",code='invalid')
    def clean(self):
        p1=self.cleaned_data['password1']
        p2=self.cleaned_data['password2']
        if p1 is not None and p2 is not None:
            if p1 != p2:
                raise  forms.ValidationError("Two passwords did not match")
            else:
                return self.cleaned_data
        else:
            raise forms.ValidationError("Both fields should match")


class StudentsInformationForm(forms.Form):
    fullname=forms.CharField(max_length=64,required=True)
    options=[('Masters','Masters'),('Graduation','Graduation'),('UnderGraduate','Under Graduate')]
    qualification=forms.ChoiceField(widget=forms.RadioSelect(),choices=options,required=True)
    university=forms.CharField(max_length=32,required=True)
    phonenumber=forms.CharField(max_length=12,required=True)
    country=forms.CharField(max_length=32,required=True)

    def clean_phonenumber(self):
        if (self.cleaned_data['phonenumber'].__len__() < 10):
            raise forms.ValidationError("Invalid Phone Number")
        else:
            return self.cleaned_data['phonenumber']

class TeacherInformationForm(forms.Form):
    fullname=forms.CharField(max_length=64,required=True)
    options=[('Masters','Masters'),('Graduation','Graduation'),('UnderGraduate','Under Graduate')]
    qualification=forms.ChoiceField(widget=forms.RadioSelect(),choices=options,required=True)
    university=forms.CharField(max_length=32,required=True)
    phonenumber=forms.CharField(max_length=12,required=True)
    country=forms.CharField(max_length=32,required=True)
    experience=forms.IntegerField()

    def clean_experience(self):
        if(self.cleaned_data['experience']<=0):
            raise forms.ValidationError("Experience should be greater than 0")
        else:
            return self.cleaned_data['experience']
    def clean_phonenumber(self):
        if(self.cleaned_data['phonenumber'].__len__()<10):
            raise forms.ValidationError("Invalid Phone Number")
        else:
            return self.cleaned_data['phonenumber']



