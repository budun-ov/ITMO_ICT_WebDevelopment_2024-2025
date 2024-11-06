from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import Car
from .forms import CarForm
from .models import Owner
from .forms import OwnerForm

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('owner_list')  # Перенаправление после успешной регистрации

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Автоматически авторизуем пользователя после регистрации
        return super().form_valid(form)

# Вывод всех владельцев
def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner_list.html', {'owners': owners})

# Вывод владельца по ID
def owner_detail(request, owner_id):
    owner = get_object_or_404(Owner, id=owner_id)
    return render(request, 'owner_detail.html', {'owner': owner})

# Обновление данных владельца
def owner_update(request, owner_id):
    owner = get_object_or_404(Car, id=owner_id)
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('owner_detail', owner_id=owner.id)
    else:
        form = OwnerForm(instance=owner)
    return render(request, 'owner_update.html', {'form': form, 'owner': owner})

# Добавление нового владельца
class OwnerCreateView(CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'owner_add.html'
    success_url = reverse_lazy('owner_list')

# Вывод всех автомобилей
class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

# Вывод автомобиля по ID
class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

# Обновление данных автомобиля
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_update.html'

    # Перенаправление после успешного обновления
    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

# Добавление нового авто
class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_add.html'
    success_url = reverse_lazy('car_list')