from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(DxRequest)
admin.site.register(Diagnostic)

# Register your models here.
