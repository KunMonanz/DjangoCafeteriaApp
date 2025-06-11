from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Promotion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    discount_percentage = models.DecimalField(max_digits=5, 
                                              decimal_places=2,
                                              validators=[
                                                  MinValueValidator(0),
                                                  MaxValueValidator(100)
                                              ]) 
    
    def __str__(self):
        return f"{self.title}({self.discount_percentage}% discount)"


class PromotionItem(models.Model):
    promotion = models.ForeignKey(Promotion,
                                  on_delete=models.SET_NULL,
                                  null=True, 
                                  blank=True)

    class Meta:
        abstract = True
    
    def discounted_price(self):
        if self.promotion:
            self.price * (1-(self.promotion.discount_percentage/100))
        return self.price


class PriceItem(models.Model):
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    price = models.DecimalField(max_digits=6, 
                            decimal_places=2)

    class Meta:
        abstract = True

    def total_price(self):
        return self.menu_item.price * self.quantity


class Profile(models.Model):
    USER_TYPES = (
        ('customer', 'CUSTOMER'),
        ('staff', 'STAFF')
        )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)


class MenuItem(PromotionItem):
    CATEGORY_CHOICES = (
        ('food', 'FOOD'),
        ('drink', 'DRINK')
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=6,
                                choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6,
                                decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price} naira"


class Order(models.Model):
    customer = models.ForeignKey(User,
                                 on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.item.all())


class OrderItem(PriceItem):
    order = models.ForeignKey('Order',
                              related_name='items',
                              on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"


class Cart(models.Model):
    customer = models.OneToOneField(User,
                                    on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.customer.username}"


class CartItem(PriceItem):
    cart = models.ForeignKey('Cart', 
                             related_name='items',
                             on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in cart of {self.cart.customer.username}"








