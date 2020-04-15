from django import forms
from .models import Hotdeal

class HotdealForm(forms.ModelForm):
    key = forms.CharField(
        # label=_("검색"),
        # help_text="싸게 사고 싶은 상품을 입력해주세요.",
        required=True,
        widget=forms.TextInput(attrs={'name': 'key', 'placeholder': '상품 입력'}),
    )
    target = forms.ChoiceField(
        # label=_("선택"),
        widget=forms.Select(attrs={'name': 'target'}),
    )
    class Meta:
        model = Hotdeal
        fields = '__all__'
