from django import forms
from .models import Checks

class CheckForm(forms.ModelForm):
    class Meta:
        model = Checks
        fields = ['date_check', 'summ_check', 'text']
        labels = {'date_check': 'Дата покупки', 'summ_check' :'Сумма покупки', 'text':'Примечание'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

