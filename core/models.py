from django.db import models
from django.contrib.auth.models import User

class Profilo(models.Model):
    utente = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profilo")
    avatar = models.CharField(
        max_length=100,
        default="avatar1.png",
        choices=[(f"avatar{i}.png", f"Avatar {i}") for i in range(1, 11)]
    )
    punti = models.PositiveIntegerField(default=0)

    def get_rank(self):
        if self.punti >= 100:
            return 'S'
        elif self.punti >= 70:
            return 'A'
        elif self.punti >= 40:
            return 'B'
        elif self.punti >= 20:
            return 'C'
        elif self.punti >= 5:
            return 'D'
        else:
            return 'F'

    def __str__(self):
        return f"{self.utente.username} - Rank: {self.get_rank()}"


class Contenuto(models.Model):
    titolo = models.CharField(max_length=100)
    artista = models.CharField(max_length=100, default="Artista sconosciuto")
    album = models.CharField(max_length=100, blank=True, null=True)
    anno = models.PositiveIntegerField(blank=True, null=True)
    genere = models.CharField(max_length=50, blank=True, null=True)
    testo = models.TextField(help_text="Descrizione, storia o significato del brano")
    link = models.URLField(help_text="Link YouTube / Spotify / altro", blank=True, null=True)
    immagine = models.ImageField(upload_to='immagini/', blank=True, null=True)
    data_pubblicazione = models.DateTimeField(auto_now_add=True)
    autore = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titolo} - {self.artista}"
    
class Preferito(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    contenuto = models.ForeignKey(Contenuto, on_delete=models.CASCADE)
    aggiunto_il = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utente', 'contenuto')

    def __str__(self):
        return f"{self.utente.username} ha salvato {self.contenuto.titolo}"

class Forum(models.Model):
    titolo = models.CharField(max_length=100)
    brano = models.CharField(max_length=100)
    creatore = models.ForeignKey(User, on_delete=models.CASCADE)
    data_creazione = models.DateTimeField(auto_now_add=True)
    descrizione = models.TextField()

    def __str__(self):
        return self.titolo
    
class CommentoForum(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    autore = models.ForeignKey(User, on_delete=models.CASCADE)
    testo = models.TextField()
    risposta_a = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    data_pubblicazione = models.DateTimeField(auto_now_add=True)
