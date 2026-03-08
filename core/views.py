from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Note, Assignment, Program, Tutorial, Subject, Tag, Announcement, Category
from .forms import UserRegisterForm  # we'll create a simple form
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import os


@login_required
def home(request):
    latest_notes = Note.objects.all().order_by('-upload_date')[:6]
    featured_subjects = Subject.objects.annotate(num_notes=Count('note')).filter(num_notes__gt=0)[:4]
    recent_updates = list(Note.objects.all().order_by('-upload_date')[:3]) + \
                    list(Assignment.objects.all().order_by('-upload_date')[:3])
    announcements = Announcement.objects.filter(is_active=True).order_by('-date')[:3]
    context = {
        'latest_notes': latest_notes,
        'featured_subjects': featured_subjects,
        'recent_updates': recent_updates[:6],
        'announcements': announcements,
    }
    return render(request, 'core/home.html', context)

@login_required
def notes_list(request):
    subjects = Subject.objects.all()
    selected_subject = request.GET.get('subject')
    query = request.GET.get('q')
    notes = Note.objects.all().order_by('-upload_date')
    if selected_subject:
        notes = notes.filter(subject_id=selected_subject)
    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(description__icontains=query))
    paginator = Paginator(notes, 9)
    page = request.GET.get('page')
    notes_page = paginator.get_page(page)
    context = {
        'subjects': subjects,
        'notes': notes_page,
        'selected_subject': selected_subject,
        'query': query,
    }
    return render(request, 'core/notes.html', context)

@login_required
def assignments_list(request):
    subjects = Subject.objects.all()
    selected_subject = request.GET.get('subject')
    query = request.GET.get('q')
    assignments = Assignment.objects.all().order_by('-upload_date')
    if selected_subject:
        assignments = assignments.filter(subject_id=selected_subject)
    if query:
        assignments = assignments.filter(Q(title__icontains=query) | Q(description__icontains=query))
    paginator = Paginator(assignments, 9)
    page = request.GET.get('page')
    assignments_page = paginator.get_page(page)
    context = {
        'subjects': subjects,
        'assignments': assignments_page,
        'selected_subject': selected_subject,
        'query': query,
    }
    return render(request, 'core/assignments.html', context)

@login_required
def programs_list(request):
    query = request.GET.get('q')
    programs = Program.objects.all().order_by('-upload_date')
    if query:
        programs = programs.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(language__icontains=query))
    paginator = Paginator(programs, 9)
    page = request.GET.get('page')
    programs_page = paginator.get_page(page)
    return render(request, 'core/programs.html', {'programs': programs_page, 'query': query})

@login_required
def tutorials_list(request):
    categories = Category.objects.all()  # Get all categories from DB
    selected_category = request.GET.get('category')  # This will be an ID
    query = request.GET.get('q')
    tutorials = Tutorial.objects.all().order_by('-upload_date')
    if selected_category:
        tutorials = tutorials.filter(category_id=selected_category)
    if query:
        tutorials = tutorials.filter(Q(title__icontains=query) | Q(content__icontains=query))
    paginator = Paginator(tutorials, 9)
    page = request.GET.get('page')
    tutorials_page = paginator.get_page(page)
    context = {
        'categories': categories,
        'tutorials': tutorials_page,
        'selected_category': int(selected_category) if selected_category else None,
        'query': query,
    }
    return render(request, 'core/tutorials.html', context)

# @login_required
# # Download view to increment counter
# def download_file(request, model, pk):
#     model_map = {'note': Note, 'assignment': Assignment, 'program': Program, 'tutorial': Tutorial}
#     obj = get_object_or_404(model_map[model], pk=pk)
#     obj.downloads += 1
#     obj.save()
#     return redirect(obj.file.url)

# Authentication
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def download_file(request, model, pk):
    model_map = {
        'note': Note,
        'assignment': Assignment,
        'program': Program,
        'tutorial': Tutorial
    }
    obj = get_object_or_404(model_map[model], pk=pk)
    # Increment download count
    obj.downloads += 1
    obj.save()
    # Serve the file as an attachment (forces download)
    file_path = obj.file.path  # full filesystem path
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    return response