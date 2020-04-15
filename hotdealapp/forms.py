from django import forms
from .models import Hotdeal

Choice = (("title", "제목"), ("content", "내용"), ("title_content", "제목 + 내용"))

class HotdealForm(forms.ModelForm):
    
    key = forms.CharField(
        # label=_("검색"),
        # help_text="싸게 사고 싶은 상품을 입력해주세요.",
        required=True,
        widget=forms.TextInput(attrs={'name': 'key', 'placeholder': '상품 입력'}),
    )
    
    target = forms.ChoiceField(choices=Choice)
    class Meta:
        model = Hotdeal
        fields = ['key', 'target']
