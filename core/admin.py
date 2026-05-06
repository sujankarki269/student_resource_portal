from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db.models import Count

from .models import (
    Subject, Note, Assignment, Program,
    Category, Tag, Announcement,
    Profile,
    WorkExperience, Education, Publication,
    HonorAward, SubjectTaught, Skill, PortfolioProfile,
    BlogPost, PublicationCategory, PublicationItem,
)

admin.site.site_title  = "SRP Admin"
admin.site.site_header = "Student Resource Portal"
admin.site.index_title = "Content Management"


# ─────────────────────────────────────────────
#  Subject
# ─────────────────────────────────────────────
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display  = ('name', 'code', 'semester', 'note_count', 'assignment_count', 'program_count')
    list_filter   = ('semester',)
    search_fields = ('name', 'code')
    ordering      = ('semester', 'name')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _notes=Count('note', distinct=True),
            _assignments=Count('assignment', distinct=True),
            _programs=Count('programs', distinct=True),
        )

    @admin.display(description='Notes', ordering='_notes')
    def note_count(self, obj):
        return obj._notes

    @admin.display(description='Assignments', ordering='_assignments')
    def assignment_count(self, obj):
        return obj._assignments

    @admin.display(description='Programs', ordering='_programs')
    def program_count(self, obj):
        return obj._programs


# ─────────────────────────────────────────────
#  Tag
# ─────────────────────────────────────────────
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)
    ordering      = ('name',)


# ─────────────────────────────────────────────
#  Note
# ─────────────────────────────────────────────
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display      = ('title', 'subject', 'uploader', 'upload_date', 'downloads', 'views', 'file_link')
    list_filter       = ('subject', 'upload_date')
    search_fields     = ('title', 'description', 'subject__name')
    date_hierarchy    = 'upload_date'
    readonly_fields   = ('downloads', 'views', 'upload_date')
    filter_horizontal = ('tags',)
    save_on_top       = True
    ordering          = ('-upload_date',)
    list_per_page     = 20
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subject', 'description', 'file', 'tags'),
        }),
        ('Stats', {
            'fields': ('uploader', 'upload_date', 'downloads', 'views'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='File')
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">📎 View</a>', obj.file.url)
        return '—'


# ─────────────────────────────────────────────
#  Assignment
# ─────────────────────────────────────────────
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display      = ('title', 'subject', 'status_badge', 'due_date', 'uploader', 'upload_date', 'downloads')
    list_filter       = ('status', 'subject', 'due_date')
    search_fields     = ('title', 'description', 'subject__name')
    date_hierarchy    = 'upload_date'
    readonly_fields   = ('downloads', 'views', 'upload_date')
    filter_horizontal = ('tags',)
    save_on_top       = True
    ordering          = ('-upload_date',)
    list_per_page     = 20
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subject', 'description', 'file', 'tags'),
        }),
        ('Status & Deadline', {
            'fields': ('status', 'due_date'),
        }),
        ('Stats', {
            'fields': ('uploader', 'upload_date', 'downloads', 'views'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Status')
    def status_badge(self, obj):
        colours = {'draft': '#6c757d', 'submitted': '#0dcaf0', 'graded': '#198754'}
        colour = colours.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;'
            'border-radius:12px;font-size:.8rem;">{}</span>',
            colour, obj.get_status_display(),
        )


# ─────────────────────────────────────────────
#  Program
# ─────────────────────────────────────────────
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display      = ('title', 'subject', 'lang_badge', 'uploader', 'upload_date', 'downloads', 'views')
    list_filter       = ('subject', 'language')
    search_fields     = ('title', 'description', 'code_snippet')
    date_hierarchy    = 'upload_date'
    readonly_fields   = ('downloads', 'views', 'upload_date')
    filter_horizontal = ('tags',)
    save_on_top       = True
    ordering          = ('-upload_date',)
    list_per_page     = 20
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subject', 'language', 'description', 'code_snippet', 'file', 'tags'),
        }),
        ('Stats', {
            'fields': ('uploader', 'upload_date', 'downloads', 'views'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Language')
    def lang_badge(self, obj):
        colours = {
            'python': ('#3572A5', '#fff'), 'javascript': ('#f7df1e', '#000'),
            'js': ('#f7df1e', '#000'), 'c': ('#555', '#fff'), 'cpp': ('#f34b7d', '#fff'),
            'java': ('#b07219', '#fff'), 'html': ('#e34c26', '#fff'),
            'css': ('#563d7c', '#fff'), 'bash': ('#89e051', '#000'), 'sql': ('#e38c00', '#fff'),
        }
        bg, fg = colours.get(obj.language.lower(), ('#667eea', '#fff'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;'
            'border-radius:6px;font-size:.8rem;font-weight:700;">{}</span>',
            bg, fg, obj.language.upper(),
        )


# ─────────────────────────────────────────────
#  Announcement
# ─────────────────────────────────────────────
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display  = ('title', 'is_active', 'date', 'preview')
    list_filter   = ('is_active',)
    search_fields = ('title', 'content')
    list_editable = ('is_active',)
    ordering      = ('-date',)
    actions       = ['make_active', 'make_inactive']

    @admin.display(description='Preview')
    def preview(self, obj):
        return obj.content[:80] + ('…' if len(obj.content) > 80 else '')

    @admin.action(description='Activate selected')
    def make_active(self, request, qs):
        qs.update(is_active=True)

    @admin.action(description='Deactivate selected')
    def make_inactive(self, request, qs):
        qs.update(is_active=False)


# ─────────────────────────────────────────────
#  Category & BlogPost
# ─────────────────────────────────────────────
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ('name', 'parent', 'slug', 'child_count', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields       = ('name',)
    list_filter         = ('parent',)
    ordering            = ('parent__name', 'name')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _children=Count('children', distinct=True),
            _posts=Count('blog_posts', distinct=True),
        )

    @admin.display(description='Sub-categories', ordering='_children')
    def child_count(self, obj):
        return obj._children or '—'

    @admin.display(description='Posts', ordering='_posts')
    def post_count(self, obj):
        return obj._posts or '—'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'category', 'is_published', 'views', 'created_date', 'updated_date')
    prepopulated_fields = {'slug': ('title',)}
    list_filter         = ('is_published', 'category')
    search_fields       = ('title', 'summary')
    date_hierarchy      = 'created_date'
    readonly_fields     = ('views', 'created_date', 'updated_date')
    list_editable       = ('is_published',)
    save_on_top         = True
    ordering            = ('-created_date',)
    list_per_page       = 20
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'category', 'summary', 'content'),
        }),
        ('Publishing', {
            'fields': ('is_published', 'created_date', 'updated_date', 'views'),
        }),
    )



