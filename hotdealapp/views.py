from django.shortcuts import render
from .forms import HotdealForm
from .data import get_fmk

# import time
# t = time.localtime()
# while True:
#     if t.tm_min % 10 == 0 and t.tm_sec == 0:
#         data = Data()

# Create your views here.
def index(request):
    # 데이터 불러올 로직
    if request.method == "POST":
        print(request.POST)
        form = HotdealForm(request.POST)
        key = request.POST['key']
        target = request.POST['target']
        datas = get_fmk(key=key, target=target)
        context = {
            'form': form,
            'datas': datas,
        }
        return render(request, 'hotdealapp/index.html', context)
    else:
        form = HotdealForm()
    # 핫딜데이터 (이름, url, 가격, 쇼핑몰 정보 보유)
        context = {
            'form': form,
        }
    return render(request, 'hotdealapp/index.html', context)
