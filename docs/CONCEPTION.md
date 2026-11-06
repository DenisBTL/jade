# Site de Jade d’Albenas

Site vitrine autonome du dépôt indépendant DenisBTL/jade.
Quatre pages statiques : accueil, thérapie, approche, contact. Aucun serveur
applicatif, formulaire de santé ou stockage de données de visiteurs.

## Contenus

Sources : export Notion de sept pages et visuels téléchargés le 6 novembre 2026
entre 9 h 50 et 9 h 55. Emblème et drapeau fournis, optimisés en WebP. Les captures
des autres thérapeutes sont des références, elles ne sont pas reproduites.
L’accueil reprend ensuite la composition de la planche fournie par Denis :
paysage bleu/lilas et fil d’or, titre à gauche, bandeau de pétales, d’eau et
d’ombres végétales, puis les quatre repères Écoute, Présence, Mouvement, Intégration.
Trois images ont été créées avec l’outil intégré image_gen, puis converties en WebP :
`dist/assets/paysage-kintsugi-v3.webp`, `dist/assets/petales-v3.webp` et
`dist/assets/ombres-vegetales-v3.webp`. Les prompts exacts figurent dans
`assets-prompts.json`. Le logo fourni reste inchangé.
Les textes et la FAQ proposés développent le brief et restent à valider par Jade.
La présentation générale de la Gestalt renvoie à https://www.epg-gestalt.fr/.

Le brief ne fournit ni portrait, ni coordonnées, ni tarif, ni durée, ni adresse
définitive. Ces informations restent explicitement à venir. Le dessin de carte
est schématique et localise la ville uniquement. Le titre de psychologue ou une
certification non fournie ne sont pas attribués à Jade.

## Modifier et consulter

- Contenu et structure partagée : `build.py` (Python 3, bibliothèque standard).
- Style : `dist/assets/style.css` ; interactions : `dist/assets/site.js`.
- Style propre au nouvel accueil : `dist/assets/home-v3.css` ; il n’est chargé
  que sur `/` pour préserver la composition des trois autres pages.
- Reflets de l’eau : `dist/assets/home-water.js`, sans dépendance externe ;
  déformation Canvas 2D limitée au lac, 24 images/s au maximum, canevas limité à
  900 pixels de large. WebGL et l’accélération graphique ne sont pas requis.
- Génération : `python build.py`.
- Consultation : `python -m http.server 8792 --directory dist`, puis
  http://localhost:8792/ (ouvrir les fichiers directement ne résout pas les liens absolus).
- Export GitHub Pages : `node export-pages.mjs`, sortie `outputs/pages/`.

## Préconisation UX/UI : version de présentation

- Problème utilisateur : découvrir l’approche de Jade et comprendre comment
  envisager une première séance alors que son installation est encore en préparation.
- Comportement : navigation entre quatre pages et accès aux informations pratiques ;
  aucune réservation proposée tant que les coordonnées ne sont pas fournies.
- Priorité / risque : P1 pour la lisibilité et l’honnêteté des informations pratiques.
- Point d’entrée : accueil, navigation, appels à découvrir l’approche et se rencontrer.
- Hiérarchie : approche et public accompagné, motifs, déroulement, questions, contact.
- États : page courante signalée ; FAQ repliée/dépliée ; menu mobile fermé/ouvert ;
  informations de contact partielles explicitement annoncées ; page 404 avec retour.
  Pas d’état de chargement, de succès d’envoi ou de permission applicative car aucun
  formulaire ni appel de données n’est présent.
- Feedback : chevron de FAQ, menu avec `aria-expanded`, dialogue d’information
  refermable au clavier ; aucun faux message de réservation ou d’envoi.
- Données : identité et public issus du brief ; adresse, horaires, durée et tarifs
  non inventés ; ville indicative clairement identifiée.
- Responsive : navigation compacte et colonnes empilées ; contrôles à 320, 390,
  768 et 1440 pixels ; absence de défilement horizontal.
- Accessibilité : lien d’évitement, titres structurés, navigation nommée, focus
  visible, images décrites, FAQ native, fermeture avec Échap, aucune animation au scroll.