# ─────────────────────────────────────────────
#  Publications
# ─────────────────────────────────────────────
@admin.register(PublicationCategory)
class PublicationCategoryAdmin(admin.ModelAdmin):
    list_display        = ('name', 'order', 'item_count', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering            = ('order', 'name')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_items=Count('publications', distinct=True))

    @admin.display(description='Items', ordering='_items')
    def item_count(self, obj):
        return obj._items


@admin.register(PublicationItem)
class PublicationItemAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'authors', 'date', 'order', 'has_link', 'has_file')
    list_filter   = ('category', 'date')
    search_fields = ('title', 'authors', 'description')
    ordering      = ('order', '-date')
    save_on_top   = True

    @admin.display(description='Link', boolean=True)
    def has_link(self, obj): return bool(obj.link)

    @admin.display(description='File', boolean=True)
    def has_file(self, obj): return bool(obj.file)


# ─────────────────────────────────────────────
#  Portfolio
# ─────────────────────────────────────────────
class WorkExperienceInline(admin.TabularInline):
    model  = WorkExperience
    extra  = 1
    fields = ('order', 'job_title', 'employer', 'start_date', 'end_date')

class EducationInline(admin.TabularInline):
    model  = Education
    extra  = 1
    fields = ('order', 'degree', 'institution', 'start_date', 'end_date')

class PublicationInline(admin.TabularInline):
    model  = Publication
    extra  = 1
    fields = ('order', 'title', 'conference_journal', 'date')

class HonorAwardInline(admin.TabularInline):
    model  = HonorAward
    extra  = 1
    fields = ('order', 'title', 'issuer', 'date')

class SubjectTaughtInline(admin.TabularInline):
    model  = SubjectTaught
    extra  = 1
    fields = ('order', 'name')

class SkillInline(admin.TabularInline):
    model  = Skill
    extra  = 1
    fields = ('order', 'name', 'category')

@admin.register(PortfolioProfile)
class PortfolioProfileAdmin(admin.ModelAdmin):
    save_on_top = True
    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('first_name', 'surname'),
                'profile_picture', 'bio',
                ('address', 'mobile', 'email'),
                ('nationality', 'date_of_birth', 'gender'),
            ),
        }),
        ('Social Links', {
            'fields': (('github', 'linkedin', 'twitter'),),
            'classes': ('collapse',),
        }),
    )
    inlines = [
        WorkExperienceInline, EducationInline, PublicationInline,
        HonorAwardInline, SubjectTaughtInline, SkillInline,
    ]


# ─────────────────────────────────────────────
#  User (with Profile inline)
# ─────────────────────────────────────────────
class ProfileInline(admin.StackedInline):
    model               = Profile
    can_delete          = False
    verbose_name_plural = 'Profile'
    fields              = ('phone', 'address')

class CustomUserAdmin(UserAdmin):
    inlines      = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter  = ('is_staff', 'is_superuser', 'is_active')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

