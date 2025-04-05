from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import cutoff

# ✅ Mapping user-friendly dropdown values to actual database branch names
BRANCH_MAPPING = {
    "CSE": "Computer Science and Engineering",
    "IT": "Information Technology",
    "EXTC": "Electronics and Telecommunication Engg",
    "MECH": "Mechanical Engineering",
    "CIVIL": "Civil Engineering",
    "AI&DS": "Artificial Intelligence and Data Science",
}


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
    return render(request, 'search_colleges.html', context=context)


@login_required
def search_colleges(request):
    item_searched = ""
    percentile_entered_float = None
    selected_branch = ""
    selected_status = ""

    # ✅ Always fetch branches and status for the navbar dropdowns
    branches = list(cutoff.objects.values_list('branch_name', flat=True).distinct())
    status_categories = list(cutoff.objects.values_list('status_category', flat=True).distinct())

    colleges = cutoff.objects.all().order_by('-open_percentile')

    if request.method == 'POST':
        item_searched = request.POST.get('search', '').strip()
        percentile_entered = request.POST.get('percentile_entered', '').strip()
        selected_branch = request.POST.get('branch', '').strip()
        selected_status = request.POST.get('status_category', '').strip()

        selected_branch_db = BRANCH_MAPPING.get(selected_branch, selected_branch)

        if percentile_entered:
            try:
                percentile_entered_float = float(percentile_entered)
            except ValueError:
                percentile_entered_float = None

        if selected_branch_db:
            colleges = colleges.filter(branch_name__iexact=selected_branch_db)

        if selected_status:
            colleges = colleges.filter(status_category__iexact=selected_status)

        if item_searched:
            colleges = colleges.filter(college_name__icontains=item_searched)

        if percentile_entered_float is not None:
            colleges = colleges.filter(open_percentile__lte=percentile_entered_float)

    context = {
        'colleges': colleges,
        'branches': branches,
        'status_categories': status_categories,
        'item_searched': item_searched,
        'percentile_entered_float': percentile_entered_float,
        'selected_branch': selected_branch,
        'selected_status': selected_status,
    }
    return render(request, 'search_colleges.html', context)
