from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Contenuto, Profilo, Forum, CommentoForum
from datetime import datetime





class RegistrazioneForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email'
        })
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password'
        })
    )

    password2 = forms.CharField(
        label='Conferma Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Conferma Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Username'
            }),
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Esiste già un account con questa email.")
        return email



class ContenutoForm(forms.ModelForm):

    class Meta:
        model = Contenuto
        fields = [
            'titolo', 'artista', 'album', 'anno', 'genere',
            'testo', 'link', 'immagine'
        ]
        CURRENT_YEAR = datetime.now().year
        YEAR_CHOICES = [(y, y) for y in range(CURRENT_YEAR, 1899, -1)]
        widgets = {
            'titolo': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Titolo del brano'
            }),
            'artista': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Artista'
            }),
            'album': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Album (facoltativo)'
            }),
            'anno': forms.Select(choices=YEAR_CHOICES, attrs={
                'class': 'form-input'
            }),
            'genere': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Genere musicale'
            }),
            'testo': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Testo del brano...',
                'rows': 4
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'Link YouTube / Spotify'
            }),
            'immagine': forms.ClearableFileInput(attrs={
                'class': 'form-input'
            }),
        }

    def clean_titolo(self):
        titolo = self.cleaned_data['titolo']
        if Contenuto.objects.filter(titolo__iexact=titolo).exists():
            raise forms.ValidationError("Esiste già un brano con questo titolo.")
        return titolo
    def clean_link(self):
        link = self.cleaned_data.get('link')
        if not link:
            raise forms.ValidationError("Il link è obbligatorio.")
        return link

    def clean_immagine(self):
        immagine = self.cleaned_data.get('immagine')
        if not immagine:
            raise forms.ValidationError("L'immagine è obbligatoria.")
        return immagine






class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profilo
        fields = ['avatar']
        widgets = {
            'avatar': forms.Select(choices=[(f"avatar{i}.png", f"Avatar {i}") for i in range(1, 11)],
                                   attrs={'class': 'form-input'})
        }

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['titolo', 'brano', 'descrizione']
        widgets = {
            'titolo': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Titolo del forum'
            }),
            'brano': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Brano associato'
            })
        }

class CommentoForumForm(forms.ModelForm):
    class Meta:
        model = CommentoForum
        fields = ['testo']
        widgets = {
            'testo': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Scrivi il tuo commento...',
                'rows': 3
            })
        }
