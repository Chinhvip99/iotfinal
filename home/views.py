from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import paho.mqtt.publish as publish
from django.http.response import JsonResponse
from .models import Iot,TCL
from django.db.models import Q

from django.db.models import Count
from collections import defaultdict

from django.utils import timezone
class HelloWorld(APIView):
    def get(self, request):
       
        value= request.GET.get('status')# trang thái muốn tắt hawocj bật thiết bị
        device= request.GET.get('device')# tên thiết bị
        # Thông tin kết nối MQTT
        mqtt_host = "192.168.1.142"
        mqtt_port = 2000
        mqtt_username = "mqtt"
        mqtt_password = "123456"
        mqtt_topic = device
        mqtt_message = value
        # Thiết lập thông tin kết nối
        auth = {'username': mqtt_username, 'password': mqtt_password}
        # Đăng tin nhắn
        try:
            publish.single(mqtt_topic, mqtt_message, hostname=mqtt_host, port=mqtt_port, auth=auth, client_id="", keepalive=60, tls=None)
            if device!='devices/control':
                Iot(name=device,value=value,time_created=timezone.now()).save()
            else:
                Iot(name="fan",value=value,time_created=timezone.now()).save()
                Iot(name="led",value=value,time_created=timezone.now()).save()

        except:
            return Response({"message": "That bai"})
        return Response({"succs": "Thành công"})
class getvalue(APIView):
    def get(self, request):

        vle= request.GET.get('vle',None)# sắp xếp theo trường nào
        sts= request.GET.get('status',None)# nếu ;à 0 thì giamt daafn1 là tăng dần

        # Lấy danh sách các bản ghi từ model Iot và nhóm chúng theo time_created
        iot_data =  TCL.objects.all()

        # Tạo một defaultdict để lưu kết quả cuối cùng
        formatted_result=[]
        for iot in iot_data:
            formatted_result.append({"temprature":iot.temp,"humidity":iot.hum,"light":iot.light,"time_create":iot.time_created})
        if sts is not None:
            if sts=='1':
                formatted_result = sorted(formatted_result, key=lambda x: int(x[vle]))
            else:
                formatted_result = sorted(formatted_result, key=lambda x: -int(x[vle]))

        return JsonResponse(formatted_result, safe=False)
class getdata(APIView):
    def get(self, request):

        vle= request.GET.get('vle',None)
        sts= request.GET.get('status',None)

        # Lấy danh sách các bản ghi từ model Iot và nhóm chúng theo time_created
        from datetime import timedelta

        iot_dataList = Iot.objects.filter(Q(name='fan') | Q(name='led')).order_by('time_created')

        devices = []  # Danh sách các thiết bị cuối cùng
        fan_status = None
        fan_time = None
        led_status = None
        led_time = None

        for data in iot_dataList:
            if data.name == 'fan':
                if data.value == 'on':
                    if fan_status =='off':
                        fan_duration=data.time_created-fan_time
                        fan_info = {"name": "fan", "trạng thái": fan_status , "duration": fan_duration.seconds, "time":fan_time }
                        devices.append(fan_info)
                else:
                    if fan_status =='on':
                        fan_duration=data.time_created-fan_time
                        fan_info = {"name": "fan", "trạng thái": fan_status , "duration": fan_duration.seconds, "time":fan_time}
                        devices.append(fan_info)
                fan_status=data.value
                fan_time=data.time_created
            elif data.name == 'led':
                
                if data.value == 'on':
                    if led_status =='off':
                        led_duration=data.time_created-led_time
                        led_info = {"name": "led", "trạng thái": led_status , "duration": led_duration.seconds, "time":fan_time}
                        devices.append(led_info)
                else:
                    if led_status =='on':
                        led_duration=data.time_created-led_time
                        led_info = {"name": "led", "trạng thái": led_status , "duration": led_duration.seconds ,"time":fan_time}
                        devices.append(led_info)
                led_status=data.value
                led_time=data.time_created
        fan_info = {"name": "fan", "trạng thái": fan_status , "duration": (timezone.now()-fan_time).seconds, "time":fan_time}
        devices.append(fan_info)
        led_info = {"name": "led", "trạng thái": led_status , "duration":  (timezone.now()-fan_time).seconds ,"time":fan_time}
        devices.append(led_info)
        if sts=='1':
            sorted_a = sorted(devices, key=lambda x: [int(x[vle].timestamp())])
        else:
            sorted_a = sorted(devices, key=lambda x: [-int(x[vle].timestamp())])
        return Response(sorted_a)
