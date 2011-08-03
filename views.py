from django.http import HttpResponse
from mathsBackend import *

def hello_world(request, value): 
	return HttpResponse(str(answerCallback(value)))

def store(request, value):
	xx(value)
	return HttpResponse("STORED")
