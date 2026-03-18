from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch
from .models import Note, Assignment, Program, Tutorial, Subject, Tag, Announcement, Category, Profile, PortfolioProfile, BlogPost 
from django.http import FileResponse
import os
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm


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
    subjects = Subject.objects.all()  # optionally annotate with program count
    selected_subject = request.GET.get('subject')
    query = request.GET.get('q')
    programs = Program.objects.all().order_by('-upload_date')
    if selected_subject:
        programs = programs.filter(subject_id=selected_subject)
    if query:
        programs = programs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(language__icontains=query)
        )
    paginator = Paginator(programs, 9)
    page = request.GET.get('page')
    programs_page = paginator.get_page(page)
    context = {
        'subjects': subjects,
        'programs': programs_page,
        'selected_subject': selected_subject,
        'query': query,
    }
    return render(request, 'core/programs.html', context)


@login_required
def tutorials_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
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
    obj.downloads += 1
    obj.save()
    file_path = obj.file.path
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    return response

@login_required
def profile(request):
    # Ensure profile exists (should be created by signal, but just in case)
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'core/profile.html', context)

@login_required
def portfolio(request):
    # Get the first (and only) profile; create one if none exists
    profile = PortfolioProfile.objects.first()
    if not profile:
        # Create a placeholder profile (optional)
        profile = PortfolioProfile.objects.create(
            first_name='Er. Sujan',
            surname='Karki',
            email='sujan@ioepc.edu.np'
        )
    print("Profile found:", profile)
    return render(request, 'core/portfolio.html', {'profile': profile})

@login_required
def tutorials_list(request):
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    context = {
        'categories': categories,
        'current_category_slug': None,  # for sidebar highlighting
    }
    return render(request, 'core/tutorials.html', context)

@login_required
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = category.children.all()
    blog_posts = category.blog_posts.filter(is_published=True).order_by('-created_date')

    # Get list of ancestor slugs for the current category
    ancestor_slugs = []
    parent = category.parent
    while parent:
        ancestor_slugs.append(parent.slug)
        parent = parent.parent

    # Choose template
    if subcategories.exists():
        template_name = 'core/parent_category.html'
        display_post = None
    else:
        template_name = 'core/subcategory_detail.html'
        display_post = blog_posts.first() if blog_posts.exists() else None
        if display_post:
            display_post.views += 1
            display_post.save()

    # Get all top-level categories for sidebar (if needed)
    top_categories = Category.objects.filter(parent__isnull=True)

    context = {
        'category': category,
        'subcategories': subcategories,
        'blog_posts': blog_posts,
        'display_post': display_post,
        'top_categories': top_categories,
        'current_category_slug': category.slug,
        'ancestor_slugs': ancestor_slugs,   # add this
    }
    return render(request, template_name, context)


@login_required
def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    # Increment views
    post.views += 1
    post.save()
    context = {
        'post': post,
    }
    return render(request, 'core/blog_post_detail.html', context)