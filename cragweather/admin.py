from django.contrib import admin
from .models import locationModel, cragModel, userAccountModel, weatherModel
# Register your models here.

admin.site.register(locationModel)
admin.site.register(cragModel)
admin.site.register(userAccountModel)
admin.site.register(weatherModel)