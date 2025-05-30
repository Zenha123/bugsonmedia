from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

def login(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')

@login_required
def home(request):
    try:
        user = request.user
        social_auth = user.social_auth.get(provider='instagram')
        access_token = social_auth.extra_data['access_token']
        
        # Add Instagram profile data to context
        profile_data = {
            'username': social_auth.extra_data.get('username'),
            'profile_pic': social_auth.extra_data.get('profile_picture')
        }
        
        return render(request, 'home.html', {
            'user': user,
            'profile': profile_data
        })
        
    except Exception as e:
        messages.error(request, "Failed to fetch Instagram data")
        return redirect('login')
    
def home(request):
    return render(request,'home.html')

def logout(request):
    auth_logout(request)
    return redirect('login')