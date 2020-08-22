from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from src.models.product import Item

# Create your views here.


class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item.objects.all()
        paginator = Paginator(items, self.paginate_by)
        page_range = paginator.page_range
        context['page_range'] = page_range
        return context


class ProductView(DetailView):
    model = Item
    template_name = 'product.html'
