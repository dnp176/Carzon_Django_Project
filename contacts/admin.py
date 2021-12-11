from django.contrib import admin
from .models import Contact
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','email','car_title')
    list_display_links = ('id','first_name')
    search_fields = ('first_name','email','car_title')
    list_per_page = 15

admin.site.register(Contact,ContactAdmin)
