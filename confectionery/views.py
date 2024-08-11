from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Prefetch, Avg, Count, Case, When, FloatField, StdDev, Variance
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.core.paginator import Paginator

from .models import Chef, Favorite, Product, ProductCustomUserComment, ProductAnanymousUserComment
from .forms import NewsLetterForm, ProductCustomUserCommentForm, ProductAnanymousUserCommentForm, SuggestionsCriticsForm

PRODUCTS_PER_PAGE = 6


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
        context['top_comments'] = ProductCustomUserComment.objects.filter(is_approved=True, dont_show_my_name=False).select_related('product', 'author__profile_picture').order_by('-stars', '-datetime_modified', '-id')[:5]
        context['chefs'] = Chef.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        if 'newsletter_sub' in request.POST:
            new_subscription=NewsLetterForm(request.POST)
            if new_subscription.is_valid():
                new_subscription.save()
                messages.success(request, _("Your email successfully added to our database! You will be noticed from all news ASAP!"))
            else:
                messages.error(request, new_subscription.errors)
        next_page = request.POST.get("next_page")
        if not next_page:
            next_page = 'homepage'
        return redirect(next_page)
        # این کامنت های طولانی که پایین نوشتم رو اول گذاشتم چون داخل یه کلاس دیگه نوشته بودم. بعد گفتم
        # بیاد به صفحه اول خوبه. به خاطر همین آوردمش اینجا. اما چون بحث جالبی بود کدها رو گذاشتم باشه
        # و به همون صورت آوردمش اینجا. فقط این که اول تو پروداکت دیتیل خاص از یه محصول نوشته بودم
        # موقعی که بهش ارجاع دادم تو کامنت ها یادم باشه که تو کلاس ProductDetail بوده و اول متد post
        # از این کلاس

        # در غیر این صورت یا لایک کرده یا نظر داده که کارهای زیر رو انجام دادم. البته برای اینا هم بهتر بود
        # به نظرم همین شکلی استفاده میکردم. ولی قبلا نوشته بودم. به هر حال تجربه شد دیگه. میتونیم با بررسی
        # با استفاده از اپراتور این ببینیم که کودوم فرم از سمت اچ تی ام ال ارسال شده. اگه اکشن ها شون
        # متفاوت باشن که خب تابع های جدا رو بررسی میکنیم. اما اگه اکشن های یکسانی داشته باشن یا 
        # اکشن نداشته باشن که صفحه ای که لودشون کرده دوباره بررسیشون کنه، این شکلی میشه با ایف بررسی کرد
        # که کودوم یکی صداش کرده بوده. البته کسی که سوال کرده بود تو استک اورفلو جذاب تر بود و اون میخواست
        # آنسابسکرایب هم بذاره. در واقع تو یه فرم ۲ تا دکمه سابمیت داشت که برای منم هر وقت لازم شد میتونم
        # ازش کمک بگیرم. اما برای همین مسئله هم خیلی کمکم کرد. دیگه کدهای قبلی رو که پایین نوشته بودم
        # عوض نمیکنم. روش من این بود که همیشه یه اینپوت هیدن تعریف میکردم بعد این ور میگرفتم ببینم اگه
        # اون اینپوت مقدار داره یه سری کارها رو بکنم و اگه نداره کار متفاوت. اما این روش جدید حرفه ای تره
        # https://stackoverflow.com/questions/866272/how-can-i-build-multiple-submit-buttons-django-form
        # این هم لینک استک اورفلویی که کمک کرد حل بشه مسئله.


