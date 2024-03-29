from django.contrib import admin


class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['document', 'id']

    class Media:
        css = {'all': ['/store/css/admin.css']}
        js = ['/store/js/admin.js']
