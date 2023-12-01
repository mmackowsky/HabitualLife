from django import forms
from .models import Category, Habit


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=100)

    class Meta:
        model = Category
        fields = ['name']


class HabitForm(forms.ModelForm):
    description = forms.CharField(max_length=250)
    active = forms.BooleanField()

    class Meta:
        model = Habit
        fields = ['description', 'active']
