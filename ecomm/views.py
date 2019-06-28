from django.views import generic

from ecomm.models import Product


class IndexView(generic.ListView):
    template_name = "ecomm/index.html"
    context_object_name = "product_list"

    def get_queryset(self):
        return Product.objects.all()


class DetailView(generic.DetailView):
    template_name = "ecomm/detail.html"
    model = Product

