# Proof of Concept - Accès Biométrique

## 📌 Objectif

Cette application est un **Proof of Concept** pour un système d’accès biométrique.
Elle permet de :

* Tester l’authentification par **reconnaissance faciale** via webcam.
* Afficher le résultat de l’authentification (**accès autorisé** ou **refusé**) sur une interface simple.
* Préparer l’intégration future de tests supplémentaires comme la **voix** et l’**empreinte digitale**.

---

## 🛠 Technologies utilisées

* **Python 3** – langage principal.
* **Django 5** – framework web (architecture MVC).
* **HTML / CSS** – interface utilisateur simple.
* **JavaScript / Face-api.js** – détection et reconnaissance faciale via webcam.
* **Git / GitHub** – versionning du code.

---

## 📁 Structure du projet

```
biometric_project/
├── biometric_project/      # Configuration Django
├── biometric_app/          # Application principale
│   ├── templates/
│   │   ├── home.html
│   │   └── biometric_test.html
│   ├── static/
│       ├── css/style.css
│       └── js/face.js
├── manage.py               # Commandes Django
└── venv/                   # Environnement virtuel (non inclus dans Git)
```

---

## ⚡ Installation et lancement

### 1. Cloner le projet

```bash
git clone https://github.com/<your-username>/biometric-poc.git
cd biometric-poc
```

### 2. Créer et activer l’environnement virtuel

* Windows :

```bash
python -m venv venv
venv\Scripts\activate
```

* macOS / Linux :

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

> Si `requirements.txt` n’existe pas, installer Django :
>
> ```bash
> pip install django
> ```

### 4. Appliquer les migrations

```bash
python manage.py migrate
```

### 5. Lancer le serveur

```bash
python manage.py runserver
```

### 6. Ouvrir l’application

Ouvrir dans le navigateur :

```
http://127.0.0.1:8000/
```

* La **page principale** affiche le statut de l’authentification.
* Le bouton **“Faire un test biométrique”** permet d’ouvrir la page pour tester la reconnaissance faciale via webcam.

---

## 🔹 Notes

* Les modèles Face-api.js doivent être placés dans :
  `biometric_app/static/models/`
  ou téléchargés depuis le dépôt officiel [face-api.js models](https://github.com/justadudewhohacks/face-api.js/tree/master/weights).
* La reconnaissance faciale est un **exemple simple** pour le Proof of Concept.
