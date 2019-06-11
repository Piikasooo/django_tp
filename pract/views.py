from __future__ import unicode_literals
from django.shortcuts import render
from pract.forms import PetitonCrForm, RegistrationForm, LoginForm, VoteForm
from pract.models import Category, Petition, voted
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth.models import User
import random
from datetime import timedelta
# Create your views here.


def base_view(request):
    kol_petition = 0
    kol_votes = 0
    for petition in Petition.objects.all():
        kol_petition += 1
        kol_votes += petition.votes
        if int(petition.votes) >= 200:
            petition.status = 'Підписи зібрані'
            petition.save()
        elif int(petition.votes) < 200 and petition.date < timezone.now():
            petition.status = 'Підписи не зібрані'
            petition.save()
    categories = Category.objects.all()
    category = random.choice(Category.objects.all())
    petitions = Petition.objects.all()
    context = {
        'categories': categories,
        'petitions': petitions,
        'random': category,
        'kol_petition': kol_petition,
        'kol_votes': kol_votes,
    }
    return render(request, 'base.html', context)

def search_view(request):
    q = request.GET['q']
    user = User.objects.get(username=q)
    petitions = Petition.objects.filter(user=user)
    context = {
        'petitions': petitions
    }
    return render(request, 'search.html', context)

def petition_view(request, petition_slug):
    petition = Petition.objects.get(slug=petition_slug)
    context = {
        'petition': petition
    }
    return render(request, 'petition.html', context)

def save_vote_to_base_view(request):
    k = 0
    q = request.POST['q']
    petitions = Petition.objects.filter(title=q)
    vot = voted.objects.all()
    for v in vot:
        if v.voteFor == q and request.user == v.vote:
            k += 1
    if k == 0:
        for petition in petitions:
            petition.votes = int(petition.votes) + 1
            petition.save()
            new_vote = voted.objects.create(
                vote= request.user,
                voteFor = q
                )
            return HttpResponseRedirect(reverse('base'))
    else:
        return HttpResponseRedirect(reverse('base'))
    return render(request, 'petition.html', {'petitions': petitions})

def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    petitions_of_category = Petition.objects.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'petitions_of_category': petitions_of_category
    }
    return render(request, 'category.html', context)


def petition_create_view(request):
    form = PetitonCrForm(request.POST or None)
    context = {
        'form': form
    }
    return render(request, 'create.html', context)

def save_petition_to_base_view(request):
    form = PetitonCrForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        tittle = form.cleaned_data['title']
        category = form.cleaned_data['category']
        info = form.cleaned_data['info']
        new_petition = Petition.objects.create(
        user = request.user,
        title = tittle,
        category = category,
        info = info
        )
        return HttpResponseRedirect(reverse('thank_you'))
    return render(request, 'create.html', {'categories': categories})


def account_view(request):
    petition = Petition.objects.filter(user=request.user)
    context = {
        'petition': petition
    }
    return render(request, 'account.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form
    }
    return render(request, 'registration.html', context)

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form
    }
    return render(request, 'login.html', context)

def pop_view(request):
    categories = Category.objects.all()
    category = random.choice(Category.objects.all())
    petitions = Petition.objects.filter(status='Підписи зібрані')
    context = {
        'categories': categories,
        'petitions': petitions,
        'random':category
    }
    return render(request, 'pop.html', context)

def notPop_view(request):
    categories = Category.objects.all()
    category = random.choice(Category.objects.all())
    petitions = Petition.objects.filter(status='Підписи не зібрані')
    context = {
        'categories': categories,
        'petitions': petitions,
        'random': category
    }
    return render(request, 'notPop.html', context)
