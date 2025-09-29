# 🛒 Commerce - Plateforme d’enchères en ligne

Projet développé dans le cadre du cours **CS50’s Web Programming with Python and JavaScript (Harvard)**.
L’objectif est de concevoir une application web de type **eBay**, permettant aux utilisateurs de publier des annonces, de placer des enchères, de commenter et de gérer une liste de surveillance.

---

## 📌 Fonctionnalités principales

* **Gestion des utilisateurs**

  * Inscription, connexion et déconnexion
  * Authentification sécurisée via Django
  * Accès différencié aux fonctionnalités selon l’état de connexion

* **Création et gestion d’annonces**

  * Création d’une annonce avec :

    * Titre
    * Description textuelle
    * Prix de départ
    * Image (optionnelle)
    * Catégorie (ex. Mode, Jouets, Électronique, Maison…)
  * Fermeture d’une enchère par le créateur

* **Enchères**

  * Les utilisateurs connectés peuvent placer des offres
  * Vérification automatique de la validité d’une enchère :

    * Supérieure au prix actuel
    * Supérieure ou égale au prix de départ
  * Attribution automatique du gagnant lors de la fermeture de l’annonce

* **Commentaires**

  * Ajout de commentaires sur les annonces
  * Affichage de tous les commentaires liés à une annonce

* **Liste de surveillance**

  * Ajout/retrait d’une annonce à sa **watchlist**
  * Page dédiée listant toutes les annonces surveillées

* **Catégories**

  * Liste de toutes les catégories disponibles
  * Filtrage des annonces par catégorie

* **Administration (Django Admin)**

  * Gestion complète des annonces, enchères et commentaires
  * Création d’un superutilisateur pour accéder à l’interface

---

## 🛠️ Stack technique

* **Backend :** Django (Python)
* **Base de données :** SQLite (par défaut)
* **Frontend :** HTML, CSS, Django Templates
* **Authentification :** Django `AbstractUser`
* **Déploiement local :** Django `runserver`

---


## 🚀 Installation et exécution

### 1. Cloner le projet

```bash
git clone https://github.com/urielmahutondji/cs50-auctions.git
cd commerce
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations

```bash
python manage.py makemigrations auctions
python manage.py migrate
```

### 5. Lancer le serveur

```bash
python manage.py runserver
```

Accéder à l’application sur : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👤 Création d’un superutilisateur

```bash
python manage.py createsuperuser
```

➡ Accès à l’administration Django via : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📝 Spécification respectée

1. Modèles : `Listing`, `Bid`, `Comment`, `User`
2. Création et gestion d’annonces
3. Affichage des annonces actives
4. Page détaillée pour chaque annonce
5. Système d’enchères et de fermeture
6. Liste de surveillance (watchlist)
7. Catégories filtrables
8. Interface d’administration complète

---

## 📸 Démonstration

👉 [Voir la vidéo de démonstration sur YouTube](https://youtu.be/F8QGseH9P2Y?si=7Y87rqFSxqt62YxX)

---

## 📌 Roadmap (améliorations futures)

* Notifications en temps réel pour les nouvelles enchères
* Intégration de WebSockets (Django Channels)
* Système de messagerie entre acheteurs et vendeurs
* Déploiement sur une plateforme cloud (Heroku, Render, etc.)

---

## 📜 Licence

Projet réalisé dans le cadre du **CS50 Web Programming with Python and JavaScript**.
Code disponible sous licence MIT.

---

## 👨‍💻 Auteur

Développé par **urielmahutondji** dans le cadre du projet **CS50W Commerce**.
