import re
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.conf import settings
from django.db.models import Count
from datetime import date
from django.db.models.functions import Lower
from django.contrib.auth import login

from .models import User
from .models import EggHunt
from .models import Egg
from .models import EggCompletion

from .forms import RegistrationForm


def index(request):
  context = {}
  return render(request, 'index.html', context)

def start(request, hunt):
  if request.user.is_authenticated:
    egghunt = get_object_or_404(EggHunt, slug=hunt)
    eggs = Egg.objects.filter(egghunt=egghunt)
    eggsAmount = eggs.count()
    leaderboard = EggCompletion.objects.filter(egg__in=eggs).values('person', 'person__username').annotate(total=Count('person')).order_by('-total')
    context = {"egghunt": egghunt, "eggsAmount": eggsAmount, "eggs": eggs, "leaderboard": leaderboard }
    return render(request, 'start.html', context)
  else:
    return redirect('register', hunt)

def egg(request, hunt, egg):
  if request.user.is_authenticated:
    egghunt = get_object_or_404(EggHunt, slug=hunt)
    egg = get_object_or_404(Egg, slug=egg)
    completion = EggCompletion.objects.filter(person=request.user).filter(egg=egg).first()
    newfound = ""
    if not completion:
      newfound = "1"
      completion = EggCompletion(person=request.user, egg=egg)
      completion.save()
    eggs = Egg.objects.filter(egghunt=egghunt)
    eggsAmount = eggs.count()
    eggsCompletion = EggCompletion.objects.filter(egg__in=eggs).filter(person=request.user).count()
    context = {"egghunt": egghunt, "egg": egg, "new": newfound, 
      "eggsAmount": eggsAmount, "eggsCompletion": eggsCompletion }
    return render(request, 'egg.html', context)
  else:
    return redirect('register', hunt, egg)


def register(request, hunt="", egg=""):
  if request.user.is_authenticated:
    if egg:
      return redirect('egg', hunt, egg)
    return redirect('start', hunt)
  else:
    form = RegistrationForm()
    if request.method == 'POST':
      user = User.objects.filter(username__exact=request.POST.get('username')).first()
      if not user:
        form = RegistrationForm(request.POST)
        if form.is_valid():
          user = form.save()
      if user:
        login(request, user)
        if egg:
          return redirect('egg', hunt, egg)
        return redirect('start', hunt)
    context = {"hunt": hunt, "egg": egg, "form": form}
    return render(request, 'register.html', context)

def overview_list(request):
  if request.user.is_authenticated:
    egghunts = EggHunt.objects.all().order_by(Lower('name'))
    return render(request, 'overview_list.html', { "egghunts": egghunts })
  else:
    return redirect('register')

def overview_details(request, hunt):
  if request.user.is_authenticated:
    egghunt = get_object_or_404(EggHunt, slug=hunt)
    eggs = Egg.objects.filter(egghunt=egghunt).order_by(Lower('name'))
    return render(request, 'overview_details.html', { "egghunt": egghunt, "eggs": eggs })
  else:
    return redirect('register')

def overview_details_clear(request, hunt):
  if request.user.is_authenticated and request.user.is_superuser:
    egghunt = get_object_or_404(EggHunt, slug=hunt)
    eggs = Egg.objects.filter(egghunt=egghunt).order_by(Lower('name'))
    eggsCompletion = EggCompletion.objects.filter(egg__in=eggs)
    eggsCompletion.delete()
    return redirect('overview_details', hunt)
  else:
    return redirect('register')
