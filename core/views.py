import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm

from .models import Contenuto, Profilo, Forum, CommentoForum, Preferito
from .forms import RegistrazioneForm, ContenutoForm, AvatarForm, ForumForm, CommentoForumForm


def home(request):
    return render(request, 'home.html')


@csrf_protect
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenziali non valide.')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def registrazione_view(request):
    if request.method == 'POST':
        form = RegistrazioneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrazioneForm()
    return render(request, 'registrazione.html', {'form': form})

def player_frame(request):
    return render(request, "player-frame.html")



@login_required
def profilo_view(request):
    profilo = request.user.profilo
    avatar_form = AvatarForm(request.POST or None, instance=profilo)
    avatar_range = range(1, 11)

    if request.method == 'POST' and avatar_form.is_valid():
        avatar_form.save()

    contenuti = Contenuto.objects.filter(autore=request.user)

    # QUERY PREFERITI
    preferiti = request.user.preferito_set.select_related('contenuto').order_by('-aggiunto_il')

    # PATH STATICO AVATAR
    avatar_files = ["avatar1.png", "avatar2.png", "avatar3.png", "avatar4.png",
                    "avatar5.png", "avatar6.png", "avatar7.png", "avatar8.png",
                    "avatar9.png", "avatar10.png"]

    return render(request, 'profilo.html', {
        'user': request.user,
        'profilo': profilo,
        'avatar_form': avatar_form,
        'contenuti': contenuti,
        'preferiti': preferiti,
        'rank': profilo.get_rank(),
        'avatar_files': avatar_files
    })



@login_required
def nuovo_contenuto_view(request):
    if request.method == 'POST':
        form = ContenutoForm(request.POST, request.FILES)
        if form.is_valid():
            contenuto = form.save(commit=False)
            contenuto.autore = request.user
            contenuto.save()

            # Aggiorna i punti utente
            profilo = request.user.profilo
            profilo.punti += 5  # ogni contenuto vale 5 punti
            profilo.save()

            return redirect('profilo')
    else:
        form = ContenutoForm()
    return render(request, 'nuovo-contenuto.html', {'form': form})


def contenuto_esteso_view(request, contenuto_id):
    contenuto = get_object_or_404(Contenuto, id=contenuto_id)

    preferito = False
    if request.user.is_authenticated:
        preferito = contenuto.preferito_set.filter(utente=request.user).exists()

    return render(request, 'contenuto-esteso.html', {
        'contenuto': contenuto,
        'preferito': preferito
    })



def forums_view(request):
    query = request.GET.get('search', '')
    if query:
        forums = Forum.objects.filter(brano__icontains=query)
    else:
        forums = Forum.objects.all()
    return render(request, 'forums.html', {'forums': forums, 'query': query})


@login_required
def crea_forum(request):
    brano_precompilato = request.GET.get('brano', '')

    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.creatore = request.user
            forum.save()
            return redirect('forums')
    else:
        form = ForumForm(initial={'brano': brano_precompilato})

    return render(request, 'crea_forum.html', {'form': form})

@login_required
def elimina_contenuto(request, contenuto_id):
    contenuto = get_object_or_404(Contenuto, id=contenuto_id)

    if contenuto.autore != request.user:
        return JsonResponse({'status': 'forbidden'}, status=403)

    # 🧹 Se ha un'immagine, eliminala fisicamente dal disco
    if contenuto.immagine and os.path.isfile(contenuto.immagine.path):
        os.remove(contenuto.immagine.path)

    contenuto.delete()
    return JsonResponse({'status': 'ok'})



def browse_view(request):
    contenuti = Contenuto.objects.all()

    autore = request.GET.get('autore')
    anno = request.GET.get('anno')
    genere = request.GET.get('genere')
    testo = request.GET.get('testo')

    if autore:
        contenuti = contenuti.filter(artista__icontains=autore)
    if anno:
        contenuti = contenuti.filter(anno=anno)
    if genere:
        contenuti = contenuti.filter(genere__icontains=genere)
    if testo:
        contenuti = contenuti.filter(testo__icontains=testo)

    return render(request, 'browse.html', {'contenuti': contenuti})

def suggerisci_brani(request):
    query = request.GET.get('term', '')
    risultati = Contenuto.objects.filter(titolo__icontains=query)[:10]
    suggerimenti = [c.titolo for c in risultati]
    return JsonResponse(suggerimenti, safe=False)


def forum_dettaglio_view(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    commenti = CommentoForum.objects.filter(forum=forum).order_by('data_pubblicazione')

    if request.method == 'POST':
        form = CommentoForumForm(request.POST)
        if form.is_valid():
            commento = form.save(commit=False)
            commento.forum = forum
            commento.autore = request.user
            commento.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Renderizza di nuovo il contenuto parziale aggiornato
                commenti = CommentoForum.objects.filter(forum=forum).order_by('data_pubblicazione')
                form = CommentoForumForm()
                return render(request, 'partials/forum_detail_content.html', {
                    'forum': forum,
                    'commenti': commenti,
                    'form': form,
                    'user': request.user
                })

            return redirect('forum_dettaglio', forum_id=forum.id)
    else:
        form = CommentoForumForm()

    # Se richiesta AJAX: ritorna solo il blocco
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/forum_detail_content.html', {
            'forum': forum,
            'commenti': commenti,
            'form': form,
            'user': request.user
        })

    # Altrimenti pagina completa
    return render(request, 'forum_dettaglio.html', {
        'forum': forum,
        'commenti': commenti,
        'form': form
    })

@login_required
def elimina_forum_view(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    if forum.creatore != request.user:
        return JsonResponse({'status': 'forbidden'}, status=403)
    forum.delete()
    return JsonResponse({'status': 'ok'})

@login_required
def elimina_commento_view(request, commento_id):
    commento = get_object_or_404(CommentoForum, id=commento_id)
    if commento.autore != request.user:
        return JsonResponse({'status': 'forbidden'}, status=403)
    forum_id = commento.forum.id
    commento.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        forum = get_object_or_404(Forum, id=forum_id)
        commenti = CommentoForum.objects.filter(forum=forum).order_by('data_pubblicazione')
        form = CommentoForumForm()
        return render(request, 'partials/forum_detail_content.html', {
            'forum': forum,
            'commenti': commenti,
            'form': form
            
        })

    return redirect('forum_dettaglio', forum_id=forum_id)

@login_required
def aggiungi_preferito(request, contenuto_id):
    contenuto = get_object_or_404(Contenuto, id=contenuto_id)
    Preferito.objects.get_or_create(utente=request.user, contenuto=contenuto)
    return redirect('contenuto_esteso', contenuto_id=contenuto_id)

@login_required
def rimuovi_preferito(request, contenuto_id):
    contenuto = get_object_or_404(Contenuto, id=contenuto_id)
    Preferito.objects.filter(utente=request.user, contenuto=contenuto).delete()
    return redirect('contenuto_esteso', contenuto_id=contenuto_id)
