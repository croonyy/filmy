import os
import django
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "filmy.settings")  # project_name 项目名称
django.setup()

from django import forms


class MyForm(forms.ModelForm):
    xxx = forms.ChoiceField(choices=[...], widget=forms.RadioSelect())


if __name__ == "__main__":
    print(__file__)
    print(os.path.abspath(__file__))
    print(os.path.dirname(__file__))
    print(os.path.abspath(os.path.dirname(__file__)))

