from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, DeleteView, FormView
from .models import Car, User_booking
from django.views import View
from django.urls import reverse_lazy
from .forms import CarForm, OrderForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class AddCarView(LoginRequiredMixin, View):
    template_name = 'add_car.html'

    def get(self, request):
        form = CarForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_carlist')
        return render(request, self.template_name, {'form': form})

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'  
    context_object_name = 'cars'  
    paginate_by = 12  

    
class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    template_name = 'car_update.html' 
    context_object_name = 'car'  
    form_class = CarForm  
    success_url = reverse_lazy('admin_carlist')  

class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    template_name = 'car_delete.html'
    context_object_name = 'car' 
    success_url = reverse_lazy('admin_carlist')


# order
#car booking
class CarBooking(LoginRequiredMixin,View):
    template_name = 'book_car.html'

    def get(self, request):
        form = OrderForm()
        context = {
            "form": form,
            "title": "Car Booking"
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = OrderForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('home')

        context = {
            "form": form,
            "title": "Create Order"
        }
        return render(request, self.template_name, context)
    

#car booking list
class order_list(LoginRequiredMixin, View):
    def get(self, request):
        order = User_booking.objects.all()

        query = request.GET.get('q')
        if query:
            order = order.filter(
                Q(movie_name__icontains=query)|
                Q(employee_name__icontains=query)
            )

        # pagination
        paginator = Paginator(order, 8)  # Show 15 contacts per page
        page = request.GET.get('page')
        try:
            order = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            order = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            order = paginator.page(paginator.num_pages)
        context = {
            'order': order,
        }
        return render(request, 'booking_list.html', context)
    
class BookingDetail(LoginRequiredMixin, DetailView):
    model = User_booking
    template_name = 'booking_detail.html'
    context_object_name = 'detail'

class BookingUpdate(LoginRequiredMixin, UpdateView):
    model = User_booking
    form_class = OrderForm
    template_name = 'booking_update.html' 
    context_object_name = 'order'  
    success_url = reverse_lazy('book_list')

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = User_booking
    template_name = 'booking_delete.html'  
    context_object_name = 'booking'  
    success_url = reverse_lazy('book_list')

# Authentication

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
    
class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        return super(RegisterPage, self).get(*args, **kwargs)
    

#Admin

class AdminCarListView(View):
    template_name = 'admin_index.html'
    paginate_by = 12

    def get(self, request):
        car_list = Car.objects.order_by('-id')

        query = request.GET.get('q')
        if query:
            car_list = car_list.filter(
                Q(car_name__icontains=query) |
                Q(company_name__icontains=query) |
                Q(num_of_seats__icontains=query) |
                Q(cost_par_day__icontains=query)
            )

        # Pagination
        paginator = Paginator(car_list, self.paginate_by)
        page = request.GET.get('page')
        try:
            cars = paginator.page(page)
        except PageNotAnInteger:
            cars = paginator.page(1)
        except EmptyPage:
            cars = paginator.page(paginator.num_pages)

        context = {'car': cars}
        return render(request, self.template_name, context)
    

# Database
import pandas as pd
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin

class ExportUsersToExcelView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def get(self, request):
        users = User.objects.values('username', 'password')

        user_data = pd.DataFrame(users)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="registered_users.xlsx"'

        # Write the DataFrame to the Excel file
        user_data.to_excel(response, index=False, sheet_name='Registered Users')

        return response



