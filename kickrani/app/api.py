from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Kickrani
from .serializer import KickraniSerializer
from .serializer import DailyChartSerializer
from .serializer import AnnualChartSerializer
from .serializer import RiderSerializer
from .serializer import ViolationSerializer
from datetime import datetime
from django.utils.dateformat import DateFormat
import cv2
from django.db.models import Count
import boto3
import json

with open('./secrets.json')as json_file:
    json_data = json.load(json_file)

aws = json_data["AWS"]

@api_view(['GET'])
def kickraniList(request):
    kickranis = Kickrani.objects.all()
    serializer = KickraniSerializer(kickranis, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def dailyChart(request):
    # now = DateFormat(datetime.now()).format('Ymd')
    # now=now[:4]+'-'+now[4:6]+'-'+now[6:8] #2021-05-21 형태로 만들기 위한 코드
    # chart = Kickrani.objects.filter(brand__contains=now)
    chart = Kickrani.objects.values('brand').annotate(num_brand=Count('brand')).order_by('brand')
    serializer = DailyChartSerializer(chart, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def annualChart(request):
    now = DateFormat(datetime.now()).format('Ymd')
    now=now[:4] #2021-05-21 형태로 만들기 위한 코드
    print(now)
    chart = Kickrani.objects.filter(datetime__contains=now)
    serializer = AnnualChartSerializer(chart, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def kickraniCreate(request):
    serializer = KickraniSerializer(data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def RiderCreate(request):
    serializer = RiderSerializer(data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def ViolationCreate(request):
    serializer = ViolationSerializer(data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)

#datetim형태 이미지저장명으로 바꾸
def dateHandler(date):
    date = date[:22].replace('-', '')
    date = date.replace(':', '')
    date = date.replace('.', '')
    date = date.replace(' ', '')
    return date

def kickraniDB(request,origin_frame):

    imageName=dateHandler(request["datetime"])
    cv2.imwrite('image/'+imageName + '.png', origin_frame)

    file_name='image/'+imageName + '.png'
    bucket=aws["bucket"]
    key='image/'+imageName + '.png'

    s3=boto3.client(
        's3',
        aws_access_key_id=aws["aws_access_key_id"],
        aws_secret_access_key=aws["aws_secret_access_key"],
    )
    s3.upload_file(
        file_name,
        bucket,
        key,
        ExtraArgs={
            "ContentType": 'image/png',
        }
    )

    request['image']=imageName
    request['location'] = "강남역"  #장소 임의로 추가

    print(imageName+'.png'+' 파일이 저장되었습니다')

    #violation 1:2인이상, 2: 헬멧미착용, 3:2인이상 및 헬멧 미착용 4:
    if request["person"]>1:
        if request["person"]!=request["helmet"]:
            request["violation"] = 3
        else:
            request["violation"] = 1
    else:
        if request["helmet"]!=1:
            request["violation"] = 2
        # else:
        #     print("정상적인 사용자 입니다")
        #     return Response(serializer.data)
    serializer = KickraniSerializer(data=request) #data=request.data
    if(serializer.is_valid()):
        print('table1 DB 저장 완료')
        serializer.save()
    else:
        print('table1 DB false')
    return Response(serializer.data)

def RiderDB(request):
    serializer = RiderSerializer(data=request)
    if(serializer.is_valid()):
        print('table2 DB 저장 완료')
        serializer.save()
    else:
        print('table2 DB false')
    return Response(serializer.data)

def ViolationDB(request):
    serializer = ViolationSerializer(data=request)
    if(serializer.is_valid()):
        print('table3 DB 저장 완료')
        serializer.save()
    else:
        print('table3 DB false')
    return Response(serializer.data)