from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from src.models.orders import Order, OrderItem
from src.models.product import Item
from django.views.generic import View
from django.utils import timezone
# Create your views here.


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            context = {
                'orders': order
            }
            return render(self.request, "order_summary.html", context)
        except:
            messages.error(self.request, "You do not have an active order.")
            return redirect("/")


def Checkout(request):
    return render(request, "checkout.html")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=slug).exists():
            messages.info(request, "This item is already in your cart.")
            return redirect("ecommerce:Product", slug=slug)
        else:
            order.items.add(order_item)
            order_item.quantity = 1
            messages.success(request, "This item was added to your cart.")
            return redirect("ecommerce:Product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        order_item.save()
        messages.success(request, "This item was added to your cart.")
        return redirect("ecommerce:Product", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            get_current_page_url = request.META['HTTP_REFERER']
            if 'order-summary' in get_current_page_url:
                messages.info(
                    request, f"The item {order_item.item.title} was removed from your cart.")
                return redirect("ecommerce:order-summary")
            else:
                messages.info(request, "This item was removed from your cart.")
                return redirect("ecommerce:Product", slug=slug)
        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("ecommerce:Product", slug=slug)
    else:
        messages.warning(request, "You do not have an active order.")
        return redirect("ecommerce:Product", slug=slug)


@login_required
def add_quantity_in_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order = Order.objects.filter(user=request.user, ordered=False)[0]
    if order.items.filter(item__slug=item.slug).exists():
        order_item.quantity += 1
        if(order_item.quantity < 6):
            order_item.save()
            messages.info(
                request, f"{order_item.item.title} quantity was updated.")
            return redirect("ecommerce:order-summary")
        else:
            messages.warning(
                request, "Maximum per item quantity limit reached")
            return redirect("ecommerce:order-summary")
    else:
        messages.info(
            request, f"You don't have this item in your cart")
        return redirect("ecommerce:order-summary")


@login_required
def remove_quantity_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order = Order.objects.filter(user=request.user, ordered=False)[0]
    if order.items.filter(item__slug=item.slug).exists() and order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
        messages.info(
            request, f"{order_item.item.title} quantity was updated.")
        return redirect("ecommerce:order-summary")
    else:
        messages.warning(request, "Item quantity cannot be zero.")
        return redirect("ecommerce:order-summary")
