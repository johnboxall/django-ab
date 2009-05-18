from django.contrib import admin
from ab.models import Experiment, Test


class TestInline(admin.TabularInline):
    model = Test

class ExperimentAdmin(admin.ModelAdmin):
    inlines = (TestInline,)
    
admin.site.register(Experiment, ExperimentAdmin)
