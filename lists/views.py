from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
	return HttpResponse('<html><title>To-Do lists</title></html>')