- Lisibilité révisée : paragraphes à 18 px minimum, introduction à 19–20 px,
  contrôles et navigation à 16 px minimum, FAQ à 18 px. Titres principaux ramenés
  à 60 px sur ordinateur et 36–44 px sur téléphone, titres secondaires à 32–38 px.
  Les libellés de section restent à 14 px et les informations de pied de page
  à 16 px, hors copyright à 14 px. Corps assombri et contraste renforcé.
- Composition révisée : largeur utile de 1 160 px, visuel d’accueil contenu,
  espacement des sections de 48 à 76 px ; accompagnements détaillés en trois,
  deux puis une colonne selon la largeur, pour éviter les colonnes de texte étroites.
- Cohérence : identité propre à Jade (ivoire, bleu, lilas, or), sans reprise des
  composants métier Mon Chai puisqu’il s’agit d’un site autonome.

### Critères d’acceptation UX/UI

1. Les quatre pages et leurs images chargent et tous les liens internes aboutissent.
2. Les visiteurs retrouvent les accompagnements, la FAQ et les informations pratiques.
3. L’absence de coordonnées ne peut pas être prise pour un système de réservation.
4. Le menu fonctionne au clavier et sur mobile ; la FAQ et le dialogue sont utilisables.
5. Aucun débordement à 320, 390, 768 et 1440 pixels ; captures de référence dans
   `.sites-runtime/qa/`, exclues des sources publiées et de l’archive d’hébergement.
6. Vérifier aussi 1024 et 1280 px, les tailles de paragraphes et contrôles calculées
   dans le navigateur, ainsi que le reflow équivalent à une fenêtre de 1280 px
   zoomée à 200 % (surface CSS 640 × 450, densité 2).

### Préconisation UX/UI : accueil selon la référence visuelle

- Problème : la première composition ne traduisait pas l’univers de la charte fournie.
- Priorité / risque : P1, cohérence visuelle et lisibilité de la première impression.
- Point d’entrée : `/`, logo et lien Accueil ; les routes existantes sont conservées.
- Hiérarchie : navigation sur le paysage, titre et introduction à gauche, action
  « Se rencontrer », localisation, triptyque visuel puis repères de l’approche.
- États : menu mobile fermé/ouvert et route courante ; pas de défilement animé.
  Les images sont décoratives, les textes et liens restent disponibles indépendamment.
- Feedback : retour visuel au survol/focus, ouverture du menu et accès effectif à
  la page contact ; le bouton ne simule aucune réservation.
- Données : textes du brief, ville de Rennes ; aucune coordonnée ajoutée.
- Responsive : paysage recadré et texte sur fond éclairci sur téléphone ; bandeau
  de trois détails conservé et repères redisposés en deux colonnes.
- Accessibilité : texte courant de 18–20 px, action de 16 px minimum, images
  décoratives exclues de la lecture vocale, contenu réel en HTML, focus visible,
  contraste du texte protégé par un voile clair sur le paysage en petit écran.
- Cohérence : palette, emblème et références kintsugi conservés, images fixes.
- Critères : vérifier six largeurs et le reflow équivalent à 200 %, navigation,
  liens et tailles calculées ; comparer la capture `accueil-haut-v3.png` à la
  référence fournie, ainsi que le rendu complet sur mobile.

## Préconisation UX/UI : accueil épuré et eau animée

- Problème : les grands aplats presque blancs et les répétitions décoratives
  alourdissent l’accueil ; Denis demande maintenant une ondulation relaxante de l’eau.
- Priorité / risque : P1 pour la cohérence et la lisibilité ; animation non essentielle.
- Point d’entrée : paysage de `/`, commande de pause en bas à droite de l’image.
- Hiérarchie : accueil, accompagnements pour adultes, approche de Jade, FAQ.
  Retirer le triptyque décoratif, les quatre mots isolés, l’introduction et la
  citation qui répètent le titre, ainsi que le dernier appel à l’action redondant.
- États : eau animée, pause manuelle, préférence de mouvement réduit, image statique
  sans JavaScript ou Canvas 2D ; arrêt des calculs hors écran et lorsque l’onglet est caché.
- Feedback : bouton « Pause » puis « Reprendre », état `aria-pressed`
  et focus visible. En absence de capacité graphique, seule l’image fixe est montrée.
