from django.shortcuts import render, redirect
from .forms import HotdealForm
from .data import get_fmk, get_ppmp, get_ruliweb, weather

# import time
# t = time.localtime()
# while True:
#     if t.tm_min % 10 == 0 and t.tm_sec == 0:
#         data = Data()

# Create your views here.
def index(request):
    form = HotdealForm()
    context = {
        'form': form,
    }
    return render(request, 'hotdealapp/index.html', context)


def result(request):
    # 데이터 불러올 로직
    if request.method == "POST":
        form = HotdealForm(request.POST)
        if form.is_valid():
            key = request.POST['key']
            # target = request.POST['target']
            fmk_datas = get_fmk(key=key)
            ppmp_datas = get_ppmp(key=key)
            ruliweb_datas = get_ruliweb(key=key)
            context = {
                'form': form,
                'datas': 1,
                'fmk_datas': fmk_datas,
                'ppmp_datas': ppmp_datas,
                'ruliweb_datas': ruliweb_datas,
            }
            return render(request, 'hotdealapp/result.html', context)
    else:
        return redirect('hotdeal:index')
