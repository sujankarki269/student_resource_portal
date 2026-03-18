from django import template
from ..models import Category

register = template.Library()

@register.inclusion_tag('core/includes/category_tree.html', takes_context=True)
def render_category_tree(context):
    request = context['request']
    current_slug = context.get('current_category_slug')
    ancestor_slugs = context.get('ancestor_slugs', [])   # get from context
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    return {
        'categories': categories,
        'current_slug': current_slug,
        'ancestor_slugs': ancestor_slugs,
        'request': request,
    }