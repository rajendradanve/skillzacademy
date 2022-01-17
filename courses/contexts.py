"""
context to get values main categories and categories
in project
"""
from .models import MainCategory, Category


def categories_list(request):
    """
    Context to main_categories, categories
    """
    main_categories = MainCategory.objects.all().order_by('friendly_name')
    categories = Category.objects.all().order_by('friendly_name')

    context = {
        'main_categories': main_categories,
        'categories': categories
    }

    return context
