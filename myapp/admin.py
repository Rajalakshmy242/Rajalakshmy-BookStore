from django.contrib import admin
from .models import *

from .models import UserOTP

admin.site.register(UserOTP)

admin.site.register(Student)
admin.site.register(UserProfile)

admin.site.register(Category)
admin.site.register(Book)

admin.site.register(Cart)
admin.site.register(Order)