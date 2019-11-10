# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import ugettext as _

from fk.forms import UserForm
from fk.models import Organization


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", { 'form': form })


def user_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserForm(instance=request.user)
    return render(request, "fk/profile.html", {'user_form': user_form })


def member_organizations_list(request):
    members = Organization.objects.filter(fkmember=True).order_by('name')
    return render(
        request,
        'fk/member_organizations_list.html',
        {
            'members': members,
            'title': _('Member organizations'),
        })
