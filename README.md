# Jade d’Albenas : site internet

Site autonome de présentation de Jade, Gestalt-thérapeute à Rennes.

- Quatre pages : accueil, thérapie, approche et contact.
- Fonds ivoire et beige, paysage inspiré du kintsugi.
- Eau animée avec grandes ondes au clic, brise et petites feuilles.
- Barre de progression, repères latéraux et chevrons entre les tableaux.
- Premier chevron dans l’eau : onde puis descente, interrompable au toucher ou à la molette.
- Pause au clavier (Échap) et respect du réglage de mouvement réduit.
- Affichage adapté au téléphone et à l’ordinateur, navigation au clavier.

## Modifier et consulter

Le contenu est dans `build.py`. Styles, images et scripts : `dist/assets/`.
Python 3 suffit à régénérer les pages, sans dépendance :

```sh
python build.py
python -m http.server 8792 --directory dist
```

Ouvrir http://localhost:8792/. Les liens absolus nécessitent un serveur HTTP.

## GitHub Pages

Le workflow `.github/workflows/pages.yml` génère le site, exporte les liens sous
le préfixe du dépôt et déploie sur GitHub Pages à chaque push sur `main`.
Aucun paquet npm nécessaire. GitHub Pages utilise la source GitHub Actions
dans les paramètres du dépôt.

```sh
python build.py
node export-pages.mjs
```

L’export est créé dans `outputs/pages/`. Adresse attendue après activation et
publication réussie : https://denisbtl.github.io/jade/.
Le préfixe utilise `GITHUB_REPOSITORY` ou `jade` par défaut.
Les sources restent utilisables à la racine sur un autre hébergeur.

## Vérification

`check_site.py`, `check_water.py` et `check_reading.py` nécessitent Playwright et Pillow. Avec un
serveur sur le port 8792, ils contrôlent les pages, le clavier, les liens, les
textes, le responsive, les animations, le clic/toucher, la pause, le mouvement réduit, la progression et les déplacements entre tableaux.
Choix visuels et critères UX/UI : `docs/CONCEPTION.md`.
Prompts des images : `assets-prompts.json`.

## Avant ouverture définitive

Textes et FAQ à valider par Jade. Coordonnées, adresse, horaires, tarifs, durée
et mentions légales complètes à renseigner. Le site reste marqué `noindex`.
Aucun formulaire ni suivi d’audience ajouté. Aucun jeton ou journal local livré.
