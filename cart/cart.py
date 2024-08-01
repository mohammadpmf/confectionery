from django.contrib import messages
from confectionery.models import Product
from django.utils.translation import gettext as _


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session # خود جنگو سشن رو میفرسته همراه با رکوئست. ما هم تو هر نمونه از کلاس خودمون ذخیره میکنیم که داشته باشیمش همه جا و هر بار هی ننویسیم self.request.session. جداگانه تو self.session ذخیره اش میکنیم که راحت دسترسی داشته باشیم بهش
        cart = self.session.get('cart') # اول میبینیم که از قبل طرف داخل سشنش کارتی ساخته که پر شده باشه یا نه. اگه باشه که ایف اجرا نمیشه. اگه نباشه یه سبد خرید خالی میسازیم براش
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
        # پس وقتی ما یه نمونه از کارت رو میسازیم، داخلش یه متغیری به اسم کارت وجود داره. که یه
        # دیکشنری پایتونی هست و ما بهش دسترسی داریم. در ادامه، کلیدهای این دیکشنری رو برابر
        # میذاریم با آی دی محصولات. و مقادیر اون کلید ها رو میذاریم تعداد انتخاب شده و خود آبجکت
        # اون محصول. وقتی دیکشنری باشن، پس آیتم تکراری توش نداریم. خلاصه این که یعنی این شکلی میشه
        # self.cart={
        #     345: {
        #         'quantity': 5,
        #         'product_obj': product obj 345,
        #         'total_price': 13132132,
        #     },
        #     412: {
        #         'quantity': 2,
        #         'product_obj': product obj 412
        #         'total_price': 123144,
        #     },
        # }

    def add(self, product: Product, quantity=1, replace_current_quantity=False):
        product_id=str(product.id)
        if product_id not in self.cart: # اگه تو سبد خرید نبود که همین الان اضافه شده. پس اضافه اش میکنیم با مقدار اولیه صفر
            self.cart[product_id]={'quantity': 0}
        if replace_current_quantity: # اگر گفته شده بود که مقدار رو جایگزین کن، یعنی طرف تو صفحه سبد خرید نهایی هست و قبلا این آیتم رو اضافه کرده بود و الان مثلا گفته ۸ تا بشه. پس مقدار جدید باید جایگزین بشه.
            self.cart[product_id]['quantity'] = quantity
            messages.success(self.request, _('Product successfully updated'))
        else: # یعنی طرف تو صفحه خرید نیست. و از توی صفحه محصول گفته ۳ تا مثلا اضافه کن. پس به مقدار قبلیش اضافه میکنیم. که دفعه اول به اضافه ۰ میشه و دفعات بعدی به اضافه مقدار قبلیش
            self.cart[product_id]['quantity'] += quantity
            messages.success(self.request, _('Product successfully added to cart'))
        self.save()

    def save(self):
        self.session.modified=True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, _('Product successfully removed from cart'))
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product_obj'] = product
        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item
    
    def __len__(self):
        return len(self.cart)
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        return sum([item['quantity'] * item['product_obj'].price for item in self.cart.values()])
    
    def is_empty(self):
        return not self.cart
        if self.cart:
            return False
        return True