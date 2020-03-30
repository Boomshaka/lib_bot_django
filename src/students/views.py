from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse
from django.contrib.auth.hashers import make_password

from django.views import View
from .forms import StudentForm
from .models import Student

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

class StudentListView(ListView):
    template_name = 'students/student_list.html'
    queryset = Student.objects.all()

class StudentDetailView(DetailView):
    template_name = 'students/student_detail.html'
    queryset = Student.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("my_id")
        return get_object_or_404(Student, id=id_)

class StudentCreateView(View):
    template_name = 'students/student_create.html'
    query = Student.objects.all()
    form_class = StudentForm

    def get(self,request, id = None, *args, **kwargs):
        form = StudentForm()
        context = {
            "form":form
        }
        return render(request, self.template_name, context)

    def post(self, request, id = None, *args, **kwargs):
        form = StudentForm(request.POST or None)
        if form.is_valid():
            # user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # make_password(password)
            form.cleaned_data['username'] = make_password(password)
            form.save()
            form = StudentForm
        
        context = {
            'form':form
        }
        return render(request, self.template_name,context)

# class StudentCreateView(CreateView):
#     template_name = 'students/student_create.html'
#     from_class = StudentForm
#     queryset = Student.objects.all()
    
#     def form_valid(self, form):
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return'../'

#     def post(self, request, id = None, *args, **kwargs):
#         form = StudentForm(request.POST or None)
#         if form.is_valid():
#             user = form.save(commit=False)
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.make_password(password)
#             user.save()
#             form = ProductForm
        
#         context = {
#             'form':form
#         }
#         return render(request, self.template_name,context)


# Create your views here.
