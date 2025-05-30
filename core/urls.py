from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registrazione/', views.registrazione_view, name='registrazione'),
    path('profilo/', views.profilo_view, name='profilo'),
    path('nuovo/', views.nuovo_contenuto_view, name='nuovo'),
    path('contenuto/<int:contenuto_id>/', views.contenuto_esteso_view, name='contenuto_esteso'),
    path("player-frame/", views.player_frame, name="player_frame"),
    path('forums/', views.forums_view, name='forums'),
    path('forums/nuovo/', views.crea_forum, name='crea_forum'),
    path('contenuto/<int:contenuto_id>/elimina/', views.elimina_contenuto, name='elimina_contenuto'),
    path('browse/', views.browse_view, name='browse'),
    path('ajax/suggerisci-brani/', views.suggerisci_brani, name='suggerisci_brani'),
    path('forums/<int:forum_id>/', views.forum_dettaglio_view, name='forum_dettaglio'),
    path('forums/<int:forum_id>/elimina/', views.elimina_forum_view, name='elimina_forum'),
    path('commenti/<int:commento_id>/elimina/', views.elimina_commento_view, name='elimina_commento'),
    path('preferiti/aggiungi/<int:contenuto_id>/', views.aggiungi_preferito, name='aggiungi_preferito'),
    path('preferiti/rimuovi/<int:contenuto_id>/', views.rimuovi_preferito, name='rimuovi_preferito'),
]
