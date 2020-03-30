from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RoomBookForm
from .models import RoomBook
from script.main import main

# Create your views here.
def home_view(request, *args, **kwargs):
    print("Request is: ", request.user)
    print("args is:", args, "kwargs is: ", kwargs)
    # return HttpResponse("<h1>Helloo</h1>")
    return render(request, "home.html",{})

def run_script(request, *args, **kwargs):
    form = RoomBookForm(request.POST or None)
    if form.is_valid():
        # form.save()
        target_time = int(form.cleaned_data['target_time'])
        target_room = int(form.cleaned_data['target_room'])
        main(target_time, target_room)

        # print("Target Time IS:", type(target_time))
        # print("TARGET ROOM IS:", type(target_room))
        form = RoomBookForm()
    
    context = {
        'form': form
    }
    return render(request, "main/book_room.html",context)





# def product_create_view(request):
#     print("GET TITLE IS:", request.GET)
#     print("POST IS:", request.POST)
#     my_title = request.POST.get('title')
#     print("MY_TITLE IS: ",my_title)
#     #Product.object.create(title=my_title)
#     form = ProductForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         form = ProductForm()

#     context = {
#         'form': form
#     }
#     return render(request, "products/product_create.html", context)