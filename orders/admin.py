from django.contrib import admin
from .models import Order , OrderItem
import csv
import datetime
from django.http import HttpResponse

# Register your models here.

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename="{opts.verbose_name}.csv"'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition

    # إنشاء كاتب CSV
    writer = csv.writer(response)

    # اختيار الحقول الفعلية فقط (بدون العلاقات مثل OneToOneRel و ManyToOneRel)
    fields = [field for field in opts.get_fields() if field.concrete and hasattr(field, 'verbose_name')]

    # كتابة رأس الجدول
    writer.writerow([field.verbose_name for field in fields])

    # كتابة البيانات
    for obj in queryset:
        row = []
        for field in fields:
            value = getattr(obj, field.name, "")
            if isinstance(value, datetime.date):
                value = value.strftime('%Y-%m-%d')
            row.append(value)
        writer.writerow(row)

    return response


export_to_csv.short_description = "Export to CSV"

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'first_name', 'last_name', 'email', 'created_at', 'paid']
    inlines = [OrderItemAdmin]
    actions = [export_to_csv]


    