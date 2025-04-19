from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Hovifix 👷🏾‍♂️💻")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Staff'  # Set default role
            form.save()  # ✅ Call this to save the password hash properly
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

