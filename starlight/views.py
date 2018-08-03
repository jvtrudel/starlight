# Copyright (C) 2018 Savoir-faire Linux Inc. (<www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import logout
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from starlight.admin import MyUserCreationForm
from starlight.forms import EditForm, CompetencyForm, EmployeeForm
from starlight.models import Skill, Employee, Competency


def home(request):
    skills = Skill.objects.order_by('name')
    employees = Employee.objects.all()
    return render(request, 'views/home.html', {'skills': skills, 'employees': employees, 'viewgroup': 'home'})


@csrf_protect
def login(request):
    return render(request, 'login/login.html')


def profile(request, id):
    employee = Employee.objects.get(pk=id)
    return render(request, 'profile_views/profile.html', {'employee': employee, 'viewgroup': 'profile'})


def edit_competency(request, employee, id):
    competency = Competency.objects.get(pk=id)
    employee = Employee.objects.get(pk=employee)
    if not request.user.has_perm('starlight.can_change_user') and not employee == request.user:
        raise PermissionDenied({"message: You do not have permission to edit this"})
    skill = competency.skill
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            interest = form.cleaned_data['interest']
            experience = form.cleaned_data['experience']
            competency_new, created = employee.competencies.all().get_or_create(skill=skill, interest=interest, experience=experience)
            if created:
                employee.competencies.add(competency_new)
                employee.competencies.remove(competency)
                messages.success(request, 'Competency succesfully edited')

            return HttpResponseRedirect('/{}/profile/'.format(employee.id))

    else:
        form = EditForm()

    return render(request, 'profile_views/edit_competency.html', {'form': form, 'competency': competency, 'viewgroup': 'profile'})


def new_competency(request, employee):
    employee = Employee.objects.get(pk=employee)
    if not request.user.has_perm('starlight.can_change_user') and not employee == request.user:
        raise PermissionDenied({"message: You do not have permission to edit this"})
    if request.method == 'POST':
        form = CompetencyForm(request.POST, employee=employee)
        if form.is_valid():
            skill = form.cleaned_data['skill']
            competency_new = form.save(commit=False)

            if employee.competencies.all().filter(skill=skill).exists():
                employee.competencies.remove(employee.competencies.all().get(skill=skill))
                competency_new.save()
                employee.competencies.add(competency_new)
                messages.success(request, 'Competency with this skill already exists, it has been updated')
            else:
                competency_new.save()
                employee.competencies.add(competency_new)
                messages.success(request, 'Competency successfully added')

            return HttpResponseRedirect('/{}/profile/'.format(employee.id))

    else:
        form = CompetencyForm(employee=employee)

    return render(request, 'profile_views/new_competency.html', {'form': form, 'viewgroup': 'profile'})


def logout_view(request):
    logout(request)
    return home(request)


def all_profiles(request):
    employees = Employee.objects.all()
    return render(request, 'views/all_profiles.html', {'employees': employees, 'viewgroup': 'all_profiles'})


@user_passes_test(lambda u: u.has_perm('starlight.can_change_user'))
def new_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            employee = Employee.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            employee.set_password(password)
            employee.save()
            return HttpResponseRedirect('/{}/profile/'.format(employee.id))
    else:
        form = EmployeeForm()

    return render(request, 'views/new_employee.html', {'form': form})