from django.contrib import admin

from .models import Breed
from .models import Dog

admin.site.register(Dog)
admin.site.register(Breed)
