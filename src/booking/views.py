from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Concert, Ticket

# 1. View untuk Muka Depan (Senarai Konsert)
def concert_list(request):
    concerts = Concert.objects.all()
    return render(request, 'booking/concert_list.html', {'concerts': concerts})

# 2. View untuk User Baru Daftar
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Password automatik di-encrypt oleh Django!
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'booking/register.html', {'form': form})

# 3. View untuk User Login
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('concert_list')
    else:
        form = AuthenticationForm()
    return render(request, 'booking/login.html', {'form': form})

# 4. View untuk User Logout
def logout_user(request):
    logout(request)
    return redirect('concert_list')


# Fungsi ni dilindungi. Hanya user yang dah login boleh akses (OWASP: Access Control)
@login_required(login_url='login')
def book_ticket(request, concert_id):
    # Cari konsert mana yang ditekan
    concert = get_object_or_404(Concert, id=concert_id)
    
    # Semak kalau tiket masih ada
    if concert.available_tickets > 0:
        # Tolak 1 dari jumlah tiket
        concert.available_tickets -= 1
        concert.save()
        
        # Cipta rekod tiket rasmi untuk user ni
        Ticket.objects.create(user=request.user, concert=concert)
        messages.success(request, f'Berjaya tempah tiket untuk {concert.name}!')
    else:
        messages.error(request, 'Maaf, tiket dah habis terjual!')
        
    return redirect('concert_list')