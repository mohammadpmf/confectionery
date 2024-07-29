from django.shortcuts import render
from django.views import generic
from django.db.models import Prefetch

from .models import Product, ProductCustomUserComment, ProductAnanymousUserComment
from .forms import ProductCustomUserCommentForm, ProductAnanymousUserCommentForm


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
        query_set = super().get_queryset().prefetch_related('images', 
            Prefetch(
                'anonymous_comments',
                queryset=ProductAnanymousUserComment.objects.filter(is_approved=True)
            ),
            Prefetch(
                'comments',
                queryset=ProductCustomUserComment.objects.select_related('author').filter(is_approved=True)
            )
        ).filter()
        return query_set
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            form = ProductCustomUserCommentForm()
        else:
            form = ProductAnanymousUserCommentForm()
        context['form']=form
        return context
    
    def post(self, request, *args, **kwargs):
        print(request) # اینجااااا نمیدونم چرا نمینویسه چیزی.
        return super().get(request, *args, **kwargs)
