from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Promotion, MenuItem, Order, Profile

admin.site.unregister(Group)
admin.site.unregister(User)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
	list_display = ['name', 'category', 'price', 'available', 'promotion']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
	list_display = ['title', 'description', 'discount_percentage']
 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created_at', 'is_completed']


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']

