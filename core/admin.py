from django.contrib import admin
from .models import Profilo, Contenuto, Preferito, Forum, CommentoForum

@admin.register(Profilo)
class ProfiloAdmin(admin.ModelAdmin):
    list_display = ('utente', 'avatar', 'punti', 'get_rank')
    search_fields = ('utente__username',)
    list_filter = ('avatar',)

    def get_rank(self, obj):
        return obj.get_rank()
    get_rank.short_description = 'Rank'


@admin.register(Contenuto)
class ContenutoAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'artista', 'album', 'anno', 'genere', 'autore', 'data_pubblicazione')
    search_fields = ('titolo', 'artista', 'genere', 'autore__username')
    list_filter = ('anno', 'genere', 'data_pubblicazione')


@admin.register(Preferito)
class PreferitoAdmin(admin.ModelAdmin):
    list_display = ('utente', 'contenuto', 'aggiunto_il')
    search_fields = ('utente__username', 'contenuto__titolo')
    list_filter = ('aggiunto_il',)


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'brano', 'creatore', 'data_creazione')
    search_fields = ('titolo', 'brano', 'creatore__username')
    list_filter = ('data_creazione',)


@admin.register(CommentoForum)
class CommentoForumAdmin(admin.ModelAdmin):
    list_display = ('forum', 'autore', 'testo', 'risposta_a', 'data_pubblicazione')
    search_fields = ('forum__titolo', 'autore__username', 'testo')
    list_filter = ('data_pubblicazione',)
