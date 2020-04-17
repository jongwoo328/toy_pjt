from django import forms
from .models import Hotdeal

Choice = ((1, "제목 + 내용"), (2, "제목"))

class HotdealForm(forms.ModelForm):
    
    key = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'name': 'key', 'placeholder': '상품 입력'}),
    )
    
    target = forms.ChoiceField(choices=Choice)
    class Meta:
        model = Hotdeal
        fields = ['key', 'target']
