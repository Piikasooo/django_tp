from __future__ import  unicode_literals

from django.contrib import admin
from pract.models import Category, Petition, voted

# Register your models here.
admin.site.register(Category)
admin.site.register(Petition)
admin.site.register(voted)