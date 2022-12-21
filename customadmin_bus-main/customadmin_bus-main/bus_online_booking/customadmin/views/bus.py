from xml.sax.saxutils import prepare_input_source

from requests import request
from bus.models import Booked_bus, Category, Journey, Transport
from customadmin.forms.addbus_form import AddbusCreationForm
from customadmin.forms.addbus_form import AddbusUpdateForm
from customadmin.forms.category_form import CategoryCreationForm
from customadmin.forms.destination import JourneyCreationForm, JourneyUpdateForm
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyDetailView,
    MyLoginRequiredView,
    MyUpdateView,
)
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import TemplateView, DetailView
from django_datatables_too.mixins import DataTableMixin
from django.contrib.auth.models import User
from ..forms import UserChangeForm, UserCreationForm
from django.shortcuts import reverse, render

from django.contrib.auth.models import User

class AddbusListView(MyListView):
    model = Transport
    template_name = 'customadmin/adminuser/addbus.html'
    ordering = ["id"]

    def get_queryset(self):
        return self.model.objects.all()

class AddbusCreateView(MyCreateView):
    model = Transport
    form_class = AddbusCreationForm
    template_name = 'customadmin/adminuser/addbus_form.html'

    def get_form_kwargs(self) :
        print("**********************")
        print(super().get_form_kwargs)
        return super().get_form_kwargs()
    
    def get_success_url(self):
        return reverse("customadmin:transport-list")
class AddbusDetailView(MyDetailView):
    template_name = "customadmin/adminuser/addbus_detail.html"
    context = {}

    def get(self, request, pk):
        self.context['addbus_detail'] = Transport.objects.filter(pk=pk).first()
        self.context['addbus_detail_1'] =Booked_bus.objects.filter(busname=self.context['addbus_detail'])
        return render(request, self.template_name, self.context)
class AddbusUpdateView(MyUpdateView):
    model = Transport
    form_class = AddbusUpdateForm
    template_name = 'customadmin/adminuser/addbus_update_form.html'

    def get_success_url(self):
        return reverse("customadmin:transport-list")
class BusDeleteView(MyDeleteView):
    model = Transport
    template_name = 'customadmin/confirm_busdelete.html'

    def get_success_url(self):
        return reverse("customadmin:transport-list")
class PessengerListView(MyListView):
    model = Booked_bus
    template_name = 'customadmin/adminuser/pessenger_list.html'
    ordering = ["id"]

    def get_queryset(self):
        return self.model.objects.all()
class CategoryListView(MyListView):
    model = Category
    template_name = 'customadmin/adminuser/bus_category_list.html'
    ordering = ["id"]

    def get_queryset(self):
        return self.model.objects.all()
class CategoryCreateView(MyCreateView):
    model = Category
    form_class = CategoryCreationForm
    template_name = 'customadmin/adminuser/buscategory_form.html'

    def get_form_kwargs(self) :
        print("**********************")
        print(super().get_form_kwargs)
        return super().get_form_kwargs()
    
    def get_success_url(self):
        return reverse("customadmin:category-list")
class CategoryDeleteView(MyDeleteView):
    model = Category
    template_name = 'customadmin/confirm_categorydelete.html'

    def get_success_url(self):
        return reverse("customadmin:category-list")
class JourneyListView(MyListView):
    model = Journey
    template_name = 'customadmin/adminuser/bus_journey_list.html'
    ordering = ["id"]

    def get_queryset(self):
        return self.model.objects.all()
class JourneyCreateView(MyCreateView):
    model = Journey
    form_class = JourneyCreationForm
    template_name = 'customadmin/adminuser/journey_form.html'

    def get_form_kwargs(self) :
        print("**********************")
        print(super().get_form_kwargs)
        return super().get_form_kwargs()
    
    def get_success_url(self):
        return reverse("customadmin:journey-list")
class JourneyDetailView(MyDetailView):
    template_name = "customadmin/adminuser/journey_detail.html"
    context = {}

    def get(self, request, pk):
        self.context['journey_detail'] = Journey.objects.filter(pk=pk).first()
        return render(request, self.template_name, self.context)
class JourneyUpdateView(MyUpdateView):
    model = Journey
    form_class = JourneyUpdateForm
    template_name = 'customadmin/adminuser/journey_update_form.html'

    def get_success_url(self):
        return reverse("customadmin:journey-list")
class JourneyDeleteView(MyDeleteView):
    model = Journey
    template_name = 'customadmin/confirm_journeydelete.html'

    def get_success_url(self):
        return reverse("customadmin:journey-list")