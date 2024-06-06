from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import paho.mqtt.publish as publish
from .models import Iot,TCL
from django.db.models import Q
from .serializer import TCLSerializer,IOTSerializer
from django.db.models import Count
from collections import defaultdict
import datetime
from django.utils import timezone
import pytz
class HelloWorld(APIView):
    def get(self, request):
        value= request.GET.get('status')# trang thái muốn tắt hawocj bật thiết bị
        device= request.GET.get('device')# tên thiết bị
        # Thông tin kết nối MQTT
        mqtt_host = "172.20.10.3"
        mqtt_port = 2000
        mqtt_username = "mqtt"
        mqtt_password = "123456"
        mqtt_topic = device
        mqtt_message = value
        print(device,value)
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
            return Response({"message": "That bai"},400)
        return Response({"success": "Thành công"},200)
class getvalue(APIView):
    def get(self, request):
        sortBy= request.GET.get('sortBy',None)
        statusSort= request.GET.get('statusSort',None)
        searchKey = str(request.GET.get('searchKey',''))
        searchBy = request.GET.get('searchBy',None)
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10) 
        # Lấy danh sách các bản ghi từ model Iot và nhóm chúng theo time_created
        iot_data =  TCL.objects.all()
        # print(iot_data)
        if searchKey and searchKey!=""  and searchBy:
            if searchBy=='temp':
                iot_data =iot_data.filter(temp=searchKey)
            elif searchBy=='light':
                iot_data =iot_data.filter(light=searchKey)
            elif searchBy=='hum':
                iot_data =iot_data.filter(hum=searchKey)
            elif searchBy=='date':
                naive_datetime = datetime.datetime.strptime(searchKey, "%Y-%m-%d %H:%M:%S")
                vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
                aware_datetime = vietnam_timezone.localize(naive_datetime)
                iot_data=iot_data.filter(time_created=aware_datetime)
            else:
                try:
                    naive_datetime = datetime.datetime.strptime(searchKey, "%Y-%m-%d %H:%M:%S")
                    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
                    aware_datetime = vietnam_timezone.localize(naive_datetime)
                    iot_data =iot_data.filter(Q(temp=searchKey) | Q(light=searchKey)|Q(hum=searchKey)|Q(time_created=aware_datetime))
                except:
                    iot_data =iot_data.filter(Q(temp=searchKey) | Q(light=searchKey)|Q(hum=searchKey))

        if statusSort and sortBy:
            statusSort="-" if statusSort=='1' else "" 
            if sortBy == 'hum':
                iot_data = iot_data.order_by(statusSort+'hum')
            elif sortBy == 'temp':
                iot_data = iot_data.order_by(statusSort+'temp')
            elif sortBy == 'light':
                iot_data = iot_data.order_by(statusSort+'light')
            elif sortBy == 'date':
                iot_data = iot_data.order_by(statusSort+'time_created')
        iot_data = iot_data[int(offset): int(offset) + int(limit)]
        iotJson = TCLSerializer(iot_data,many=True)
        return Response(iotJson.data,200)
class getdata(APIView):
    def get(self, request):
        sortBy= request.GET.get('sortBy',None)
        statusSort= request.GET.get('statusSort',None)
        searchKey = str(request.GET.get('searchKey',''))
        searchBy = request.GET.get('searchBy',None)
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10) 
        # Lấy danh sách các bản ghi từ model Iot và nhóm chúng theo time_created
        iot_data =  Iot.objects.all()
        # print(iot_data)
        if searchKey and searchKey!=""  and searchBy:
            if searchBy=='name':
                iot_data =iot_data.filter(name=searchKey)
            elif searchBy=='status':
                iot_data =iot_data.filter(value=searchKey)
            elif searchBy=='date':
                naive_datetime = datetime.datetime.strptime(searchKey, "%Y-%m-%d %H:%M:%S")
                vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
                aware_datetime = vietnam_timezone.localize(naive_datetime)
                iot_data=iot_data.filter(time_created=aware_datetime)
            else:
                try:
                    naive_datetime = datetime.datetime.strptime(searchKey, "%Y-%m-%d %H:%M:%S")
                    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
                    aware_datetime = vietnam_timezone.localize(naive_datetime)
                    iot_data =iot_data.filter(Q(name=searchKey) | Q(value=searchKey)|Q(time_created=aware_datetime))
                except:
                    iot_data =iot_data.filter(Q(name=searchKey) | Q(value=searchKey))

        if statusSort and sortBy:
            statusSort="-" if statusSort=='1' else "" 
            if sortBy == 'name':
                iot_data = iot_data.order_by(statusSort+'name')
            elif sortBy == 'status':
                iot_data = iot_data.order_by(statusSort+'value')
            elif sortBy == 'date':
                iot_data = iot_data.order_by(statusSort+'time_created')
        iot_data = iot_data[int(offset): int(offset) + int(limit)]
        iotJson = IOTSerializer(iot_data,many=True)
        return Response(iotJson.data,200)

class getStatusDeviceFinal(APIView):
    def get(self,request):
        device= request.GET.get('device')
        iot = Iot.objects.filter(name=device).order_by('-id').first()
        iotJson =IOTSerializer(iot)
        return Response(iotJson.data,status=200)
class getStatusDeviceFinal(APIView):
    def get(self,request):
        device= request.GET.get('device')
        iot = Iot.objects.filter(name=device).order_by('-id').first()
        iotJson =IOTSerializer(iot)
        return Response(iotJson.data,status=200)
class getHLTFinal(APIView):
    def get(self,request):
        tcl = TCL.objects.all().order_by('-id').first()
        tclJson =TCLSerializer(tcl)
        return Response(tclJson.data,status=200)
