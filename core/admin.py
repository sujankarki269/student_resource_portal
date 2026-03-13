from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Subject, Note, Assignment, Program, Category, Tutorial, Tag, Announcement, Profile, WorkExperience, Education, Publication, HonorAward, SubjectTaught, Skill, PortfolioProfile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 1

class HonorAwardInline(admin.TabularInline):
    model = HonorAward
    extra = 1

class SubjectTaughtInline(admin.TabularInline):
    model = SubjectTaught
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

@admin.register(PortfolioProfile)
class PortfolioProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'surname', 'profile_picture', 'bio',
                       'address', 'mobile', 'email', 'nationality',
                       'date_of_birth', 'gender')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'twitter')
        }),
    )
    inlines = [WorkExperienceInline, EducationInline, PublicationInline,
               HonorAwardInline, SubjectTaughtInline, SkillInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.register(Subject)
admin.site.register(Note)
admin.site.register(Assignment)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'language', 'upload_date')
    list_filter = ('subject', 'language')
    search_fields = ('title', 'description')

admin.site.register(Tutorial)
admin.site.register(Tag)
admin.site.register(Announcement)
admin.site.register(Category)
