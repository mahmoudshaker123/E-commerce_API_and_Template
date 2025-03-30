from django.conf import settings
from decimal import Decimal
from store.models import Product
from coupons.models import Coupon

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id=self.session.get('coupon_id')



    def add(self, product, quantity=1, update_quantity=False):
        """ إضافة المنتج إلى السلة """
        product_id = str(product.id)  
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}  # تخزين كـ str

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """ حفظ البيانات بعد تحويلها إلى JSON-friendly format """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """ حذف منتج من السلة """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """ جلب المنتجات وإعداد بياناتها """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product  

        for item in cart.values():
            item['price'] = Decimal(item['price'])  # تحويل السعر إلى Decimal
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ إرجاع العدد الإجمالي للعناصر """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """ حساب الإجمالي بعد التحويل إلى Decimal """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass

        return None
    
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100))*self.get_total_price()
        return Decimal(0)
    
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()




    def clear(self):
        """ مسح محتويات السلة """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
