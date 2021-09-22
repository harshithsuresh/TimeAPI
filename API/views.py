import json
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def convert(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return str(hours)+"h:"+str(minutes)+"m:"+str(seconds)+"s"

def formatTime(time):
    return datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")

def inBetween(now, start, end):
    if start <= end:
        return start <= now < end
    else: 
        return start <= now or now < end 
        
def getShift(hour):
    if hour>=6 and hour<14:
        return "shiftA"
    elif hour>=14 and hour<20:
        return "shiftB"
    elif hour>=20 and hour<6:
        return "shiftC" 


@api_view(['POST'])
def Question1(request):
    res={
    "shiftA" :{ "production_A_count" :0, "production_B_count" :0},
    "shiftB" :{ "production_A_count" :0, "production_B_count" :0},
    "shiftC" :{ "production_A_count" :0, "production_B_count" :0},
    }
    data=request.data
    jsonData = json.load(open('static/input1.json'))
    try:
        start_time = formatTime(data['start_time'])
        end_time = formatTime(data['end_time'])
    except Exception as e:
        message={'details':'Enter valid Time format (%Y-%m-%dT%H:%M:%SZ)'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
    for row in jsonData:
        time=datetime.strptime(row['time'], "%Y-%m-%d %H:%M:%S")
        if inBetween(time,start_time,end_time):
            shift=getShift(time.hour)
            if row['production_A']==True:
                res[shift]['production_A_count']+=1
            if row['production_B']==True:
                res[shift]['production_B_count']+=1
              
    return Response(res)




@api_view(['POST'])
def Question2(request):
    data=request.data
    jsonData = json.load(open('static/input2.json'))
    try:
        start_time = formatTime(data['start_time'])
        end_time = formatTime(data['end_time'])
    except Exception as e:
        message={'details':'Enter valid Time format (%Y-%m-%dT%H:%M:%SZ)'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
    downtime=runtime=0
    res={}
    for row in jsonData:
        time=datetime.strptime(row['time'], "%Y-%m-%d %H:%M:%S")
        if inBetween(time,start_time,end_time):
            if runtime>1021:
                downtime+=row['runtime']-1021
                runtime+=1021
            else:
                runtime+=row['runtime']

    totalTime=(end_time-start_time).total_seconds()
    utilisation=totalTime/(totalTime+downtime)*100
    res["runtime"]=convert(runtime)
    res["downtime"]=convert(downtime)
    res["utilisation"]=round(utilisation,2) 

    return Response(res)      



@api_view(['POST'])
def Question3(request):
    data=request.data
    jsonData = json.load(open('static/input3.json'))
    try:
        start_time = formatTime(data['start_time'])
        end_time = formatTime(data['end_time'])
    except Exception as e:
        message={'details':'Enter valid Time format (%Y-%m-%dT%H:%M:%SZ)'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
    tmp={}
    for row in jsonData:
        time=datetime.strptime(row['time'], "%Y-%m-%d %H:%M:%S")
        if inBetween(time,start_time,end_time):
            id=int((row['id'])[-3:])
            if row['state']==True:
                belt1=0
                belt2=row['belt2']
            else:
                belt1=row['belt1']
                belt2=0 
            if id in tmp:
                tmp[id]['sum_belt1']+=belt1
                tmp[id]['sum_belt2']+=belt2
                tmp[id]['count']+=1
            else:
                tmp[id]={'sum_belt1':belt1,'sum_belt2':belt2,'count':1}
    res=[]           
    for key,value in tmp.items():
        avg_belt1=int(value['sum_belt1']/value['count'])
        avg_belt2=int(value['sum_belt2']/value['count'])
        res.append({'id':key,'avg_belt1':avg_belt1,'avg_belt2':avg_belt2})

    return Response(res)          

