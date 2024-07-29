from django.shortcuts import render
from django.views import generic
from django.db.models import Prefetch

from .models import Product, ProductCustomUserComment


class HomePage(generic.TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cakes']=[]
        context['pastries']=[]
        context['breads']=[]
        total = 0
        for product in Product.objects.order_by('id'):
            if total==18:
                break
            if product.product_type=='cake' and len(context['cakes'])<6:
                context['cakes'].append(product)
                total+=1
            elif product.product_type=='pastry' and len(context['pastries'])<6:
                context['pastries'].append(product)
                total+=1
            elif product.product_type=='bread' and len(context['breads'])<6:
                context['breads'].append(product)
                total+=1
        # context['cakes'] = Product.objects.filter(product_type='cake').order_by('id')[:6]
        # context['pastries'] = Product.objects.filter(product_type='pastry').order_by('id')[:6]
        # context['breads'] = Product.objects.filter(product_type='bread').order_by('id')[:6]
        return context


class CategoryList(generic.ListView):
    model = Product
    template_name = 'category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = self.kwargs['category']
        return super().get_queryset().filter(product_type=category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context


class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        query_set = super().get_queryset().prefetch_related('images', 'anonymous_comments',
            Prefetch(
                'comments',
                queryset=ProductCustomUserComment.objects.select_related('author')
            )
        )
        return query_set
        
    def get_context_data(self, **kwargs):
        # if self.request.user.is_authenticated برای فرم ها گذاشتم. اگه انانیموس بود باید یه فرم ارسال بشه تو صفحه. اگه لاگین بود یه فرم دیگه
        context = super().get_context_data(**kwargs)
        return context
