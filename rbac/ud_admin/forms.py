from django import forms

from rbac.models import Test
# from ../models import Code
from rbac.ud_admin.widgets import AceWidget, JsonWidget
from django import forms


class UdModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Test
        # fields = [field.name for field in Test._meta.fields]
        fields = [field.name for field in model._meta.fields]


def GenerateUdModelForm(model, attrs={}):
    meta = type('Meta', (),
                {"model": model,
                 "fields": [field.name for field in model._meta.fields]})

    modelform = type(f'{model.__name__}UdModelForm', (forms.ModelForm,), attrs)
    modelform.Meta = meta
    return modelform


class TestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    title = forms.CharField()

    code2 = forms.CharField(label='源码2',
                            widget=AceWidget(
                                mode="json",
                                theme="dracula"),
                            )

    class Meta:
        model = Test
        # fields = [field.name for field in Test._meta.fields]
        fields = [field.name for field in model._meta.fields]