- Données : image et textes existants ; aucune nouvelle collecte ni route.
- Responsive : ondulation calculée dans les coordonnées de l’image pour conserver
  le même rivage après recadrage ; texte et montagnes immobiles sur tous les formats.
- Accessibilité : mouvement de faible amplitude, arrêt utilisateur, respect de
  `prefers-reduced-motion`, canevas décoratif masqué aux lecteurs d’écran ; texte
  de 18 px minimum et commande de 16 px minimum sur fond suffisamment contrasté.
- Cohérence : à la demande de Denis, les fonds de l'accueil sont ivoire, beige
  et sable chaud, pied de page compris. Le paysage et les couleurs du texte
  conservent l'identité de Jade. Les séparateurs et commandes prennent des tons
  chauds assortis ; vérifier la lisibilité du pied de page sur ordinateur et mobile.
- Critères : eau visiblement modifiée entre deux captures espacées, montagnes
  inchangées ; pause réellement figée, préférence de mouvement réduit statique,
  absence de Canvas sans erreur ; contrôles habituels sur six largeurs et à 200 %.
- Vérification : `check_water.py` contrôle les pixels, les clics/touchers, la
  commande au clavier et l’arrêt des rendus sur téléphone et ordinateur dans
  Chromium sans réglage graphique particulier. L’effet reste fonctionnel lorsque
  WebGL est désactivé ; la dégradation sans Canvas et sans JavaScript est vérifiée.

### Préconisation UX/UI : grande onde au clic

- Problème : Denis ne voit pas l'ondulation ; elle dépendait de WebGL et restait
  trop discrète. Priorité P1 : un effet demandé doit être perceptible et accessible.
- Point d'entrée : surface de l'eau sur l'accueil, indication « Toucher l'eau »
  sur mobile / « Cliquer sur l'eau » sur ordinateur et activation au clavier.
- Hiérarchie : interaction décorative après le texte ; aucune action de navigation
  ou réservation n'est interceptée.
- États : ondulation de repos, forte onde au clic puis amortissement en cinq
  secondes, pause/reprise, préférence de mouvement réduit et image de secours.
- Feedback : déformation de plusieurs dizaines de pixels centrée sur l'interaction,
  bouton Pause/Reprendre. Une interaction sur l'eau relance le mouvement en pause.
- Données : coordonnées du clic utilisées uniquement en mémoire, sans collecte.
- Responsive : même effet sur clic et toucher, calculé après le recadrage de l'image.
- Accessibilité : vraie zone bouton activable par Entrée/Espace, label explicite,
  indication de 16 px, montagnes/textes fixes, pause et mouvement réduit conservés.
- Cohérence : mêmes couleurs et paysage ; rendu Canvas 2D sans exigence WebGL.
- Critères : interaction réellement testée sur ordinateur et mobile, effet bien
  supérieur au mouvement de repos, arrêt progressif, montagne inchangée, pause
  stable et effet fonctionnel même lorsque WebGL est désactivé.

### Préconisation UX/UI : brise dans les feuillages

- Problème / priorité : P2, Denis souhaite une légère brise et de petites feuilles
  qui tombent dans les arbres du paysage, sans déplacer tout le décor.
- Point d'entrée : paysage de l'accueil, même commande Pause/Reprendre que l'eau.
- Hiérarchie : feuillages de la rive droite et quelques feuilles discrètes ;
  le texte, les montagnes et les boutons restent immobiles et lisibles.
- États : animation, pause globale, onglet caché / paysage hors écran et mouvement
  réduit ; image fixe sans JavaScript ou Canvas, sans nouvelle action obligatoire.
- Feedback : la commande existante annonce désormais la pause des animations
  du paysage et fige l'eau, la brise et les feuilles ensemble.
- Données : coordonnées et couleurs décoratives définies localement, sans collecte.
- Responsive : arbres et origines des feuilles repérés dans les coordonnées de
  l'image, pour suivre le recadrage mobile ; moins de feuilles sur petit écran.
- Accessibilité : canevas décoratif, aucun obstacle aux clics, pause clavier
  conservée, `prefers-reduced-motion` respecté, pas de clignotement.
