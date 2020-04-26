from django.shortcuts import render, redirect
from .forms import HotdealForm
from .data import get_fmk, get_ppmp, get_ruliweb

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
            results = []
            results += get_fmk(key=key)
            results += get_ppmp(key=key)
            results += get_ruliweb(key=key)
            # target = request.POST['target']
            context = {
                'form': form,
                'datas': 1,
                'results': results,
            }
            return render(request, 'hotdealapp/result.html', context)
    else:
        return redirect('hotdeal:index')
