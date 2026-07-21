from django.db.models import Q
from django.db.models.sql import query
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Category


class ProductListView(ListView):
    template_name = 'shop/product-list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        query_params.pop('category', None)
        context['query_string'] = query_params.urlencode()

        context["product"] = Product.objects.filter(is_available=True)
        context['category'] = Category.objects.filter(parent=None, is_active=True)
        context['total_items'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)

        if search_q := self.request.GET.get('q'):
            queryset = queryset.filter(
                Q(name__icontains=search_q) |
                Q(description__icontains=search_q) |
                Q(short_description__icontains=search_q) |
                Q(category__name__icontains=search_q)
            )

        if min_price := self.request.GET.get('min_price'):
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_price := self.request.GET.get('max_price'):
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        if self.request.GET.get('only_available'):
            queryset = queryset.filter(stock__gt=0)

        if category_slug := self.request.GET.get('category'):
            category = Category.objects.filter(slug=category_slug, is_active=True).first()
            if category:
                category_ids = category.get_descendant_ids()
                queryset = queryset.filter(category_id__in=category_ids)

        sort = self.request.GET.get('sort', 'all_product')

        if sort == 'bestseller':
            queryset = queryset.filter(is_bestseller=True)
        elif sort == 'cheapest':
            queryset = queryset.order_by('price')
        elif sort == 'expensive':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')

        return queryset


class ProductDetailView(DetailView):
    template_name = 'shop/product-detail.html'
    queryset = Product.objects.filter(is_available=True)
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['breadcrumb_categories'] = product.category.get_ancestors()
        return context


class CategoryDetailView(ListView):
    model = Product
    template_name = "shop/product-list.html"
    paginate_by = 20

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs["pk"])

        queryset =  Product.objects.filter(
            category_id__in=category.get_descendant_ids(),
            is_available=True,
        )

        if search_q := self.request.GET.get('q'):
            queryset = queryset.filter(
                Q(name__icontains=search_q) |
                Q(description__icontains=search_q) |
                Q(short_description__icontains=search_q) |
                Q(category__name__icontains=search_q)
            )

        if min_price := self.request.GET.get('min_price'):
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_price := self.request.GET.get('max_price'):
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        if self.request.GET.get('only_available'):
            queryset = queryset.filter(stock__gt=0)

        if category_slug := self.request.GET.get('category'):
            category = Category.objects.filter(slug=category_slug, is_active=True).first()
            if category:
                category_ids = category.get_descendant_ids()
                queryset = queryset.filter(category_id__in=category_ids)

        sort = self.request.GET.get('sort', 'all_product')

        if sort == 'bestseller':
            queryset = queryset.filter(is_bestseller=True)
        elif sort == 'cheapest':
            queryset = queryset.order_by('price')
        elif sort == 'expensive':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query_params = self.request.GET.copy()
        query_params.pop("page", None)

        context["query_string"] = query_params.urlencode()
        context["total_items"] = self.object_list.count()

        return context
