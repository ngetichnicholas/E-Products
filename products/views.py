from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import Group
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.core.mail import EmailMessage
from .models import *
from .forms import *


# Create your views here.
def index(request):
  current_user = request.user
  products = Product.objects.all()
  return render(request, 'index.html',{'current_user':current_user, 'products':products})

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def contact(request):

    return render(request,'contact.html')

def signup_view(request):
    if request.method=='POST':
        signup_form=UserSignUpForm(request.POST)
        if signup_form.is_valid():
            user=signup_form.save()
            user.refresh_from_db()
            user.email = signup_form.cleaned_data.get('email')
            user.is_customer = True
            group, created = Group.objects.get_or_create(name='customer')
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('registration/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            to_email = signup_form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.send()
            return redirect('activation_sent')
    else:
        signup_form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'signup_form': signup_form})

def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        auth_login(request, user)
        messages.info(request, f"You are now logged in as {username}")
        return redirect('home')
      else:
        messages.error(request, "Invalid username or password.")
    else:
      messages.error(request, "Invalid username or password.")
  form = AuthenticationForm()
  return render(request = request,template_name = "registration/login.html",context={"form":form})

def activation_sent_view(request):
  return render(request, 'registration/activation_sent.html')

def activate(request, uidb64, token):
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  # checking if the user exists, if the token is valid.
  if user is not None and account_activation_token.check_token(user, token):
    # if valid set active true 
    user.is_active = True
    # set signup_confirmation true
    user.signup_confirmation = True
    user.save()
    login(request)
    return redirect('login')
  else:
    return render(request, 'registration/activation_invalid.html')
