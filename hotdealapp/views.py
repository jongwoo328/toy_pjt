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


def result(request):
    key = request.GET.get('key')
    Hotdeal.objects.create(key=key)
    ranks = get_rank()
    result = []
    # result += get_fmk(key=key)
    result += get_ppmp(key=key)
    # result += get_ruliweb(key=key)
    context = {
        'key': key,
        'results': sorted(result, key=lambda x: (-len(x['date']), x['date']), reverse=True),
        'ranks': ranks,
    }
    return render(request, 'hotdealapp/result.html', context)

