from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from patients.models import Patient, DxRequest

class MedicDashboard(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'app/medics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context_data = super(MedicDashboard, self).get_context_data(**kwargs)
        context_data["pending_diagnostics"] = DxRequest.objects.filter(active=True).order_by('date').reverse()
        return context_data


class DiagnosticAtentionView(LoginRequiredMixin, CreateView, DetailView):
    pk_url_kwarg = 'dx_req'
    model = DxRequest
    form_class = DxRequestCreationForm
    template_name ='app/medics/dx_req.html'

    def form_valid(self, form):
        dx = form.save(commit=False)
        dx.patient = self.dxrequest
        dx.save()        
        self.dxrequest.active = False
        self.dxrequest.save()
        return redirect(reverse('medics:dashboard'))

    def post(self, request, *args, **kwargs):
        self.dxrequest = DxRequest.objects.get(id=kwargs["dx_req"])
        return super(DiagnosticAtentionView, self).post(request, *args, **kwargs)


class PatientDetailView(LoginRequiredMixin, DetailView):
    
    pk_url_kwarg = 'patient'
    model = Patient
    template_name ='app/medics/patient_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super(PatientDetailView, self).get_context_data(**kwargs)
        diagnostics = []
        dx_requests = context_data['patient'].dx_requests.all()
        for r in dx_requests:
            try:
                r.diagnostics
                diagnostics.append(r)
            except Exception as e:
                pass
        context_data["dx_requests"] = context_data['patient'].dx_requests.all().order_by('date')
        context_data["diagnostics"] = diagnostics
        return context_data
        