class CategoryList(generic.ListView):
    def get(self, request, *args, **kwargs):
        category = self.kwargs['category']
        sort_by = self.request.GET.get('sort-by')
        queryset = Product.objects.filter(product_type=category).annotate(
            average_stars=Avg(
            Case(
                When(comments__is_approved=True, then='comments__stars'),
                    output_field=FloatField()
                )
            )
        )
        if sort_by in [None, 'recommendation']:
            sort_by='recommendation' # اگه انتخاب نکرده بود خودم میذارم بر اساس پیشنهاد خریداران.
            queryset=queryset.order_by('-average_stars', '-id')
            # همیشه بر اساس آی دی هم مرتب میکنم که تو پیجینیشن محصول تکراری نشون نده.
            # در واقع بر اساس یه فیلد یونیک باید این کار رو میکردم که پیشنهاد خود کوپایلت
            # هم آی دی بود و به خوبی جواب میده. چون یکتاست.
        elif sort_by=='newest':
            queryset=queryset.order_by('-id')
        elif sort_by=='cheapest':
            queryset=queryset.order_by('price_toman', '-id')
        elif sort_by=='most_expensive':
            queryset=queryset.order_by('-price_toman', '-id')
        elif sort_by=='more_durable':
            queryset=queryset.order_by('-expiration_days', '-id')
        elif sort_by=='fastest':
            queryset=queryset.order_by('preparation_time', '-id')
        paginator = Paginator(queryset, PRODUCTS_PER_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            # دیگه لازم نیست خود پروداکتز رو بفرستم. یعنی میفرستادم تو هر صفحه دوباره همه
            # رو کامل نشون میداد. از کوپایلت پرسیدم گفت که باید روی پیج آبج حلقه بزنم.
            'active_page': sort_by,
            'page_obj': page_obj,
            }
        return render(request, 'category.html', context)


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
        # ).annotate(average_stars=Avg('comments__stars'), count_stars=Count('comments__stars'))
        # این میانگین همه کامنت های کاستوم یوزرها رو میداد. حالا اگه بخوایم فقط میانگین کامنت های
        # تایید شده کاستوم یوزر ها رو بده، این کار رو میکنیم. (از کوپایلت مایکروسافت پرسیدم.)
        ).annotate(
            average_stars=Avg(
            Case(
                When(comments__is_approved=True, then='comments__stars'),
                    output_field=FloatField()
                )
            ),
            count_stars=Count(
            Case(
                When(comments__is_approved=True, then='comments__stars'),
                    output_field=FloatField()
                )
            ),
            std_dev=StdDev(
            Case(
                When(comments__is_approved=True, then='comments__stars'),
                    output_field=FloatField()
                )
            )
        )
        return query_set
        
    def get_context_data(self, **kwargs):
        product = kwargs.get('object') # یا product = self.get_object()
        user = self.request.user
        context = super().get_context_data(**kwargs)
        if user.is_authenticated:
            c = ProductCustomUserComment.objects.filter(product=product, author=user).first()
            if c:
                form = ProductCustomUserCommentForm(instance=c)
            else:
                form = ProductCustomUserCommentForm()
        else:
            form = ProductAnanymousUserCommentForm()
        context['form'] = form
        context['comments'] = ProductCustomUserComment.objects.select_related('author').\
            filter(is_approved=True, product=product).order_by('-datetime_modified')
        context['anonymous_comments'] = ProductAnanymousUserComment.objects.filter(is_approved=True, product=product).order_by('-datetime_created')
        if user.is_authenticated:
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
            c = ProductCustomUserComment.objects.filter(product=product, author=self.request.user).first()
            if c:
                comment_form = ProductCustomUserCommentForm(request.POST, instance=c)
            else:
                comment_form = ProductCustomUserCommentForm(request.POST)
        else:
            comment_form = ProductAnanymousUserCommentForm(request.POST)
        if comment_form.is_valid():
            cleaned_data = comment_form.cleaned_data
        else:
            messages.error(request, comment_form.errors)
            return super().get(request, *args, **kwargs)
        if user.is_authenticated:
            if c:
                comment_form.save()
                messages.success(request, _("Your comment updated successfully."))
            else: # این رو کمی بهتر هم میشد نوشت و با همون حالت کامیت= فالس ذخیره کرد و کارهای دیگه. اما انجام ندادم این هم یه روش هست. گفتم زودتر پروژه رو کامل کنم ایشالله پروژه های بعدی بهتر بنویسم. این هم خیلی روش خوبیه.
                cleaned_data.update({
                    'product_id': product.pk,
                    'author': user,
                })
                ProductCustomUserComment.objects.create(**cleaned_data)
                messages.success(request, _("Your comment recieved successfully."))
        else:
            cleaned_data.update({
                'product_id': product.pk,
            })
            messages.success(request, _("Your comment recieved successfully. But as you are not a member of this site, it will be shown after confirmation!"))
            ProductAnanymousUserComment.objects.create(**cleaned_data)
        return super().get(request, *args, **kwargs)


