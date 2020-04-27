from django.shortcuts import render, redirect
from .forms import HotdealForm
from .models import Hotdeal
from .data import get_fmk, get_ppmp, get_ruliweb
from django.db.models import Count

def get_rank():
    rank_limit = 5
    search_rank = []
    for rank in Hotdeal.objects.values('key').order_by('-count', 'key').annotate(count=Count('key'))[:rank_limit]:
        search_rank.append((rank.get('count'), rank.get('key')))
    return search_rank

def index(request):
    form = HotdealForm()
    context = {
        'form': form,
    }
    return render(request, 'hotdealapp/index.html', context)


# def result(request):
#     # 데이터 불러올 로직
#     if request.method == "POST":
#         form = HotdealForm(request.POST)
#         if form.is_valid():
#             form.save()
#             ranks = get_rank()
#             key = request.POST['key']
#             results = []
#             results += get_fmk(key=key)
#             results += get_ppmp(key=key)
#             results += get_ruliweb(key=key)
#             # target = request.POST['target']
#             context = {
#                 'form': form,
#                 'results': sorted(results, key=lambda x: (-len(x['date']), x['date']), reverse=True),
#                 'ranks': ranks
#             }
#             return render(request, 'hotdealapp/result.html', context)
#     else:
#         return redirect('hotdeal:index')

def result(request):
    key = request.GET.get('key')
    Hotdeal.objects.create(key=key)
    ranks = get_rank()
    result = []
    result += get_fmk(key=key)
    result += get_ppmp(key=key)
    result += get_ruliweb(key=key)
    context = {
        'key': key,
        'results': sorted(result, key=lambda x: (-len(x['date']), x['date']), reverse=True),
        'ranks': ranks,
    }
    return render(request, 'hotdealapp/result.html', context)