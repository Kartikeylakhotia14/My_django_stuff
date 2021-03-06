
from . import forms
from . import models
from . import serializers
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
def index(request):
    return render(request, 'kreiva/index.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
                profile.save()
                registered = True
        else:
                print(user_form.errors, profile_form.errors)
    else:
            user_form = forms.UserForm()
            profile_form = forms.UserProfileInfoForm()
    return render(request, "kreiva/registration.html", {'registered': registered, 'user_form': user_form,
                                                                'profile_form': profile_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and Password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied")
    return render(request, 'kreiva/login.html', {})
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged In, Nice!")




class UserPartiInfo(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return models.UserPartiInfo.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk=None):
        if pk:
            city = self.get_object(pk)
            serializer = serializers.UserPartiInfoSerializer(city)
            return Response(serializer.data)
        # else:
        #     state = models.State.objects.order_by("name")
        #     city = models.City.objects.order_by("state", "name")
        # return render(request, 'places/city.html', {'citys': city, 'states': state})

    def post(self, request):
            serializer = serializers.UserPartiInfoSerializer(data=request.data)
            response = {'status': True}
            if serializer.is_valid():
                serializer.save()
            else:
                response.update({'status': False, 'msg': str(serializer.errors)})
            return Response(response)
