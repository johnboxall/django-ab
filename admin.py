from django.contrib import admin
from ab.models import Experiment, Test

class TestInline(admin.TabularInline):
    model = Test

# class TestAdmin(admin.ModelAdmin):
#    list_display = ("name", "hits", "conversion",)

class ExperimentAdmin(admin.ModelAdmin):
#    list_display = ("name", "hits", "conversion",)
    inlines = (TestInline,)

    
admin.site.register(Experiment, ExperimentAdmin)
# admin.site.register(Test, TestAdmin)