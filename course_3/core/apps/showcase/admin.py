from django.contrib import admin

from .models import Breed
from .models import Dog

# Register your models here.

admin.site.register(Dog)
admin.site.register(Breed)
