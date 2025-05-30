# 📀 JukeWiki - Progetto Django

JukeWiki è una piattaforma wiki/social dedicata alla cultura musicale e letteraria. Gli utenti possono inserire contenuti, commentare, creare forum e salvare i propri brani/articoli preferiti. Il progetto è sviluppato con Django.

---

## 📌 Funzionalità

- Autenticazione utenti (registrazione, login, logout)
- Inserimento di contenuti musicali/culturali
- Visualizzazione contenuto esteso con link, immagine, testo, artista
- Salvataggio contenuti nei preferiti
- Creazione forum e commenti (anche risposte nidificate)
- Pagina profilo con avatar, punti e rank utente
- Reel degli ultimi contenuti accessibile anche senza login
- Filtri di ricerca per autore, anno, genere

---

## ⚙️ Tecnologie Utilizzate

| Componente         | Tecnologia             |
|--------------------|------------------------|
| Backend            | Django (Python 3)      |
| Frontend           | HTML, CSS (custom)     |
| Database           | SQLite (sviluppo)      |
| File Upload        | Django Media           |
| Autenticazione     | Django Auth            |
| Template Engine    | Django Templates       |

---

## 🧪 Setup del Progetto

1. **Clona il progetto** o scaricalo come ZIP.
2. Crea ambiente virtuale:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```
3. Installa i pacchetti:
   ```bash
   pip install -r requirements.txt
   ```
4. Avvia il server:
   ```bash
   python manage.py runserver
   ```

---

## 📂 Struttura Principale

```
jukewiki/
├── manage.py
├── db.sqlite3
├── media/
├── static/
├── jukewiki/
│   ├── settings.py
│   └── urls.py
├── core/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   └── static/
```

---

## 🧠 Modello E-R

- **Profilo**: avatar, punti, rank
- **Contenuto**: brano o articolo
- **Preferito**: salvataggi utente-contenuto
- **Forum**: discussione collegata a brano
- **CommentoForum**: commenti e risposte nidificate
