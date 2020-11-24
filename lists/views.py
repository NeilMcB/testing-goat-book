from django.shortcuts import redirect, render

from .models import Item


def homepage(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/')

	return render(request, 'homepage.html', {'items': Item.objects.all()})
