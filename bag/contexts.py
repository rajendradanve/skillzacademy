from user_profile.models import Discount
from decimal import Decimal

def bag_contents(request):
    # Getting values of discount percentage and discount threshold amount. 
    discount = Discount.objects.filter(offer_name='Discount').first()
    discount_percentage = discount.discount_percentage
    discount_threshold = discount.discount_amount_threshold
    
    bag_items = []
    total = 0
    product_count = 0
    
    if total < discount_threshold:
        discount_delta = discount_threshold - total
        grand_total = total
    else:
        discount_delta = 0
        grand_total = total * Decimal(discount_percentage/100)
        
        
    context = {
        'bag_items': bag_items,
        'discount_percentage': discount_percentage,
        'discount_threshold': discount_threshold, 
        'total': total,
        'grand_totla': grand_total,
        'discount_delta': discount_delta,
        
    }
    
    return context