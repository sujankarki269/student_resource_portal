from django.contrib import admin
from .models import Subject, Note, Assignment, Program, Category,Tutorial, Tag, Announcement

admin.site.register(Subject)
admin.site.register(Note)
admin.site.register(Assignment)
admin.site.register(Program)
admin.site.register(Tutorial)
admin.site.register(Tag)
admin.site.register(Announcement)
admin.site.register(Category)