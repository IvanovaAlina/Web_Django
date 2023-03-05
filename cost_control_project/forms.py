from django import forms
from .models import Checks, CategoryPurchase

class CheckForm(forms.ModelForm):
    class Meta:
        model = Checks
        fields = ['date_check', 'summ_check', 'category', 'text']
        labels = {'date_check': 'Дата покупки','summ_check' :'Сумма покупки', 'category' : 'Категория', 'text':'Примечание'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class CategoryPurchaseForm(forms.ModelForm):
    class Meta:
        model = CategoryPurchase
        fields = ['name_purchase', 'comment']
        labels = {'name_purchase': 'Наименование', 'comment' : 'Комментарий'}
        widgets = {'comment': forms.Textarea(attrs={'cols': 80})}



