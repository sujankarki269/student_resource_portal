from .models import Tag, Announcement

def global_context(request):
    return {
        'all_tags': Tag.objects.all(),
        'active_announcements': Announcement.objects.filter(is_active=True)[:3],
    }