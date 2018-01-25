from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        if username == '' or password == '':
            return render(request, "index.html", {"error": "username or password null!"})
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 验证登录
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600)
            request.session['user'] = username  # 存入session信息到浏览器中
            request.session['pwd'] = password
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
    return render(request, "index.html")


@login_required()
def event_manage(request):
    username = request.session.get('user', '')
    event_list = Event.objects.all()
    # username = request.COOKIES.get('user', '')  # 注意COOKIES属性都为大写
    return render(request, 'event_manage.html', {"user": username, "events": event_list})


# 发布会名称搜索
@login_required()
def search_name(request):
    username = request.session.get('user', '')
    search_names = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_names)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


# 嘉宾管理
@login_required()
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    return render(request, 'guest_manage.html', {"user": username, "guests": guest_list})


# 嘉宾搜索
@login_required()
def search_phone(request):
    username = request.session.get('user', '')
    search_phones = request.GET.get('phone', '')
    search_name_bytes = search_phones.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {"user": username, "guests": contacts})


# 签到界面
@login_required()
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


# 签到动作
@login_required()
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'user has sign in'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success', 'guest': result})


# logout
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response