class FavoriteList(LoginRequiredMixin, generic.ListView):
    def get(self, request, *args, **kwargs):
        # روش اول
        # user = request.user
        # favorites = Favorite.objects.filter(user=user).select_related('product').order_by('-id')
        # products = []
        # for product in favorites:
        #     products.append(product.product)
        # return products
        user = request.user
        sort_by = self.request.GET.get('sort-by')
        queryset = Product.objects.filter(favorited_users__user=user).annotate(
            average_stars=Avg(
            Case(
                When(comments__is_approved=True, then='comments__stars'),
                    output_field=FloatField()
                )
            )
        )
        if sort_by in [None, 'recommendation']:
            sort_by='recommendation' # اگه انتخاب نکرده بود خودم میذارم بر اساس پیشنهاد خریداران.
            queryset=queryset.order_by('-average_stars', '-id')
        elif sort_by=='newest':
            queryset=queryset.order_by('-id')
        elif sort_by=='cheapest':
            queryset=queryset.order_by('price_toman', '-id')
        elif sort_by=='most_expensive':
            queryset=queryset.order_by('-price_toman', '-id')
        elif sort_by=='more_durable':
            queryset=queryset.order_by('-expiration_days', '-id')
        elif sort_by=='fastest':
            queryset=queryset.order_by('preparation_time', '-id')
        paginator = Paginator(queryset, PRODUCTS_PER_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            'active_page': sort_by,
            'page_obj': page_obj,
            }
        return render(request, 'category.html', context)


class ProductList(generic.ListView):
    def get(self, request, *args, **kwargs):
        sort_by = self.request.GET.get('sort-by')
        queryset = Product.objects.annotate(
            average_stars=Avg(
            Case(
                When(comments__is_approved=True, then='comments__stars'),
                    output_field=FloatField()
                )
            )
        )
        if sort_by in [None, 'recommendation']:
            sort_by='recommendation' # اگه انتخاب نکرده بود خودم میذارم بر اساس پیشنهاد خریداران.
            queryset=queryset.order_by('-average_stars', '-id')
        elif sort_by=='newest':
            queryset=queryset.order_by('-id')
        elif sort_by=='cheapest':
            queryset=queryset.order_by('price_toman', '-id')
        elif sort_by=='most_expensive':
            queryset=queryset.order_by('-price_toman', '-id')
        elif sort_by=='more_durable':
            queryset=queryset.order_by('-expiration_days', '-id')
        elif sort_by=='fastest':
            queryset=queryset.order_by('preparation_time', '-id')
        paginator = Paginator(queryset, PRODUCTS_PER_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            'active_page': sort_by,
            'page_obj': page_obj,
            }
        return render(request, 'category.html', context)


class AboutUs(generic.TemplateView):
    template_name = 'about_us.html'


class AboutMe(generic.TemplateView):
    template_name = 'about_me.html'


class ContactUs(generic.TemplateView):
    template_name = 'contact_us.html'

    def post(self, request, *args, **kwargs):
        new_suggestion_or_something_else = SuggestionsCriticsForm(request.POST)
        if new_suggestion_or_something_else.is_valid():
            new_suggestion_or_something_else.save()
            messages.success(request, _("Your message has been recieved successfully! If it needs a response, we'll contact you ASAP!"))
        else:
            messages.error(request, new_suggestion_or_something_else.errors)
        return super().get(request, *args, **kwargs)


class ChefList(generic.ListView):
    template_name = 'chefs.html'
    model = Chef
    context_object_name = 'chefs'
