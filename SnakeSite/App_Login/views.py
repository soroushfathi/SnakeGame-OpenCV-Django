from django.shortcuts import render, HttpResponseRedirect
from .forms import Sign_Up_Form, edit_info,change_description_pic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from Game_App.models import record


# Create your views here.


def home(request):
    records = record.objects.all()[:10]
    return render(request, 'App_Login/home.html', context={'records': records})


def sign_up(request):
    form = Sign_Up_Form()
    signed_up = False
    if request.method == 'POST':
        form = Sign_Up_Form(request.POST)
        if form.is_valid():
            form.save()
            signed_up = True
    diction = {'form': form, 'signed_up': signed_up}
    return render(request, 'App_Login/sign_up.html', context=diction)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Login:home'))
    diction = {'form': form}
    return render(request, 'App_Login/login.html', context=diction)


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:home'))


@login_required
def profile(request):
    return render(request, 'App_Login/profile.html',context={})


@login_required
def edit_information(request):
    current_user = request.user
    form = edit_info(instance=current_user)
    if request.method == 'POST':
        form = edit_info(instance=current_user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/edit_info.html', context={'form': form})


@login_required
def change_pass(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_Login:login'))
    diction = {'form':form}
    return render(request, 'App_Login/change_pass.html', context=diction)


@login_required
def add_desc_pic(request):
    current_user = request.user
    form = change_description_pic()
    if request.method == 'POST':
        form = change_description_pic(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_info = form.save(commit=False)
            new_info.user = current_user
            new_info.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/change_profile.html', context={'form': form})


@login_required
def change_desc_pic(request):
    current_user = request.user
    form = change_description_pic(instance=current_user.game_user)
    if request.method == 'POST':
        form = change_description_pic(instance=current_user.game_user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/change_profile.html', context={'form': form})



