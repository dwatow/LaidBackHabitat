from django import forms

class OrderForm(forms.Form):
	customer_id = forms.CharField(max_length=10)
	customer_name = forms.CharField(max_length=255)
	customer_phone = forms.CharField(max_length=10)
	customer_address = forms.CharField(max_length=255, required=False)

