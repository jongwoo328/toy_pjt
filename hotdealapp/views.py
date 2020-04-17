from django.shortcuts import render
from .forms import HotdealForm
from .data import get_fmk, get_ppmp

# import time
# t = time.localtime()
# while True:
#     if t.tm_min % 10 == 0 and t.tm_sec == 0:
#         data = Data()

# Create your views here.
def index(request):
    # 데이터 불러올 로직
    if request.method == "POST":
        form = HotdealForm(request.POST)
        if form.is_valid():
            key = request.POST['key']
            target = request.POST['target']
            fmk_datas = get_fmk(key=key, target=target)
            ppmp_datas = get_ppmp(key=key, target=target)
            context = {
                'form': form,
                'datas': 1,
                'fmk_datas': fmk_datas,
                'ppmp_datas': ppmp_datas,
            }
            return render(request, 'hotdealapp/index.html', context)
    else:
        form = HotdealForm()
    # 핫딜데이터 (이름, url, 가격, 쇼핑몰 정보 보유)
    context = {
        'form': form,
        'datas': None,
    }
    return render(request, 'hotdealapp/index.html', context)
