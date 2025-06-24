from django.shortcuts import render, redirect
from .models import Profile
from .forms import SignUpForm, UserForm, ProfileForm
from django.contrib.auth import login ,authenticate
# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
          form.save()
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password1')
          user = authenticate(username=username, password=password)
          if user is not None:
              login(request, user)
              return redirect('/accounts/profile/')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile/profile.html', {'profile': profile})

def profile_update(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=request.user)
        profileform = ProfileForm(request.POST, instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            my_profile = profileform.save(commit=False)
            my_profile.user = request.user
            my_profile.save()
            return redirect('/accounts/profile/')
    else:
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)
    return render(request, 'profile/profile_update.html', {'userform': userform, 'profileform': profileform})