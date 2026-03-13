from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Subject, Note, Assignment, Program, Category, Tutorial, Tag, Announcement, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.register(Subject)
admin.site.register(Note)
admin.site.register(Assignment)
admin.site.register(Program)
admin.site.register(Tutorial)
admin.site.register(Tag)
admin.site.register(Announcement)
admin.site.register(Category)