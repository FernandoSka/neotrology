from django.views.generic import TemplateView, CreateView, ListView
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import Patient


class HomeView(LoginView):

    template_name = 'ethereal/index.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse("medics:dashboard")
        if self.request.user.patient:
            return reverse("patients:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return redirect(reverse("medics:dashboard"))
            if self.request.user.patient:
                return redirect(reverse("patients:dashboard"))

        return super(HomeView, self).dispatch(request, *args, **kwargs)


class LogoutView(LogoutView):
    next_page  = 'patients:home'


class PatientCreateView(CreateView):
    form_class = PatientCreationForm
    template_name = 'app/patient_sign.html'

    def get_success_url(self):
        return reverse('patients:home')


class PatientDashboard(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'app/patients/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context_data = super(PatientDashboard, self).get_context_data(**kwargs)
        diagnostics = []
        dx_requests = self.request.user.patient.dx_requests.all()
        for r in dx_requests:
            try:
                r.diagnostics
                diagnostics.append(r)
            except Exception as e:
                pass
            
        context_data = {
            "patient":self.request.user.patient,
            "dx_requests" : self.request.user.patient.dx_requests.all().order_by('date'),
            "diagnostics" : diagnostics
            }
        return context_data


class DxRequestCreateView(LoginRequiredMixin, CreateView):
    form_class = DxRequestCreationForm
    template_name = 'app/patients/dx_request.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.patient.has_active_dx():
            return redirect(reverse('patients:dashboard'))
        return super(DxRequestCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        dx = form.save(commit=False)
        dx.patient = self.request.user.patient
        dx.save()
        return redirect(reverse('patients:dashboard'))
        

# Create your views here.
