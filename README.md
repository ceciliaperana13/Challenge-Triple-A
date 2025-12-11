# Challenge-Triple-A
Ce projet consiste à créer un tableau de bord complet de monitoring système.
Le script Python récupère des informations en temps réel sur :
    • Le système (hostname, OS, uptime, utilisateurs connectés)
    • Le CPU (cœurs, fréquence, utilisation)
    • La mémoire vive
    • Le réseau (adresse IP principale)
    • Les processus (Top 3 les plus gourmands)
    • Les fichiers présents dans un dossier utilisateur (images, vidéos, documents, autres)
Les données sont automatiquement injectées dans un template HTML pour générer un fichier index.html lisible dans un navigateur.
Le projet respecte les contraintes du sujet : HTML5 complet, sections sémantiques, CSS séparé, variables personnalisées et traitement algorithmique complet.

Prérequis
Avant de commencer, vous devez avoir installé :
    • Python 3.x
    • pip (inclus avec Python)
    • VSCode (facultatif mais recommandé)
    • Le module Python psutil

Utilisation
Lancer le script
python monitor.py
Ce script :
    1. Récupère les informations système
    2. Remplit le template template.html
    3. Génère automatiquement le fichier index.html
Ouvrir index.html
Une fois généré, double-cliquez simplement sur :
index.html
Le tableau de bord s’affiche dans votre navigateur.
Fonctionnalités
    • Analyse complète du CPU, RAM, uptime, OS, IP
    • Détection du nombre d’utilisateurs connectés
    • Top 3 des processus les plus gourmands
    • Analyse automatique d’un dossier utilisateur
    • Calcul de statistiques de fichiers
    • Génération dynamique d’un tableau de bord HTML
    • Barre de progression RAM avec CSS
    • Mise en page responsive et moderne
    • Dashboard entièrement autonome (sans Flask, sans JavaScript)
Difficultés rencontrées
    • Installation du module psutil sur VSCode (résolu via python -m pip install psutil)
    • Problèmes de remplacement des variables dans le template HTML
    • Gestion du temps CPU des processus (besoin d’un premier appel + délai)
    • Conversion mémoire en MB/GB
    • Organisation et cohérence des variables dans le template
    • Analyse de fichiers récursive (os.walk)
    • Débogage des chemins et encodage UTF-8 lors de la génération du fichier HTML

Améliorations possibles
    • Ajouter un rafraîchissement automatique via JavaScript
    • Export JSON complet des données système
    • Graphiques dynamiques CPU/RAM
    • Page multi-onglets (CPU / RAM / Processus)
    • Ajout d’icônes locales plutôt que des URLs
    • Version Flask pour une mise à jour en temps réel
    • Tableau détaillé de tous les processus
    • Sélection dynamique du dossier à analyser
Auteur·rice·s
    • Cécilia Perrana
    • Melvin Vincent