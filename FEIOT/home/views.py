from django.shortcuts import render

# Create your views here.
def DataSensor(request):
    return render(request,'DataSensor.html')
def History(request):
    return render(request,'History.html')
def DashBoard(request):
    return render(request,'DashBoard.html')
def Admin(request):
    return render(request,'Admin.html')