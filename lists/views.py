from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
	return render(
		request,
		'homepage.html',
		{'new_item_text': request.POST.get('item_text', '')},
	)
