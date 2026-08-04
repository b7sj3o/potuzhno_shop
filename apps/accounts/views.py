from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {'orders': orders})
