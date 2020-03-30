from django import forms

from .models import Student

class StudentForm(forms.ModelForm):
    firstname = forms.CharField(label = 'First Name')

    lastname = forms.CharField(label = 'Last Name')

    username       = forms.CharField(label='Username', 
                        widget=forms.TextInput(attrs={"placeholder":"Username"}))

    password = forms.CharField( 
                        widget=forms.PasswordInput(
                                attrs={
                                    'placeholder':'Password',
                                    "class":"new-class-name two",
                                    "id":"my-id-for-textarea",
                                }))

    email = forms.EmailField(
                    label = 'Email',
                    required = False
    )
    class Meta:
        model = Student
        fields = [
            'firstname',
            'lastname',
            'username',
            'password',
            'email'
        ]
    
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if not email.endswith("ucsb.edu"):
            raise forms.ValidationError("This is not a valid UCSB email")
        else:
            return email
