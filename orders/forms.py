from django import forms
from .models import Order , OrderPayment

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order  
        fields = ['first_name', 'last_name', 'email' , 'address', 'postal_code', 'city']



class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = OrderPayment
        fields = ['payment_phone' , 'payment_image']


    def clean_payment_phone(self):
        payment_phone = self.cleaned_data.get('payment_phone')

        if not payment_phone.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        if len(payment_phone) != 11:
            raise forms.ValidationError('Phone number must be 11 digits long.')
        valid_prefixes = ['010', '011', '012', '015']
        if not any(payment_phone.startswith(prefix) for prefix in valid_prefixes):
            raise forms.ValidationError('Phone number must start with 010, 011, 012, or 015.')
        return payment_phone

        