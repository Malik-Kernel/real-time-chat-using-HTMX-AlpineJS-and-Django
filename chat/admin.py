from django.contrib import admin
from chat.models import *

admin.site.register(UserProfile)
admin.site.register(Rooms)
admin.site.register(Message)