- Cohérence : feuilles petites, dans les tons lilas, gris bleuté et or doux du
  paysage ; fonds ivoire/beige conservés, aucun nouvel aplat bleu.
- Critères : mouvements de feuillage visibles entre deux captures, feuilles
  localisées sur la rive ; ciel et montagnes inchangés ; pause et mouvement réduit
  figent tous les effets ; grandes ondes au clic toujours fonctionnelles.

## Avant ouverture publique

Faire valider les textes, le cadre de la pratique et les droits des visuels par
Jade ; renseigner les coordonnées, tarif, durée, adresse, accès PMR, horaires et
mentions légales complètes ; choisir le domaine et la prise de rendez-vous. Le site
est livré pour consultation privée, avec `noindex` et `robots.txt` restrictif.
Ces balises ne remplacent pas le contrôle d’accès privé de l’hébergeur.


## Préconisation UX/UI : dépôt autonome

- Priorité / problème : P1, séparer le site de Jade des autres projets.
- Point d’entrée : `/jade/` sur GitHub Pages, racine sur un hébergement autonome.
- Hiérarchie : quatre pages et navigation existantes.
- États et feedback : export des liens et ressources sous le bon préfixe,
  coordonnées à venir, FAQ, page 404, pause et reprise du paysage.
- Données : contenus fournis et proposés, aucun renseignement professionnel inventé.
- Responsive : affichage téléphone et ordinateur identique, sans débordement.
- Accessibilité : clavier, titres structurés, contrastes et mouvement réduit.
- Critères : quatre pages et ressources disponibles sous `/jade/`, navigation et
  animations actives, compilation sans dépendance npm ni donnée de connexion.


## Préconisation UX/UI : accueil sans cadre extérieur

- Priorité / problème : P1, Denis demande un accueil sans bord visible autour du site.
- Point d’entrée : accueil `/jade/`, dès le haut de la fenêtre.
- Hiérarchie : paysage et fonds des sections pleine largeur ; les textes conservent
  des marges intérieures pour leur lisibilité et leur alignement.
- États et feedback : même contenu, navigation, eau interactive, brise et pause ;
  suppression des marges extérieures, limites de largeur et arrondis des sections.
- Données : aucune modification des informations ni des coordonnées manquantes.
- Responsive : paysage au bord gauche et droit à 320, 390, 768, 1440 et 1920 px ;
  pied de page pleine largeur et aucun défilement horizontal.
- Accessibilité : focus visibles et formes des boutons conservés ; texte de taille
  et largeur lisibles, mouvement réduit toujours respecté.
- Critères : paysage à x=0, y=0, largeur de fenêtre et rayon nul ; sections et pied
  de page sans cadre extérieur sur téléphone et grand écran ; animations actives.


## Préconisation UX/UI : fondus des tableaux et vent dans la végétation

- Priorité / problème : P1, les changements de fond sont trop francs et le mouvement
  doit surtout se lire dans les arbres de la rive, comme demandé par Denis.
- Point d’entrée : parcours vertical de l’accueil ; végétation à droite du paysage.
- Hiérarchie : fondus statiques entre les tableaux, sans apparition au scroll ;
  vent plus net dans les couronnes et feuilles issues des arbres, eau calme au repos.
- États et feedback : pause globale, reprise, clic dans l’eau, mouvement réduit et
  image fixe de secours ; aucun nouveau contrôle ou écran.
- Données : visuel fourni au projet et feuilles décoratives, sans collecte.
- Responsive : fondus adaptés à la hauteur disponible ; végétation et feuilles
  recadrées avec l’image sur téléphone ; paysage toujours bord à bord.
- Accessibilité : lisibilité des textes et des contrôles protégée, aucun clignotement,
  pause et mouvement réduit respectés ; les fondus restent statiques.
- Cohérence : dégradés dans les tons ivoire, beige et sable, aucun cadre ajouté.
- Critères : pas de rupture de couleur aux jonctions ; arbres visiblement animés
  sans mouvement du ciel ou des montagnes ; feuilles issues de la zone boisée ;
  pause stable, grandes ondes toujours possibles et aucun débordement horizontal.
