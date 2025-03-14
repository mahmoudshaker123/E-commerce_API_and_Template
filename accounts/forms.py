from django import forms
from .models import Account


class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = Account
        fields = ['first_name' , 'last_name' , 'country' , 'email' , 'phone_number' ]


    def clean(self):
        cleaned_data = super(RegisterForm , self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
    def __init__(self , *args , **kwargs):
        super(RegisterForm , self).__init__(*args , **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter Country'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Enter Confirm Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'