from django.shortcuts import render, redirect
from django.contrib import messages
from base.models import CustomUser, Note
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from math import sin, cos, sqrt, atan2, radians
from django.core.serializers.json import DjangoJSONEncoder
from base.forms import UserProfileForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Note
import json


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'Identifiant ou mot de passe incorrect.')
            return redirect('/login')

    return render(request, 'main/login.html')


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        interet = request.POST.get('interet')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        age = request.POST.get('age')
        
        if username == '' or password == '' or email == '':
            messages.error(request, 'Il manque un ou plusieurs champs.')
            return redirect('/register')
        
        users = CustomUser.objects.all()
        for user in users :
         
            if user.username == request.POST.get('username'):
                messages.error(request, "Ce nom d'utilisateur est déjà utilisé. Choisis-en un autre.")
                return redirect('/register')
        user = CustomUser.objects.create_user(username=username, email=email, gender=gender, interet=interet, latitude=latitude, longitude=longitude, password=password, first_name=first_name, last_name=last_name, age=age)
        user.save()
        
        return redirect('/home')
    
    else:
        context = {}
        return render(request, 'main/register.html', context)


def distance_users(x1, y1, x2, y2):
    R = 6373.0
    lat1 = radians(x1)
    lon1 = radians(y1)
    lat2 = radians(x2)
    lon2 = radians(y2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
   
    return distance


@login_required
def home(request):
    current_user = request.user
   
    if current_user.interet == 'Both':
        potential_matches = CustomUser.objects.filter(
            Q(interet=current_user.gender) | Q(interet='Both')
        ).exclude(id=current_user.id)
    else:
        potential_matches = CustomUser.objects.filter(
            Q(gender=current_user.interet),
            Q(interet=current_user.gender) | Q(interet='Both')
        ).exclude(id=current_user.id)

    potential_matches = potential_matches.exclude(
    id__in=Note.objects.filter(emitter=current_user).values('receiver'))

    nearby_users = []
    for user in potential_matches:
        
        distance = distance_users(current_user.latitude, current_user.longitude, user.latitude, user.longitude)

        if distance < 5:  
            nearby_users.append(user)

    serialized_users = [
        {
            'id': user.id,
            'first_name': user.first_name,
            'age' : user.age,
            'image_url': user.image.url if user.image else '/static/images/Neutral.png'  
        }
        for user in nearby_users
    ]

    return render(request, 'main/home.html', {
        'nearby_users_json': json.dumps(serialized_users, cls=DjangoJSONEncoder),
    })


def logout_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('Confirm') == 'Oui':
                logout(request)
                return redirect('login')  
            else:
                return redirect('home')  
        
        return render(request, 'main/logout.html')

    return redirect('login')

@csrf_exempt
def create_note(request):
    if request.method == "POST":
        data = json.loads(request.body)
        emitter = CustomUser.objects.get(id=data['emitter_id'])
        receiver = CustomUser.objects.get(id=data['receiver_id'])
        is_like = data['is_like']
        
        note = Note.objects.create(emitter=emitter, receiver=receiver, is_like=is_like)
        note.save()
        if is_like == True:
            match = Note.objects.filter(emitter=receiver, receiver=emitter, is_like=True).exists()
        else:
            match= False
        return JsonResponse({'status': 'success', 'match': match})
    
    return JsonResponse({'status': 'failed'}, status=400)

def mesmatchs(request):
    current_user = request.user
    likes_donnés = Note.objects.filter(emitter_id=current_user.id, is_like=True)
    likes_reçus = Note.objects.filter(receiver= current_user, is_like=True)
    matchs = []

    for i in likes_donnés : 
        for j in likes_reçus :
            if i.receiver == j.emitter :
                matchs.append(i.receiver)


    distances = {}
    for match in matchs:
        distance = distance_users(
            current_user.latitude,
            current_user.longitude,
            match.latitude,
            match.longitude
        )
        distances[match.username] = distance

    context = { 'matchs' : matchs, 'distances' : distances}
    return render(request, 'main/mesmatchs.html', context)

def profil(request):
    return render(request, 'main/profil.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès. En cas de changement d'intérêt, vos anciens matchs sont conservés.")
            return redirect('profil')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profil.html', {'form': form})
