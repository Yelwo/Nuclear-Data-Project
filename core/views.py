from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from isotopes.models import Isotope
from nucreactions.models import Reaction


def index(request):
    num_isotopes = Isotope.objects.all().count()
    num_reactions = Reaction.objects.all().count()
    return render(request, 'index.html', context={'num_isotopes': num_isotopes,
                                                  'num_reactions': num_reactions})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

