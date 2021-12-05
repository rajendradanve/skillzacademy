from decimal import Decimal
from django.shortcuts import get_object_or_404
from user_profile.models import Discount

from courses.models import Course


def bag_contents(request):
    # Getting values of discount percentage and discount threshold amount.
    discount_percentage = 0
    discount_threshold = 0
    discount_delta = 0
    discount_flag = False
    
    if Discount.objects.filter(offer_flag=True).exists():
        discount_flag = True
        discount = Discount.objects.filter(offer_flag=True).first()
        discount_percentage = discount.discount_percentage
        discount_threshold = discount.discount_amount_threshold
        
    bag_items = []
    total = 0
    course_count = 0

    # created bag session variable if not exist.
    bag = request.session.get('bag', [])

    # Added bag items to bag_items list along with course object.
    for course_id in bag:
        course = get_object_or_404(Course, pk=course_id)
        total += course.price
        bag_items.append({
            'course_id': course_id,
            'course': course,
            })

    if discount_flag:
        if total < discount_threshold:
            discount_delta = discount_threshold - total
            grand_total = total
        else:
            discount_delta = 0
            grand_total = total * (1-Decimal(discount_percentage/100))
    else:
        grand_total = total

    context = {
        'bag_items': bag_items,
        'discount_percentage': discount_percentage,
        'discount_threshold': discount_threshold,
        'total': total,
        'grand_total': grand_total,
        'discount_delta': discount_delta,
        'discount_flag': discount_flag,
    }

    return context
