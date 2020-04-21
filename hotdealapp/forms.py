from django import forms
from .models import Hotdeal

# Choice = ((1, "제목 + 내용"), (2, "제목"))

class HotdealForm(forms.ModelForm):
    
    key = forms.CharField(
        label="",
        required=True,
        widget=forms.TextInput(attrs={'name': 'key', 'placeholder': '상품 입력', 'class': 'search_input', 'autocomplete': 'off'}),
    )
    # target = forms.ChoiceField(
    #     label="",
    #     choices=Choice)
    class Meta:
        model = Hotdeal
        fields = ['key']
