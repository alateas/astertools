from django.contrib import admin
from models import Fax,FaxDev,FaxDevPermission
from django.core.exceptions import ObjectDoesNotExist

class FaxAdmin(admin.ModelAdmin):
    list_display = ('id', 'pdf_link', 'sender_number', 'sender_name', 'description' , 'fax_dev', 'date')
    date_hierarchy = 'date'

    def queryset(self, request):
        qs = super(FaxAdmin, self).queryset(request)
        user = request.user
        if user.is_superuser:
            return qs

        alowed_fax_devs = []
        for fax_dev in FaxDev.objects.all():
            if fax_dev.has_access(user):
                alowed_fax_devs.append(fax_dev)
        
        return qs.filter(fax_dev__in=alowed_fax_devs)

class FaxDevAdmin(admin.ModelAdmin):
    list_display = ('title', 'dev_name', 'email')

class FaxDevPermissionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Fax, FaxAdmin)
admin.site.register(FaxDev, FaxDevAdmin)
admin.site.register(FaxDevPermission, FaxDevPermissionAdmin)
