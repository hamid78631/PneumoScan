# 🫁 PneumoScan 

> Système d'aide au diagnostic médical par intelligence artificielle, avec explicabilité — détection de la pneumonie à partir de radiographies thoraciques.

![Statut](https://img.shields.io/badge/statut-en%20développement-orange)
![Objectif](https://img.shields.io/badge/objectif-éducatif-blue)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Laravel](https://img.shields.io/badge/Laravel-FF2D20?logo=laravel&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Sommaire

- [À propos du projet](#-à-propos-du-projet)
- [But éducatif & note d'intégrité](#-but-éducatif--note-dintégrité)
- [Avertissement médical](#-avertissement-médical)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Stack technique](#-stack-technique)
- [Jeu de données](#-jeu-de-données)
- [Méthodologie](#-méthodologie)
- [Feuille de route](#-feuille-de-route)
- [Structure du projet](#-structure-du-projet)
- [Installation & lancement](#-installation--lancement)
- [Perspectives futures](#-perspectives-futures)
- [Auteur](#-auteur)

---

## 🎯 À propos du projet

**PneumoScan AI** est une application web qui assiste les professionnels de santé dans la détection de la **pneumonie** à partir de radiographies thoraciques.

L'utilisateur téléverse une radio, et le système renvoie :
1. Un **diagnostic probable** (normal / pneumonie) accompagné d'un score de confiance.
2. Une **carte de chaleur (Grad-CAM)** qui met en évidence les zones de l'image ayant influencé la décision du modèle.

Ce second point est au cœur du projet : en médical, un modèle qui ne peut pas **expliquer** sa décision est inutilisable en pratique. PneumoScan AI ne se contente pas de prédire — il montre *pourquoi*, ce qui le rend interprétable et digne de confiance.

### Pourquoi ce projet ?

Dans de nombreuses régions, l'accès à des radiologues reste limité et les délais d'analyse sont longs. Un outil de **tri assisté par IA**, capable de signaler rapidement les cas suspects, peut avoir un réel impact sur la prise en charge des patients.

---

## 🎓 But éducatif & note d'intégrité

> **Ce projet est réalisé dans un cadre purement éducatif**, en tant que Projet de Fin d'Année (PFA) du cycle ingénieur, spécialité Data Science.

Son objectif est l'apprentissage et la démonstration de compétences en :
- apprentissage profond et vision par ordinateur,
- IA explicable (Explainable AI),
- architecture logicielle orientée micro-services,
- déploiement d'un modèle de machine learning en production.

**L'intégralité du code de ce projet est écrite par l'auteur.** Les outils d'assistance (documentation, IA, tutoriels) sont utilisés uniquement comme support de réflexion et d'apprentissage, jamais comme substitut au travail personnel. Chaque ligne de code est comprise, écrite et assumée par l'auteur.

---

## ⚕️ Avertissement médical

> **PneumoScan AI est un outil d'AIDE à la décision, et non un dispositif de diagnostic médical.**

Les prédictions du système ne doivent **jamais** remplacer l'avis d'un médecin qualifié. L'outil est destiné à assister, signaler et prioriser — la décision finale appartient toujours au professionnel de santé. Ce projet n'est pas certifié pour un usage clinique réel.

---

## ✨ Fonctionnalités

- 📤 Téléversement de radiographies thoraciques
- 🧠 Classification automatique (normal / pneumonie) avec score de confiance
- 🔥 Génération de cartes de chaleur **Grad-CAM** (explicabilité)
- 👤 Gestion des utilisateurs et authentification sécurisée
- 🗂️ Historique des analyses (patient, image, résultat, date)
- 📊 Tableau de bord des analyses passées

---

## 🏗️ Architecture

Le projet suit une **architecture micro-services** : trois composants indépendants qui communiquent entre eux. Cette séparation permet de faire collaborer l'écosystème PHP/Laravel (logique métier) et l'écosystème Python (intelligence artificielle), chacun dans son domaine de force.

```
┌──────────────┐      ┌──────────────────┐      ┌──────────────────────┐
│              │      │                  │      │                      │
│    React     │ ───▶ │     Laravel      │ ───▶ │  Service IA (Python) │
│  (Interface) │ ◀─── │  (Backend métier)│ ◀─── │   FastAPI            │
│              │      │                  │      │                      │
└──────────────┘      └──────────────────┘      └──────────────────────┘
   Téléversement       Authentification (JWT)      Chargement du modèle
   Affichage résultat  Gestion utilisateurs        Inférence (prédiction)
   Carte de chaleur    Base de données             Génération Grad-CAM
                       Historique des analyses
```

**Flux d'une analyse :**
1. Le médecin téléverse une radio depuis l'interface **React**.
2. **Laravel** reçoit la requête, vérifie l'authentification, puis transmet l'image au service IA.
3. Le **service Python/FastAPI** charge le modèle, effectue la prédiction et génère la carte de chaleur Grad-CAM.
4. Laravel enregistre le résultat en base de données et le renvoie à React.
5. React affiche le diagnostic et la carte de chaleur à l'utilisateur.

---

## 🛠️ Stack technique

| Couche | Technologies |
|--------|-------------|
| **Frontend** | React, JavaScript/TypeScript |
| **Backend métier** | Laravel (PHP), Laravel Sanctum (authentification par jetons) |
| **Service IA** | Python, FastAPI, TensorFlow / PyTorch |
| **Base de données** | MySQL / PostgreSQL |
| **Entraînement** | Google Colab (GPU gratuit) |
| **Explicabilité** | Grad-CAM |
| **Outils** | Git, Docker (optionnel) |

---

## 📊 Jeu de données

**Chest X-Ray Images (Pneumonia)** — jeu de données public de radiographies thoraciques étiquetées (normal / pneumonie).

Points méthodologiques à traiter :
- **Déséquilibre des classes** (plus de cas pneumonie que de cas normaux).
- **Augmentation de données** pour renforcer la robustesse du modèle.
- **Découpage stratifié** entraînement / validation / test.

---

## 🔬 Méthodologie

Ce qui distingue ce projet d'un simple classifieur, ce sont les choix méthodologiques rigoureux :

1. **Analyse exploratoire (EDA)** — comprendre la distribution, la qualité et l'équilibre des images.
2. **Modèle de référence (baseline)** — un premier réseau simple, pour fixer un score à battre.
3. **Transfert d'apprentissage** — comparaison d'architectures pré-entraînées (ResNet, EfficientNet, et un Vision Transformer).
4. **Réglage fin (fine-tuning)** — adaptation des modèles au domaine médical.
5. **Explicabilité (Grad-CAM)** — visualisation des zones décisives.
6. **Évaluation médicale rigoureuse** — au-delà de l'accuracy : sensibilité, spécificité, courbe ROC-AUC, matrice de confusion.

---

## 🗺️ Feuille de route

- [ ] **Phase 0 — Cadrage**
  Validation du sujet avec l'encadrant, définition précise du cas d'usage.
- [ ] **Phase 1 — Données & EDA**
  Récupération du jeu de données, analyse exploratoire des images.
- [ ] **Phase 2 — Préprocessing & baseline**
  Prétraitement, augmentation, premier modèle de référence sur Colab.
- [ ] **Phase 3 — Transfert d'apprentissage**
  Comparaison d'architectures pré-entraînées, réglage fin.
- [ ] **Phase 4 — Explicabilité & évaluation**
  Intégration de Grad-CAM, évaluation avec les bonnes métriques médicales.
- [ ] **Phase 5 — Déploiement & rapport**
  Service FastAPI, backend Laravel, interface React, rédaction du rapport.

---

## 📁 Structure du projet

```
PneumoScan-AI/
├── frontend/              # Application React (interface)
├── backend/               # API Laravel (métier, sécurité, base de données)
├── ai-service/            # Service Python / FastAPI (IA)
│   ├── notebooks/         # EDA et expérimentations (Jupyter / Colab)
│   ├── models/            # Modèles entraînés
│   ├── app/               # API d'inférence (prédiction + Grad-CAM)
│   └── requirements.txt   # Dépendances Python
├── docs/                  # Documentation, schémas, rapport
├── .gitignore
└── README.md
```

---

## 🚀 Installation & lancement

> ⚠️ Le projet est en cours de développement. Cette section sera complétée au fur et à mesure.

```bash
# Cloner le dépôt
git clone https://github.com/<utilisateur>/PneumoScan-AI.git
cd PneumoScan-AI

# --- Service IA (Python) ---
cd ai-service
pip install -r requirements.txt
uvicorn app.main:app --reload

# --- Backend (Laravel) ---
cd ../backend
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan serve

# --- Frontend (React) ---
cd ../frontend
npm install
npm start
```

---

## 🔭 Perspectives futures

Grâce à son **architecture modulaire**, PneumoScan AI est conçu pour évoluer. Le service IA étant indépendant, d'autres modèles pourront être ajoutés sans modifier le reste de l'application. Pistes envisagées :

- 👁️ **Rétinopathie diabétique** — détection des stades de gravité à partir d'images du fond de l'œil (dépistage d'une cause majeure de cécité évitable).
- 🩺 **Mélanome** — classification de lésions cutanées pour le dépistage du cancer de la peau.

> Ces extensions dépassent le périmètre du PFA actuel (centré sur la pneumonie) et constituent des évolutions possibles du projet.

---

## 👤 Auteur

**Hamid** — Étudiant en cycle ingénieur, spécialité Data Science
Université Mundiapolis
Projet de Fin d'Année (PFA) — 2025/2026

---

## 📄 License

Ce projet est distribué sous licence MIT — voir le fichier `LICENSE` pour plus de détails.
