import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import get_object_or_404


from items.models import Order, Item

stripe.api_key = settings.STRIPE_SECRET_KEY




def buy(request, id):
    item = get_object_or_404(Item, pk=id)
    if not item:
        return JsonResponse({'error': 'Item not found'}, status=404)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                "unit_amount": int(item.price * 100),
            },
            'quantity': 1,   # <-- добавьте эту строку
        }],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return JsonResponse({'session_id': session.id})
def item(request, id):
    item = get_object_or_404(Item, pk=id)
    if not item:
        return JsonResponse({'error': 'Item not found'}, status=404)
    context = {
        'item': item,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'items/item.html', context)


def buy_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    currency = order.get_currency()

    line_items = []
    for item in order.items.all():
        item_data = {
            'price_data': {
                'currency': currency,
                'unit_amount': int(item.price * 100),
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
            },
            'quantity': 1,
        }

    if order.tax and order.tax.stripe_tax_rate_id:
        item_data['tax_rates'] = [order.tax.stripe_tax_rate_id]
        line_items.append(item_data)

    session_params = {
        'payment_method_types': ['card'],
        'line_items': line_items,
        'mode': 'payment',
        'success_url': 'http://localhost:8000/success/',
        'cancel_url': 'http://localhost:8000/cancel/',
    }

    if order.discount and order.discount.stripe_coupon_id:
        session_params['discounts'] = [{'coupon': order.discount.stripe_coupon_id}]


    session = stripe.checkout.Session.create(**session_params)
    return JsonResponse({'session_id': session.id})


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    context = {
        "order": order,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'total': order.get_total_price(),
    }
    return render(request, 'items/order.html', context)


