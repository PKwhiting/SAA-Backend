from django.contrib import admin
from .car import Car
from .models import Bid
from .models import SavedVehicle
from .models import VehicleFilter
# from .user import User
from django.contrib.auth.models import User

# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#         'username', 'email', 'first_name', 'last_name', 'is_staff',
#         )

#     fieldsets = (
#         (None, {
#             'fields': ('username', 'password')
#         }),
#         ('Personal info', {
#             'fields': ('first_name', 'last_name', 'email', 'phone_number')
#         }),
#         ('Permissions', {
#             'fields': (
#                 'is_active', 'is_staff', 'is_superuser',
#                 'groups', 'user_permissions'
#                 )
#         }),
#         ('Important dates', {
#             'fields': ('last_login', 'date_joined')
#         }),
#     )

#     add_fieldsets = (
#         (None, {
#             'fields': ('username', 'password1', 'password2')
#         }),
#         ('Personal info', {
#             'fields': ('first_name', 'last_name', 'email')
#         }),
#         ('Permissions', {
#             'fields': (
#                 'is_active', 'is_staff', 'is_superuser',
#                 'groups', 'user_permissions'
#                 )
#         }),
#         ('Important dates', {
#             'fields': ('last_login', 'date_joined')
#         }),
#     )

admin.site.register(Car)
admin.site.register(Bid)
admin.site.register(SavedVehicle)
admin.site.register(VehicleFilter)
# admin.site.register(User, UserAdmin)