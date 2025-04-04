from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import cutoff


# ========== AUTH VIEWS ==========

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Already logged in

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ========== MAIN APP VIEWS ==========

@login_required
def home(request):
    return redirect('search_colleges')


@login_required
def start(request):
    colleges = cutoff.objects.all().order_by('-open_percentile')
    context = {'colleges': colleges}
    return render(request, 'search_colleges.html', context=context)  # Replace 'testing.html' with 'start.html'


@login_required
def search_colleges(request):
    item_searched = 0
    percentile_entered_float = 0
    colleges = cutoff.objects.all().order_by('-open_percentile')
    if request.method == 'GET':
        colleges = cutoff.objects.all().order_by('-open_percentile')
        context = {'colleges': colleges, 'nor_search':True}
        return render(request, 'search_colleges.html', context=context)
    
    if request.method == 'POST':
        item_searched = request.POST.get('search', '')
        percentile_entered = request.POST.get('percentile_entered', '')
        if percentile_entered:
            try:
                percentile_entered_float = float(percentile_entered)
            except ValueError:
                percentile_entered_float = 0

        if item_searched:
            colleges = cutoff.objects.filter(college_name__icontains=item_searched).order_by('-open_percentile')
        elif not percentile_entered and not item_searched:
            colleges = cutoff.objects.all().order_by('-open_percentile')
            context = {'colleges': colleges}
            return render(request, 'search_colleges.html', context=context)

    context = {
        'colleges': colleges,
        'item_searched': item_searched,
        'percentile_entered_float': percentile_entered_float
    }
    return render(request, 'search_colleges.html', context=context)
