from django.contrib import admin


class Admin(admin.ModelAdmin):
    search_fields = ['id']

    class Media:
        css = {'all': ['/store/css/admin.css']}
        js = ['/store/js/admin.js']
