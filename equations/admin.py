from django.contrib import admin
from .models import Mathematician, Equation

#here we specify data for admin interface
# django lets us use an interface, useful for things like manual db populating

# Register your models here.
admin.site.register(Mathematician)
admin.site.register(Equation)
