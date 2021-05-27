from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Addresses
from .serializers import AddressesSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json
from .faq_chatbot import faq_answer

# 장고에서 제공하는 사용자 IP 획득 함수
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Create your views here.
@csrf_exempt
def address_list(request):
    if request.method == 'GET':
        query_set = Addresses.objects.all()
        serializer = AddressesSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def address(request, pk):

    obj = Addresses.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = AddressesSerializer(obj)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)



@csrf_exempt
def login(request):

    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))
        id = request.POST.get('userid','')
        pw = request.POST.get('userpw', '')
        print("id = " + id + " pw = " + pw)

        result = authenticate(username=id, password=pw)

        if result :
            print("로그인 성공!")
            return HttpResponse(status=200)
        else:
            print("실패")
            return HttpResponse(status=401)


    return render(request, 'addresses/login.html')

@csrf_exempt
def app_login(request):

    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))
        id = request.POST.get('userid', '')
        pw = request.POST.get('userpw', '')
        print("id = " + id + " pw = " + pw)

        result = authenticate(username=id, password=pw)

        if result:
            print("로그인 성공!")
            return JsonResponse({'code': '0000', 'msg': '로그인성공입니다.'}, status=200)
        else:
            print("실패")
            return JsonResponse({'code': '1001', 'msg': '로그인실패입니다.'}, status=200)

# 0.0.0.0:8000/chat_test 내부 테스트용
@csrf_exempt
def chat_test(request):
    if request.method == 'POST':
        input1 = request.POST['input1']
        useragent1 = request.POST['useragent1']
        client_ip1 = get_client_ip(request)
        response = faq_answer(input1, useragent1, client_ip1)
        try:
            output = dict()
            output['response'] = response
            return HttpResponse(json.dumps(output), status=200)
        except:
            output = dict()
            output['response'] = '비슷한 질문에 대한 답변이 없습니다'
            return HttpResponse(json.dumps(output), status=200)
    else:
        return render(request, 'addresses/chat_test.html')

# 0.0.0.0/chat_service 웹 사이트 배포용
@csrf_exempt
def chat_service(request):
    if request.method == 'POST':
        input1 = request.POST['input1']
        useragent1 = request.POST['useragent1']
        client_ip1 = get_client_ip(request)
        response = faq_answer(input1, useragent1, client_ip1)
        try:
            output = dict()
            output['response'] = response
            return HttpResponse(json.dumps(output), status=200)
        except:
            output = dict()
            output['response'] = '비슷한 질문에 대한 답변이 없습니다'
            return HttpResponse(json.dumps(output), status=200)
    else:
        return render(request, 'addresses/chat_service.html')