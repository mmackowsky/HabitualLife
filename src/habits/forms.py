from colorfield.fields import ColorField
from django import forms
from django.forms import CheckboxInput, Select, TextInput

from .models import Category, Habit


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    color = ColorField(default="#FF0000")

    class Meta:
        model = Category
        fields = ["name", "color", "user"]


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = [
            "name",
            "category",
            "frequency",
            "is_positive",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(HabitForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["category"].queryset = Category.objects.filter(user=user)
