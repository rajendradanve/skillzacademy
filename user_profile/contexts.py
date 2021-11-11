from .models import Discount


def discount(request):
    
    discount = Discount.objects.filter(offer_name='Discount').first()
    
    discount_percentage = discount.discount_percentage
    discount_threshold = discount.discount_amount_threshold
    
    
    context = {
        'discount_percentage': discount_percentage,
        'discount_threshold': discount_threshold, 
    }
    
    return context
