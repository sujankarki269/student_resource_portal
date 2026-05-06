from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Note, Assignment, Program, Subject, Announcement, Category, Profile, PortfolioProfile, BlogPost, PublicationCategory, Bookmark, TutorialProgress
from django.http import FileResponse, Http404, JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_POST
import os
import json
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm


@login_required
def home(request):
    latest_notes = Note.objects.all().order_by('-upload_date')[:6]
    featured_subjects = Subject.objects.annotate(num_notes=Count('note')).filter(num_notes__gt=0)[:4]
    recent_updates = [{'item': n, 'type': 'Note'} for n in Note.objects.all().order_by('-upload_date')[:3]] + \
                    [{'item': a, 'type': 'Assignment'} for a in Assignment.objects.all().order_by('-upload_date')[:3]]
    announcements = Announcement.objects.filter(is_active=True).order_by('-date')[:3]
    context = {
        'latest_notes': latest_notes,
        'featured_subjects': featured_subjects,
        'recent_updates': recent_updates[:6],
        'announcements': announcements,
        'stats': {
            'notes': Note.objects.count(),
            'assignments': Assignment.objects.count(),
            'programs': Program.objects.count(),
            'subjects': Subject.objects.count(),
        },
    }
    return render(request, 'core/home.html', context)

def _word_search(queryset, query, fields):
    """Return queryset filtered by every word in query across the given fields."""
    words = [w for w in query.strip().split() if w]
    if not words:
        return queryset
    combined = Q()
    for word in words:
        word_q = Q()
        for field in fields:
            word_q |= Q(**{f'{field}__icontains': word})
        combined |= word_q
    return queryset.filter(combined).distinct()

@login_required
def notes_list(request):
    subjects = Subject.objects.annotate(num_notes=Count('note'))
    selected_subject = request.GET.get('subject')
    query = request.GET.get('q', '').strip()
    notes = Note.objects.select_related('subject').prefetch_related('tags').order_by('-upload_date')
    if selected_subject:
        notes = notes.filter(subject_id=selected_subject)
    if query:
        notes = _word_search(notes, query, [
            'title', 'description', 'subject__name', 'tags__name',
        ])
    paginator = Paginator(notes, 9)
    notes_page = paginator.get_page(request.GET.get('page'))
    bookmarked_ids = set(
        Bookmark.objects.filter(user=request.user, note__isnull=False)
        .values_list('note_id', flat=True)
    )
    context = {
        'subjects': subjects,
        'notes': notes_page,
        'selected_subject': selected_subject,
        'query': query,
        'bookmarked_ids': bookmarked_ids,
    }
    return render(request, 'core/notes.html', context)

@login_required
def assignments_list(request):
    subjects = Subject.objects.annotate(num_notes=Count('assignment'))
    selected_subject = request.GET.get('subject')
    query = request.GET.get('q', '').strip()
    assignments = Assignment.objects.select_related('subject').prefetch_related('tags').order_by('-upload_date')
    if selected_subject:
        assignments = assignments.filter(subject_id=selected_subject)
    if query:
        assignments = _word_search(assignments, query, [
            'title', 'description', 'subject__name', 'tags__name',
        ])
    paginator = Paginator(assignments, 9)
    assignments_page = paginator.get_page(request.GET.get('page'))
    bookmarked_ids = set(
        Bookmark.objects.filter(user=request.user, assignment__isnull=False)
        .values_list('assignment_id', flat=True)
    )
    context = {
        'subjects': subjects,
        'assignments': assignments_page,
        'selected_subject': selected_subject,
        'query': query,
        'bookmarked_ids': bookmarked_ids,
    }
    return render(request, 'core/assignments.html', context)

@login_required
def programs_list(request):
    subjects = Subject.objects.annotate(num_notes=Count('programs'))
    selected_subject = request.GET.get('subject')
    query = request.GET.get('q', '').strip()
    programs = Program.objects.select_related('subject').prefetch_related('tags').order_by('-upload_date')
    if selected_subject:
        programs = programs.filter(subject_id=selected_subject)
    if query:
        programs = _word_search(programs, query, [
            'title', 'description', 'language', 'subject__name', 'tags__name',
        ])
    paginator = Paginator(programs, 9)
    programs_page = paginator.get_page(request.GET.get('page'))
    bookmarked_ids = set(
        Bookmark.objects.filter(user=request.user, program__isnull=False)
        .values_list('program_id', flat=True)
    )
    context = {
        'subjects': subjects,
        'programs': programs_page,
        'selected_subject': selected_subject,
        'query': query,
        'bookmarked_ids': bookmarked_ids,
    }
    return render(request, 'core/programs.html', context)

