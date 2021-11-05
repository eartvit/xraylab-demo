from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import XRayData
from django.views.generic import ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin


class XRayListView(LoginRequiredMixin, ListView):
    login_url = 'login'  # specify the login_url within the LoginRequiredMixin
    model = XRayData
    template_name = 'xraylab/home.html'  # By default it searches for this pattern <app>/<model>_<viewtype>.html
    context_object_name = 'xray_tests'
    ordering = ['-test_date']  # Order descending - last uploaded result is at the top of the list.


class XRayUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    success_message = 'Notes updated'
    login_url = 'login'
    model = XRayData
    template_name = 'xraylab/details_update.html'
    context_object_name = 'xray_data'
    fields = ['notes']
    # pk_url_kwarg = 'id'

    def form_valid(self, form):
        if form.instance.notes == '':
            form.instance.author = None
        else:
            form.instance.author = self.request.user

        return super().form_valid(form)


def about(request):
    return render(request, 'xraylab/about.html')

