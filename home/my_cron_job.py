from django_cron import CronJobBase, Schedule
import random
import threading
from .models import TCL
from paho.mqtt import client as mqtt_client

broker_address = "192.168.1.142"
port = 2000
topic = "sensor"
username = "mqtt"
password = "123456"
import json

from django.utils import timezone

import time

class MyCronJob(CronJobBase):
    RUN_EVERY_SECS = 1   # Lịch trình chạy mỗi 5 phút

    schedule = Schedule(run_every_mins=RUN_EVERY_SECS)
    code = 'home.my_cron_job'  # Đường dẫn đến cron job

    def do(self):
        a=timezone.now()
        while True:

            try:
                
                connected = False
                def on_connect(client, userdata, flags, rc):
                        nonlocal connected
                        if rc == 0:
                            print("Connected to MQTT Broker!")
                            client.subscribe(topic)
                        
                        else:
                            print(f"Failed to connect, return code {rc}")

                def on_message(client, userdata, msg):
                        nonlocal a
                        print(f"Received {msg.payload.decode()} from {msg.topic} topic")
                        temperature = json.loads(msg.payload.decode())['temperature'] #láy dữ liệu trên cmd
                        b=timezone.now()
                        # Tạo một đối tượng Iot mới và lưu vào cơ sở dữ liệu
                        # iot_data = Iot(name="temp", value=temperature,time_created=b)
                        # iot_data.save()
                        humidity = json.loads(msg.payload.decode())['humidity']

                        # Tạo một đối tượng Iot mới và lưu vào cơ sở dữ liệu
                        # iot_datahumidity = Iot(name="humidity", value=humidity,time_created=b)
                        # iot_datahumidity.save()
                        light = json.loads(msg.payload.decode())['light']

                        # Tạo một đối tượng Iot mới và lưu vào cơ sở dữ liệu
                        # iot_datalight = Iot(name="light", value=light,time_created=b)
                        # iot_datalight.save()

                        tcl= TCL(temp=temperature,light=light,hum=humidity,time_created=b)
                        tcl.save()

                        a=timezone.now()
                        time.sleep(30)
                        client.loop_stop()
                    # Thiết lập kết nối MQTT
                client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION1)
                client.username_pw_set(username, password)
                client.on_connect = on_connect #gọi hàm để khởi tạo kết nối mqtt
                client.on_message = on_message # gọi hàm lấy giá trị trường mqtt

                client.connect(broker_address, port)
                client.loop_start() 
                client.join()
            except Exception:
                time.sleep(30)
                print('loi')

                
           



