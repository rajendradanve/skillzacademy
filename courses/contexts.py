from .models import MainCategory, Category


def categories_list(request):
    
    main_categories = MainCategory.objects.all()
    categories = Category.objects.all()
    for x in main_categories:
        print(type(x))
        
    for y in categories:
        print(type(y))
    
    context = {
        
        'main_categories': main_categories,
        'categories': categories
        
    }
    
    return context
