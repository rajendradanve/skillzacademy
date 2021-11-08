from .models import MainCategory, Category


def categories_list(request):
    
    main_categories = MainCategory.objects.all()
    categories = Category.objects.all()
    
    context = {
        
        'main_categories': main_categories,
        'categories': categories
        
    }
    
    return context
