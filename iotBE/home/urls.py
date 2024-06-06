from django.urls import path
from .views import HelloWorld,getvalue,getdata,getStatusDeviceFinal,getHLTFinal
urlpatterns = [
    #điều khiển thiết bị
    path('device',HelloWorld.as_view()),
    path('getStatusDeviceFinal',getStatusDeviceFinal.as_view()),
    path('getHLTFinal',getHLTFinal.as_view()),

    #lấy giá trị của 3 cái bao gồm ánh sáng, nhiệt độ , độ ẩm
    path('getvalue',getvalue.as_view()),
    # get trạng thái thái tắt bật có khoảng thời gian
    path('getdata',getdata.as_view())
]
