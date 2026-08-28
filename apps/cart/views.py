from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from apps.shop.models import Product

def cart_add(request, product_id):
    # додав додавання товару до сесії кошика
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    image_url = ''
    for attr in ['image', 'photo', 'img']:
        if hasattr(product, attr):
            img_obj = getattr(product, attr)
            if img_obj and hasattr(img_obj, 'url'):
                image_url = img_obj.url
                break
            elif isinstance(img_obj, str):
                image_url = img_obj
                break
                
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': image_url
        }
        
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'Товар {product.name} успішно додано до кошика!')
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))

def cart_increase(request, product_id):
    # додав збільшення кількості позиції в кошику
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        cart[pid]['quantity'] += 1
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart:cart_detail')

def cart_decrease(request, product_id):
    # додав зменшення кількості або видалення позиції з кошика
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        if cart[pid]['quantity'] > 1:
            cart[pid]['quantity'] -= 1
        else:
            del cart[pid]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart:cart_detail')

def cart_detail(request):
    # додав рендеринг сторінки кошика з розрахунком суми
    from django.shortcuts import render
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'total_price': total_price})
