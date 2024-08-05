from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Prefetch, Avg, Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _

from .models import Favorite, Product, ProductCustomUserComment, ProductAnanymousUserComment
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
        return super().get_queryset().filter(product_type=category).\
        annotate(average_stars=Avg('comments__stars')).order_by('-average_stars')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context
    
    def get(self, request, *args, **kwargs):
        category = self.kwargs['category']
        sort_by = self.request.GET.get('sort-by')
        queryset = Product.objects.filter(product_type=category).annotate(average_stars=Avg('comments__stars'))
        if sort_by in [None, 'recommendation']:
            queryset=queryset.order_by('-average_stars')
        elif sort_by=='newest':
            queryset=queryset.order_by('-id')
        elif sort_by=='cheapest':
            queryset=queryset.order_by('price_toman')
        elif sort_by=='most_expensive':
            queryset=queryset.order_by('-price_toman')
        elif sort_by=='more_durable':
            queryset=queryset.order_by('-expiration_days')
        elif sort_by=='fastest':
            queryset=queryset.order_by('preparation_time')
        context = {'products': queryset}
        return render(request, 'category.html', context)
        return super().get(request, *args, **kwargs)


class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        query_set = super().get_queryset().prefetch_related(
            'images',
            Prefetch(
                'anonymous_comments',
                queryset=ProductAnanymousUserComment.objects.filter(is_approved=True)
            ),
            Prefetch(
                'comments',
                queryset=ProductCustomUserComment.objects.select_related('author').filter(is_approved=True)
            )
        ).annotate(average_stars=Avg('comments__stars'), count_stars=Count('comments__stars'))
        return query_set
        
    def get_context_data(self, **kwargs):
        product = kwargs.get('object') # یا product = self.get_object()
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            form = ProductCustomUserCommentForm()
        else:
            form = ProductAnanymousUserCommentForm()
        context['form'] = form
        context['comments'] = ProductCustomUserComment.objects.select_related('author').\
            filter(is_approved=True, product=product).order_by('-datetime_modified')
        context['anonymous_comments'] = ProductAnanymousUserComment.objects.filter(is_approved=True, product=product).order_by('-datetime_created')
        context['liked'] = True if Favorite.objects.filter(product=product, user=self.request.user) else False
        return context
    
    def post(self, request, *args, **kwargs):
        user = request.user
        product = self.get_object()
        like_situation = request.POST.get('like_situation')
        if like_situation in ['0', '1']: # یعنی طرف رو دکمه لایک زده و کامنت نذاشته
            if like_situation=='1':
                Favorite.objects.create(product=product, user=user)
                messages.success(request, _("%s successfully added to your favorites." %product.title))
            else:
                temp = Favorite.objects.filter(product=product, user=user)
                temp.delete()
                messages.success(request, _("%s successfully removed from your favorites." %product.title))
            return redirect('product_detail', product.pk)
        if user.is_authenticated:
            comment_form = ProductCustomUserCommentForm(request.POST)
        else:
            comment_form = ProductAnanymousUserCommentForm(request.POST)
        if comment_form.is_valid():
            cleaned_data = comment_form.cleaned_data
        else:
            messages.error(request, comment_form.errors)
            return super().get(request, *args, **kwargs)
        if user.is_authenticated:
            cleaned_data.update({
                'product_id': product.pk,
                'author': user,
            })
            ProductCustomUserComment.objects.create(**cleaned_data)
            messages.success(request, "پیغام شما با موفقیت ثبت شد.")
        else:
            cleaned_data.update({
                'product_id': product.pk,
            })
            messages.success(request, "پیغام شما با موفقیت ارسال شد. اما چون عضو سایت نیستید، پس از تایید مدیریت نمایش داده خواهد شد.")
            ProductAnanymousUserComment.objects.create(**cleaned_data)
        return super().get(request, *args, **kwargs)


class FavoriteList(LoginRequiredMixin, generic.ListView):
    model = Favorite # روش ۱
    # model = Product # روش ۲
    template_name = 'category.html'
    context_object_name = 'products'
    paginate_by=10

    # روش ۱
    def get_queryset(self):
        user = self.request.user
        favorites = Favorite.objects.filter(user=user).select_related('product')
        products = []
        for product in favorites:
            products.append(product.product)
        return products

    # روش ۲
    # def get_queryset(self):
    #     user = self.request.user
    #     products = Product.objects.filter(favorited_users__user=user)
    #     return products


class ProductList(generic.ListView):
    model = Product
    template_name = 'category.html'
    context_object_name = 'products'
    paginate_by=10
    queryset = Product.objects.order_by('-id').annotate(average_stars=Avg('comments__stars')).order_by('-average_stars', '-id')
