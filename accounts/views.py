from django.contrib.auth import get_user_model

from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import login, logout

User = get_user_model()


# Create your views here.

def authentication_view(request: WSGIRequest):
    return render(request, 'authentication.html')


def registration_view(request: WSGIRequest):
    if request.method == 'GET':
        return render(request, "registration.html")
    elif request.method == 'POST':
        data: dict = request.POST.dict()
        data['errors'] = []

        if data['username'] and data['email'] and data['password1'] and data['password2']:

            if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).count() > 0:
                data['errors'].append('*Такой username или email уже существует.')

            if data['password1'] != data['password2']:
                data['errors'].append('*Пароли не совпадают.')

        else:
            data['errors'].append('*Все поля должны быть заполнены.')
        if not (data['errors']):
            user = User(username=data['username'], email=data['email'])
            user.set_password(data['password1'])
            user.save()

            login(request, user)
            return redirect('home')

        return render(request, 'registration.html', context=data)


def user_login(request: WSGIRequest):
    if request.method == 'GET':
        return render(request, 'login.html', )
    elif request.method == 'POST':
        data: dict = request.POST.dict()
        data['errors'] = []

        if User.objects.filter(username=data['username']).exists():
            user: User = User.objects.get(username=data['username'])
            if user.check_password(data['password']):
                login(request, user)
                return redirect('home')
            else:
                data['errors'].append('Неправильный логин или пароль')
        return render(request, 'login.html', context=data)


def user_logout(request: WSGIRequest):
    logout(request)
    return redirect('home')
