from django.shortcuts import render,redirect,get_object_or_404
from numpy import sign
from api.temhum import send,error,gisangapi
from .models import Board, GisangGrid
from django.views.decorators.http import require_http_methods,require_POST,require_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import pandas as pd
from numpy import NaN

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
        gisanggrid = GisangGrid.objects.filter(si=rth[0],gu=rth[1])
        for i in range(gisanggrid.count()):
            if gisanggrid[i].do == 'default':
                gridx = gisanggrid[i].gridx
                gridy = gisanggrid[i].gridy
            if gisanggrid[i].do == rth[2]:
                gridx = gisanggrid[i].gridx
                gridy = gisanggrid[i].gridy
        apirth = gisangapi(rth[2],gridx,gridy)
        board = Board(location=apirth[0],api_tem=apirth[1],api_hum=apirth[2],real_tem=temperature,real_hum=humidity)
        board.error_tem = (apirth[1]-err[0])/apirth[1]*100
        board.error_hum = (apirth[2]-err[1])/apirth[2]*100
        board.writer = request.user
        board.save()
        return redirect('boards:index')
    else:
        if request.GET.get('longitude'):
            longitude = request.GET.get('longitude') # 경도
            latitude = request.GET.get('latitude') # 위도
            temperature = request.GET.get('temperature') #온도
            humidity= request.GET.get('humidity') #습도
            rth = send(longitude,latitude)
            err = error(temperature,humidity)
            gisanggrid = GisangGrid.objects.filter(si=rth[0],gu=rth[1])
            for i in range(gisanggrid.count()):
                if gisanggrid[i].do == 'default':
                    gridx = gisanggrid[i].gridx
                    gridy = gisanggrid[i].gridy
                if gisanggrid[i].do == rth[2]:
                    gridx = gisanggrid[i].gridx
                    gridy = gisanggrid[i].gridy
            apirth = gisangapi(rth[2],gridx,gridy)
            board = Board(location=apirth[0],api_tem=apirth[1],api_hum=apirth[2],real_tem=temperature,real_hum=humidity)
            board.error_tem = (apirth[1]-err[0])/apirth[1]*100
            board.error_hum = (apirth[2]-err[1])/apirth[2]*100
            board.writer = request.user
            board.save()
            return redirect('boards:index')
        else:
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

def gisangupdate(request):
    #엑셀 읽기
    if str(request.user) =='admin':
        a1 = pd.read_excel('gisangapi.xlsx', header=1)
        #읽은 엑셀을 리스트로변환
        alist = a1.values.tolist()
        for i in range(len(alist)):
            if alist[i][4] is NaN:
                alist[i][4] = 'default'
            if alist[i][5] is NaN:
                alist[i][5] = 'default'
            gisanggrid = GisangGrid(si=alist[i][2],gu=alist[i][3],do=alist[i][4],gridx=alist[i][5],gridy=alist[i][6])
            gisanggrid.save()
        return redirect('boards:search')
    else:
        return redirect('boards:search')

def gisnagdelete(request):
    if str(request.user) =='admin':
        gisanggrid = GisangGrid.objects.all()
        gisanggrid.delete()
        return redirect('boards:search')
    else:
        return redirect('boards:search')