@login_required
def download_file(request, model, pk):
    model_map = {
        'note': Note,
        'assignment': Assignment,
        'program': Program,
    }
    obj = get_object_or_404(model_map[model], pk=pk)
    obj.downloads += 1
    obj.save()
    file_path = obj.file.path
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    return response

@login_required
@xframe_options_exempt
def pdf_preview(request, model, pk):
    """Serve a PDF inline for the preview modal — no X-Frame-Options header."""
    model_map = {
        'note': Note,
        'assignment': Assignment,
        'program': Program,
    }
    if model not in model_map:
        raise Http404
    obj = get_object_or_404(model_map[model], pk=pk)
    if not obj.file:
        raise Http404
    file_path = obj.file.path
    if not file_path.lower().endswith('.pdf'):
        raise Http404
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
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

    top_categories = Category.objects.filter(parent__isnull=True)

    completed_ids = set(
        TutorialProgress.objects.filter(user=request.user)
        .values_list('blog_post_id', flat=True)
    )

    subs_with_progress = []
    if subcategories.exists():
        for sub in subcategories:
            sub_post_ids = list(
                sub.blog_posts.filter(is_published=True).values_list('id', flat=True)
            )
            total = len(sub_post_ids)
            done = sum(1 for pid in sub_post_ids if pid in completed_ids)
            subs_with_progress.append({
                'sub': sub,
                'total': total,
                'done': done,
                'pct': int(done * 100 / total) if total else 0,
            })

    context = {
        'category': category,
        'subcategories': subcategories,
        'subs_with_progress': subs_with_progress,
        'blog_posts': blog_posts,
        'display_post': display_post,
        'post_completed': display_post.id in completed_ids if display_post else False,
        'top_categories': top_categories,
        'current_category_slug': category.slug,
        'ancestor_slugs': ancestor_slugs,
    }
    return render(request, template_name, context)


@login_required
def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.views += 1
    post.save()
    post_completed = TutorialProgress.objects.filter(user=request.user, blog_post=post).exists()
    context = {
        'post': post,
        'post_completed': post_completed,
    }
    return render(request, 'core/blog_post_detail.html', context)


@login_required
def publications_list(request):
    categories = PublicationCategory.objects.prefetch_related('publications').all()
    context = {'categories': categories}
    return render(request, 'core/publications.html', context)


@login_required
@require_POST
def toggle_bookmark(request):
    data = json.loads(request.body)
    model_type = data.get('model')
    pk = data.get('pk')
    model_map = {'note': Note, 'assignment': Assignment, 'program': Program}
    if model_type not in model_map:
        return JsonResponse({'error': 'Invalid model'}, status=400)
    obj = get_object_or_404(model_map[model_type], pk=pk)
    filter_kwargs = {'user': request.user, model_type: obj}
    existing = Bookmark.objects.filter(**filter_kwargs).first()
    if existing:
        existing.delete()
        return JsonResponse({'bookmarked': False})
    Bookmark.objects.create(**filter_kwargs)
    return JsonResponse({'bookmarked': True})


@login_required
def bookmarks_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related(
        'note__subject', 'assignment__subject', 'program__subject'
    )
    notes_bm = [b for b in bookmarks if b.note_id]
    assignments_bm = [b for b in bookmarks if b.assignment_id]
    programs_bm = [b for b in bookmarks if b.program_id]
    context = {
        'notes_bm': notes_bm,
        'assignments_bm': assignments_bm,
        'programs_bm': programs_bm,
        'total': len(notes_bm) + len(assignments_bm) + len(programs_bm),
    }
    return render(request, 'core/bookmarks.html', context)


@login_required
@require_POST
def toggle_tutorial_progress(request):
    data = json.loads(request.body)
    post_id = data.get('post_id')
    blog_post = get_object_or_404(BlogPost, pk=post_id, is_published=True)
    existing = TutorialProgress.objects.filter(user=request.user, blog_post=blog_post).first()
    if existing:
        existing.delete()
        return JsonResponse({'completed': False})
    TutorialProgress.objects.create(user=request.user, blog_post=blog_post)
    return JsonResponse({'completed': True})