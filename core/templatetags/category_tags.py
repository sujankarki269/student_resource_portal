from django import template
from ..models import Category

register = template.Library()

@register.inclusion_tag('core/includes/category_tree.html', takes_context=True)
def render_category_tree(context):
    # We need the current category slug to highlight active item
    request = context['request']
    current_slug = context.get('current_category_slug')
    # Get all top-level categories with their children pre-fetched
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    return {
        'categories': categories,
        'current_slug': current_slug,
        'request': request,
    }