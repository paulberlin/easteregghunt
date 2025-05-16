from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import EggHunt
from .models import Egg
from .models import EggCompletion


class EggAdmin(admin.ModelAdmin):
  list_display = ('name', 'egghunt', 'slug', 'description')

class EggCompletionAdmin(admin.ModelAdmin):
  list_display = ('egg', 'person')

class EggHuntAdmin(admin.ModelAdmin):
  list_display = ('name', 'slug', 'description')

admin.site.register(EggHunt, EggHuntAdmin)
admin.site.register(Egg, EggAdmin)
admin.site.register(EggCompletion, EggCompletionAdmin)
admin.site.register(User)
