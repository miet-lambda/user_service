from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from users.forms import SimpleRegistrationForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = SimpleRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SimpleRegistrationForm()
    return render(request, 'admin/register.html', {'form': form})
