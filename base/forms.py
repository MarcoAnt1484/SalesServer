from django.forms import ModelForm
from django import forms
from .models import Sales, Inventory

class SalesForm(ModelForm):
	class Meta:
		model = Sales
		fields = '__all__'

class ProductsForm(ModelForm):
	class Meta:
		model = Inventory
		fields = ['Name', 'Description', 'ProductID', 'Amount', 'Price']

class InventoryForm(ModelForm):
	class Meta:
		model = Inventory
		fields = ['ProductID', 'Amount']

class FilterForm(forms.Form):
	startDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required = False)
	endDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required = False)

	ProductID = forms.IntegerField(required = False)
	Type = forms.ChoiceField(choices=[("Income","Income"),("Sales Amount","Sales Amount")])

class FilterFormTable(forms.Form):
	startDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required = False)
	endDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required = False)

	ProductID = forms.IntegerField(required = False)