from django.contrib import admin

# Register your models here.
from .models import Instrument
from .models import Rule
from .models import Archive
from .models import Period

admin.site.register(Instrument)
admin.site.register(Rule)
admin.site.register(Archive)
admin.site.register(Period)