from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Text)
admin.site.register(Link)
admin.site.register(File)
