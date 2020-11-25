from django.shortcuts import redirect, render

from .models import Item


def homepage(request):
	return render(request, 'homepage.html')


def view_list(request):
	return render(request, 'list.html', {'items': Item.objects.all()})


def new_list(request):	
	Item.objects.create(text=request.POST['item_text'])
	return redirect('/lists/the-only-list-in-the-world/')

