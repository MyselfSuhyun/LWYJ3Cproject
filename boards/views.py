from django.shortcuts import render,redirect,get_object_or_404
from api.temhum import send,error
from .models import Board
from django.views.decorators.http import require_http_methods,require_POST,require_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@require_safe
def index(request):
    boards = Board.objects.order_by('-pk')
    boards = boards.filter(writer=request.user)
    context = {
        'boards':boards,
    }
    return render(request,'boards/index.html',context)

@login_required
@require_http_methods(['GET','POST'])
def search(request):
    if request.method=='POST':
        longitude = request.POST.get('longitude') # 경도
        latitude = request.POST.get('latitude') # 위도
        temperature = request.POST.get('temperature') #온도
        humidity= request.POST.get('humidity') #습도
        rth = send(longitude,latitude)
        err = error(temperature,humidity)
        board = Board(location=rth[0],api_tem=rth[1],api_hum=rth[2],real_tem=temperature,real_hum=humidity)
        board.error_tem = (rth[1]-err[0])/rth[1]*100
        board.error_hum = (rth[2]-err[1])/rth[2]*100
        board.writer = request.user
        board.save()
        return redirect('boards:index')
    else:
        # if request.GET.get('longitude'):
        #     longitude = request.GET.get('longitude') # 경도
        #     latitude = request.GET.get('latitude') # 위도
        #     temperature = request.GET.get('temperature') #온도
        #     humidity= request.GET.get('humidity') #습도
        #     rth = send(longitude,latitude)
        #     err = error(temperature,humidity)
        #     board = Board(location=rth[0],api_tem=rth[1],api_hum=rth[2],real_tem=temperature,real_hum=humidity)
        #     board.error_tem = (rth[1]-err[0])/rth[1]*100
        #     board.error_hum = (rth[2]-err[1])/rth[2]*100
        #     board.writer = request.user
        #     board.save()
        #     return redirect('boards:index')
        # else:
        board= Board()
    context = {
        'board':board,
    }
    return render(request,'boards/search.html',context)

@login_required
@require_safe
def graph(request):
    boards = Board.objects.order_by('-pk')
    boards = boards.filter(writer=request.user)
    key = boards.latest('id')
    board = get_object_or_404(Board,pk=key.pk)
    context = {
        'board':board,
    }
    return render(request,'boards/graph.html',context)

@login_required
@require_safe
def totalgraph(request):
    boards = Board.objects.order_by('-pk')
    boards = boards.filter(writer=request.user)
    apitem = []
    reatem = []
    apihum = []
    reahum = []
    credate =[]
    for i in range(boards.count()):
        apitem.append(boards[i].api_tem)
        reatem.append(boards[i].real_tem)
        apihum.append(boards[i].api_hum)
        reahum.append(boards[i].real_hum)
        credate.append(boards[i].id)
    context = {
        'boards':boards,
        'apitem':apitem,
        'reatem':reatem,
        'apihum':apihum,
        'reahum':reahum,
        'credate':credate,
    }
    return render(request,'boards/totalgraph.html',context)