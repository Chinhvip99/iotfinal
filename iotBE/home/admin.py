from django.contrib import admin
from .models import Iot

class IotAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'time_created')
#đăng ký mô hình Iot với trang quản trị Django, và sử dụng lớp IotAdmin để tùy chỉnh giao diện quản trị cho mô hình đó.
admin.site.register(Iot, IotAdmin)
