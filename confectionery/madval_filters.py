from decimal import Decimal
from django.contrib import admin

from django.utils.translation import gettext as _


class WeightFilter(admin.SimpleListFilter):
    LESS_THAN_1 = '<1'
    BETWEEN_1_AND_1_5 = '1<=1.5'
    BETWEEN_1_5_AND_2 = '1.5<=2'
    MORE_THAN_2 = '>2'
    # MORE_THAN_2 = 'bozorg' هر چی دلم میخواد. این چیزی هست که تو یو آر ال میفرسته
    title = _('Weight in Kgs') # عنوانی که تو پنل ادمین مینویسه برای ما
    parameter_name = 'weight' # این هم اسم کوئری پارامتری هست که با متد گت توی یو آر ال میفرسته. آی دی یا هر چیزی بذاریم مهم نیست. اما بهتره منطقی باشه که وِیت منطقی هست. اما خلاصه کدی که تو متد گت کوئری ست مینویسیم اجرا میشه و این فقط اسم کوئری پارامتر هست

    def lookups(self, request, model_admin):
        return [
            (WeightFilter.LESS_THAN_1, _('Less than 1 Kg')),
            (WeightFilter.BETWEEN_1_AND_1_5, _('1 to 1.5 Kg')),
            (WeightFilter.BETWEEN_1_5_AND_2, _('1.5 to 2 Kg')),
            (WeightFilter.MORE_THAN_2, _('More than 2 Kgs')),
            # ('الکی', 'هرچیزی همین طوری الکی'), اینا تگ های لینکی هست که تو پنل ادمین برامون میسازه
        ]
    
    def queryset(self, request, queryset):
        if self.value() == WeightFilter.LESS_THAN_1:
            return queryset.filter(weight__lt=1)
        if self.value() == WeightFilter.BETWEEN_1_AND_1_5:
            return queryset.filter(weight__range=(1, Decimal(1.5)))
        if self.value() == WeightFilter.BETWEEN_1_5_AND_2:
            return queryset.filter(weight__range=(Decimal(1.5), 2))
        if self.value() == WeightFilter.MORE_THAN_2:
            return queryset.filter(weight__gt=2)


class PriceFilter(admin.SimpleListFilter):
    LESS_THAN_OR_EQUAL_TO_100 = '<100'
    BETWEEN_100_AND_200 = '100<=200'
    BETWEEN_200_AND_300 = '200<=300'
    BETWEEN_300_AND_500 = '300<=500'
    MORE_THAN_500 = '>500'
    # MORE_THAN_500 = 'geroon' هر چی دلم میخواد. این چیزی هست که تو یو آر ال میفرسته
    title = _('Price in Tomans') # عنوانی که تو پنل ادمین مینویسه برای ما
    parameter_name = _('price') # این هم اسم کوئری پارامتری هست که با متد گت توی یو آر ال میفرسته. آی دی یا هر چیزی بذاریم مهم نیست. اما بهتره منطقی باشه که پرایس منطقی هست. اما خلاصه کدی که تو متد گت کوئری ست مینویسیم اجرا میشه و این فقط اسم کوئری پارامتر هست

    def lookups(self, request, model_admin):
        return [
            (PriceFilter.LESS_THAN_OR_EQUAL_TO_100, _('Cheapest')),
            (PriceFilter.BETWEEN_100_AND_200, _('Cheap')),
            (PriceFilter.BETWEEN_200_AND_300, _('Average')),
            (PriceFilter.BETWEEN_300_AND_500, _('Expensive')),
            (PriceFilter.MORE_THAN_500, _('The most expensive')),
            # ('الکی', 'هرچیزی همین طوری الکی'), اینا تگ های لینکی هست که تو پنل ادمین برامون میسازه
        ]
    
    def queryset(self, request, queryset):
        if self.value() == PriceFilter.LESS_THAN_OR_EQUAL_TO_100:
            return queryset.filter(price_toman__lt=100000)
        if self.value() == PriceFilter.BETWEEN_100_AND_200:
            return queryset.filter(price_toman__range=(100000, 200000))
        if self.value() == PriceFilter.BETWEEN_200_AND_300:
            return queryset.filter(price_toman__range=(200000, 300000))
        if self.value() == PriceFilter.BETWEEN_300_AND_500:
            return queryset.filter(price_toman__range=(300000, 500000))
        if self.value() == PriceFilter.MORE_THAN_500:
            return queryset.filter(price_toman__gt=500000)
        return queryset
