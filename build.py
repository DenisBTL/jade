"""Génère les quatre pages statiques, sans dépendance ni données de visiteurs."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
NAV = [('/', 'Accueil'), ('/therapie/', 'La thérapie'), ('/mon-approche/', 'Mon approche'), ('/contact/', 'Me contacter')]
ARROW = '<span aria-hidden="true">↗</span>'

def button(text, href='/contact/', secondary=False):
    return f'<a class="button{(" secondary" if secondary else "")}" href="{href}">{text}{ARROW}</a>'

def icon(kind):
    paths = {
        'anxiete': '<path d="M8 35c-6-12 1-20 10-20 7 0 12 6 12 13 0 8-5 13-10 13-4 0-7-4-6-8 1-5 8-7 11-3M31 13l4-5m-1 14 7-2M9 10l-3-4"/>',
        'separation': '<path d="M24 41S5 31 5 18C5 5 20 5 24 15 28 5 43 5 43 18c0 13-19 23-19 23Z"/><path d="m25 13-5 10 8 5-6 10"/>',
        'relations': '<circle cx="14" cy="14" r="6"/><circle cx="35" cy="20" r="6"/><path d="M3 39v-6c0-11 22-11 22 0v6m2 0v-3c0-9 17-9 17 0v3M25 7l5-3m6 5 4-2"/>',
        'emotions': '<path d="M5 26c7-22 13-22 19 0s12 22 19 0M5 35c7-22 13-22 19 0M24 17c7-22 13-22 19 0"/>',
        'identite': '<path d="M17 43V32C1 28 8 5 24 5c16 0 21 16 15 24l-5 3v11M18 15c7-5 15 2 11 8-2 3-6 2-6 7m0 6v1"/>',
        'pin': '<path d="M39 20c0 12-15 24-15 24S9 32 9 20a15 15 0 1 1 30 0Z"/><circle cx="24" cy="20" r="5"/>',
        'presence': '<circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="6"/><path d="M24 2v5m0 34v5M2 24h5m34 0h5"/>',
        'ecoute': '<path d="M14 24c-7-14 1-20 10-20s17 10 11 20c-4 6-10 6-10 13 0 9-12 9-12 0m7-15c-3-6 1-11 5-9 7 3 0 9-3 12"/>',
    }
    return f'<svg class="line-icon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[kind]}</svg>'

TOPICS = [
    ('anxiete', 'Anxiété', 'Quand les inquiétudes prennent de la place et qu’il devient difficile de souffler.'),
    ('separation', 'Séparations', 'Lorsqu’un lien change, se termine, et qu’un nouvel équilibre reste à trouver.'),
    ('relations', 'Difficultés relationnelles', 'Pour explorer votre manière d’être en lien avec les autres et avec vous-même.'),
    ('emotions', 'Émotions', 'Pour donner une place à ce que vous ressentez, même lorsque tout semble se mélanger.'),
    ('identite', 'Questions identitaires', 'Pour prendre le temps de questionner qui vous êtes et ce qui vous ressemble.'),
]

def topics(full=False):
    return f'<div class="topics{(" detailed" if full else "")}">' + ''.join(f'<article class="topic">{icon(k)}<h3>{t}</h3>{f"<p>{d}</p>" if full else ""}</article>' for k,t,d in TOPICS) + '</div>'

FAQ = [
    ('Qu’est-ce que la Gestalt-thérapie ?', 'La Gestalt est une approche qui s’intéresse à la manière dont vous vivez les situations et entrez en relation. Elle accueille les pensées, les émotions et les sensations corporelles, avec une attention particulière à ce qui se passe dans le présent.'),
    ('Je n’ai jamais fait de thérapie. Par où commencer ?', 'Vous n’avez rien à préparer et vous n’avez pas besoin de trouver les mots justes. Une première rencontre permet de parler de ce qui vous amène, de poser vos questions et de faire connaissance.'),
    ('Comment se déroule une séance ?', 'La séance est un temps d’échange à partir de ce que vous souhaitez apporter : une situation, une émotion, un questionnement. Nous prenons le temps d’observer ensemble ce qui se passe pour vous, à votre rythme.'),
    ('Est-il possible de consulter en visio ?', 'Un accompagnement en visioconférence est envisageable après une première séance en présentiel. Les modalités seront discutées ensemble.'),
    ('Quels sont les tarifs et la durée d’une séance ?', 'Le tarif et la durée des séances seront précisés prochainement, avant toute prise de rendez-vous.'),
]

def faq(all=False):
    selected = FAQ if all else FAQ[:3]
    return '<div class="faq-list">' + ''.join(f'<details><summary>{q}<span aria-hidden="true">+</span></summary><p>{a}</p></details>' for q,a in selected) + '</div>'

def cta():
    return '<section class="closing"><div class="wrap closing-inner"><div><p class="eyebrow">LE PREMIER PAS VOUS APPARTIENT</p><h2>Et si nous prenions<br>le temps d’en parler ?</h2></div>' + button('Les informations pratiques') + '</div></section>'

HOME = '''<section class="home-hero">
  <img class="home-landscape" src="/assets/paysage-kintsugi-v3.webp" alt="" width="1774" height="887" fetchpriority="high">
  <canvas class="home-water-canvas" aria-hidden="true"></canvas>
  <button class="water-splash" type="button" aria-label="Créer une grande onde dans l’eau" hidden><span class="water-splash-desktop">Cliquer sur l’eau</span><span class="water-splash-mobile">Toucher l’eau</span></button>
  <button class="water-toggle" type="button" aria-pressed="false" aria-label="Mettre les animations du paysage en pause" hidden><span class="water-toggle-icon" aria-hidden="true">Ⅱ</span><span class="water-toggle-text">Pause</span></button>
  <div class="wrap home-hero-inner"><div class="home-hero-copy">
    <h1>Un espace pour vous<br>rencontrer autrement</h1>
    <p class="home-hero-intro">Prendre le temps d’écouter ce qui se passe<br>ici et maintenant.</p>''' + button('Se rencontrer') + '''
  </div><p class="home-location"><span aria-hidden="true"></span>GESTALT-THÉRAPEUTE · RENNES</p></div>
</section>
<section class="home-accompaniments"><div class="section wrap"><div class="section-heading"><div><p class="eyebrow">ACCOMPAGNEMENT INDIVIDUEL · ADULTES</p><h2>Un espace pour<br>ce que vous traversez.</h2></div><p class="section-aside">J’accompagne les adultes à Rennes. Nous explorons ensemble les situations qui vous préoccupent et la manière dont vous les vivez.</p></div>''' + topics() + '''<a class="text-link" href="/therapie/#accompagnements">Découvrir les accompagnements <span aria-hidden="true">↗</span></a></div></section>
<section class="approach-band"><div class="wrap approach-grid"><img class="home-approach-image" src="/assets/petales-v3.webp" alt="" width="900" height="600" loading="lazy"><div class="approach-copy"><p class="eyebrow">JADE D’ALBENAS · MON APPROCHE</p><h2>Éclairer ensemble.</h2><p>« J’aime penser mon accompagnement comme une lampe torche que l’on tient ensemble dans le travail thérapeutique. »</p><p>Éclairer progressivement ce qui est là, sans savoir à votre place. Voir ce qui peut être ajusté, compris ou transformé.</p><a class="text-link" href="/mon-approche/">Faire connaissance <span aria-hidden="true">↗</span></a></div></div></section>
<section class="home-questions"><div class="section wrap faq-section"><div><p class="eyebrow">VOS PREMIÈRES QUESTIONS</p><h2>Avant de<br>se rencontrer.</h2></div><div>''' + faq() + '''<a class="text-link" href="/therapie/#questions">Toutes les questions <span aria-hidden="true">↗</span></a></div></div></section>'''

THERAPIE = '''<section class="page-hero wrap"><p class="eyebrow">LA THÉRAPIE · POUR LES ADULTES</p><h1>Se comprendre.<br><em>Ouvrir d’autres possibles.</em></h1><p class="lead">Un espace pour explorer ce que vous traversez,<br>en portant attention à ce qui se vit ici et maintenant.</p></section>
<section class="section soft"><div class="wrap editorial"><div><p class="eyebrow">LA GESTALT</p><h2>Vous accueillir<br>dans votre globalité.</h2></div><div><p class="large-copy">Ce que vous pensez, ce que vous ressentez, ce qui se passe dans votre corps : tout cela a sa place.</p><p>La Gestalt porte une attention à votre expérience présente et à la façon dont vous entrez en relation avec votre environnement. Le dialogue permet d’explorer ensemble vos ressentis, vos besoins et vos manières de vivre les situations.</p><p>Il ne s’agit pas d’arriver avec un récit bien ordonné. Nous partons de ce qui est là, pour vous, au moment de la rencontre.</p><a class="text-link" href="https://www.epg-gestalt.fr/">En savoir plus auprès de l’EPG <span aria-hidden="true">↗</span></a></div></div></section>
<section class="section wrap" id="accompagnements"><p class="eyebrow">MES ACCOMPAGNEMENTS</p><h2>Ce que l’on peut explorer ensemble.</h2><p class="intro-width">J’accompagne les adultes autour de ces questionnements. Ils peuvent se croiser, évoluer ou simplement vous aider à mettre des mots sur ce que vous traversez.</p>''' + topics(True) + '''</section>
<section class="section navy"><div class="wrap"><p class="eyebrow">LE TEMPS D’UNE SÉANCE</p><h2>Une rencontre, pas à pas.</h2><div class="steps"><article><span>01</span><h3>Faire connaissance</h3><p>Une première séance en présentiel pour parler de ce qui vous amène et poser vos questions.</p></article><article><span>02</span><h3>Explorer ensemble</h3><p>Mettre des mots sur votre vécu, avec une attention à vos émotions et à vos sensations.</p></article><article><span>03</span><h3>Avancer à votre rythme</h3><p>Prendre le temps de sentir ce qui vous convient. Les modalités du suivi se discutent ensemble.</p></article></div></div></section>
<section class="section wrap faq-section" id="questions"><div><p class="eyebrow">QUESTIONS FRÉQUENTES</p><h2>Quelques repères<br><em>pour commencer.</em></h2></div><div>''' + faq(True) + '''</div></section>''' + cta()

APPROCHE = '''<section class="page-hero wrap"><p class="eyebrow">MON APPROCHE · JADE D’ALBENAS</p><h1>La rencontre,<br><em>comme point de départ.</em></h1><p class="lead">Une présence attentive. Un travail à deux.<br>Une place pour votre singularité.</p></section>
<section class="approach-band"><div class="wrap approach-grid"><div class="quote-art" aria-hidden="true"><img src="/assets/embleme.webp" alt="" width="850" height="600"><span class="quote-art-word">ensemble.</span></div><div class="approach-copy"><p class="eyebrow">MA POSTURE</p><h2>Tenir la lampe<br><em>torche à deux.</em></h2><blockquote>« J’aime penser mon accompagnement comme une lampe torche que l’on tient ensemble dans le travail thérapeutique : il ne s’agit pas de “savoir à la place de”, mais d’éclairer progressivement ce qui est là, et de voir ce qui peut être ajusté, compris ou transformé. »</blockquote><p class="quote-signature">Jade d’Albenas</p></div></div></section>
<section class="section wrap editorial"><div><p class="eyebrow">L’INSPIRATION KINTSUGI</p><h2>Faire une place<br>à son histoire.</h2></div><div><p class="large-copy">Les lignes dorées qui relient les fragments du logo racontent cette inspiration.</p><p>Le kintsugi est un art japonais qui souligne les lignes de réparation des céramiques avec de l’or. Cette image résonne avec ma manière d’envisager l’accompagnement : accueillir les différentes parts de son histoire et les liens qui se tissent entre elles.</p><p>Une invitation à se rencontrer avec ce que l’on est aujourd’hui, plutôt qu’à chercher un modèle auquel se conformer.</p></div></section>
<section class="section soft"><div class="wrap"><p class="eyebrow">LES REPÈRES DE NOTRE RENCONTRE</p><h2>Une présence qui vous laisse de la place.</h2><div class="values"><article>''' + icon('ecoute') + '''<h3>L’écoute</h3><p>Accueillir vos mots, vos silences et ce qui cherche encore à se dire.</p></article><article>''' + icon('presence') + '''<h3>Le présent</h3><p>Porter attention à ce que vous vivez dans la rencontre, ici et maintenant.</p></article><article>''' + icon('relations') + '''<h3>La relation</h3><p>Explorer ensemble, dans un dialogue qui respecte votre expérience.</p></article></div></div></section>
<section class="section wrap editorial" id="accueil-inclusif"><div><img class="pride" src="/assets/accueil-inclusif.webp" alt="Drapeau des fiertés Progress Pride" width="72" height="72" loading="lazy"><p class="eyebrow">UN ACCUEIL INCLUSIF</p><h2>Votre singularité<br>a sa place.</h2></div><div><p class="large-copy">Un accueil respectueux des personnes LGBTQIA+.</p><p>Votre orientation, votre identité de genre et vos questionnements peuvent trouver leur place dans cet espace, sans présupposé sur votre parcours ou vos relations.</p><p>Nous prenons le temps d’explorer ce qui compte pour vous, dans le respect de votre manière de vous définir.</p></div></section>
<section class="section soft"><div class="wrap editorial"><div><p class="eyebrow">MA PRATIQUE</p><h2>Un accompagnement<br>supervisé.</h2></div><div><p class="large-copy">Gestalt-thérapeute supervisée à l’École Parisienne de Gestalt.</p><p>La supervision constitue un espace de recul et de réflexion sur ma pratique. Le cadre de l’accompagnement et ses modalités seront présentés lors de notre première rencontre.</p></div></div></section>''' + cta()

CONTACT = '''<section class="page-hero wrap"><p class="eyebrow">ME CONTACTER · LES INFORMATIONS PRATIQUES</p><h1>Faire le premier pas,<br><em>à votre rythme.</em></h1><p class="lead">Une première rencontre pour faire connaissance<br>et prendre le temps de poser vos questions.</p></section>
<section class="section soft"><div class="wrap contact-grid"><div><p class="eyebrow">RENDEZ-VOUS</p><h2>Bientôt,<br><em>les premiers échanges.</em></h2><p>Les coordonnées professionnelles et les modalités de prise de rendez-vous seront communiquées prochainement.</p><div class="status-note"><span aria-hidden="true"></span>Coordonnées à venir</div><p class="small-note">Aucune réservation n’est ouverte sur ce site pour le moment.</p></div><div class="practice-info"><h3>Votre accompagnement</h3><dl><div><dt>Pour qui ?</dt><dd>Adultes, en individuel</dd></div><div><dt>Où ?</dt><dd>À Rennes</dd></div><div><dt>En visio ?</dt><dd>Possible après une première séance en présentiel</dd></div><div><dt>Durée & tarif</dt><dd>À préciser avant la prise de rendez-vous</dd></div></dl></div></div></section>
<section class="section wrap contact-grid"><div class="rennes-map" aria-label="Localisation indicative : Rennes, sans adresse de cabinet définie"><svg viewBox="0 0 540 380" fill="none" aria-hidden="true"><rect width="540" height="380" fill="#e9e8ee"/><g stroke="#f8f7f3" stroke-width="18"><path d="M-20 100 560 290M130-20 270 400M430-20 280 400M-20 310 560 80M-20 20 560 220M30-20 490 400"/><path d="M-20 210Q170 170 240 220T570 180" stroke="#b8c8d8" stroke-width="26"/></g><circle cx="275" cy="185" r="52" fill="#273873" fill-opacity=".06"/><circle cx="275" cy="185" r="28" fill="#273873" fill-opacity=".1"/><circle cx="275" cy="185" r="9" fill="#273873"/><circle cx="275" cy="185" r="4" fill="#f8f7f3"/></svg><span class="map-label">Rennes<span>Localisation indicative</span></span></div><div><p class="eyebrow">LE CABINET</p><h2>Se retrouver<br><em>à Rennes.</em></h2><p>Le lieu du cabinet est en cours de définition. L’adresse exacte, les horaires, les transports à proximité et les conditions d’accessibilité seront précisés une fois le lieu confirmé.</p><p class="small-note">Le repère représente la ville de Rennes, pas l’emplacement du futur cabinet.</p><a class="text-link" href="https://www.openstreetmap.org/search?query=Rennes">Situer Rennes sur la carte <span aria-hidden="true">↗</span></a></div></section>
<section class="section wrap faq-section"><div><p class="eyebrow">AVANT LA PREMIÈRE RENCONTRE</p><h2>Vous n’avez pas<br>à tout savoir déjà.</h2></div><div>''' + faq() + '''<a class="text-link" href="/therapie/#questions">Voir toutes les questions <span aria-hidden="true">↗</span></a></div></section>'''

def page(path, title, description, content):
    content = content.replace('<br>', '<br> ')
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if path==url else '')+f'>{label}</a>' for url,label in NAV)
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f8f7f3"><title>{escape(title)}</title><meta name="description" content="{escape(description)}"><meta name="robots" content="noindex, nofollow"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><link rel="icon" type="image/webp" href="/assets/favicon.webp"><link rel="stylesheet" href="/assets/style.css"><script defer src="/assets/site.js"></script></head>
<body><a class="skip-link" href="#contenu">Aller au contenu</a>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="/" aria-label="Jade d’Albenas, accueil"><img src="/assets/favicon.webp" alt="" width="55" height="55"><span>Jade <span class="brand-family">d’Albenas</span><small>GESTALT-THÉRAPEUTE</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation"><span>Menu</span><span class="menu-lines" aria-hidden="true"></span></button><nav id="navigation" aria-label="Navigation principale">{nav}</nav><a class="header-cta" href="/contact/">Se rencontrer {ARROW}</a></div></header>
<main id="contenu">{content}</main>
<footer><div class="wrap footer-top"><div><a class="footer-name" href="/">Jade d’Albenas</a><p>Gestalt-thérapeute · Rennes<br>Accompagnement individuel des adultes</p><a class="inclusive-link" href="/mon-approche/#accueil-inclusif"><img src="/assets/accueil-inclusif.webp" width="25" height="25" alt="Drapeau des fiertés">Un accueil inclusif</a></div><div><h2>Explorer</h2>{nav}</div><div><h2>Le cabinet à Rennes</h2><p>Adresse, accès et horaires à venir.<br>Visio possible après une première<br>séance en présentiel.</p><a href="/contact/">Les informations pratiques ↗</a></div></div><div class="wrap footer-bottom"><p>© 2026 Jade d’Albenas</p><p>Écoute · Présence · Relation</p><button class="legal-open" type="button">Informations du site</button></div></footer>
<dialog id="legal"><button class="legal-close" autofocus aria-label="Fermer les informations du site">×</button><p class="eyebrow">INFORMATIONS DU SITE</p><h2>Une première version<br>pour faire connaissance.</h2><p>Ce site présente le projet de Jade d’Albenas, Gestalt-thérapeute à Rennes. Les coordonnées professionnelles, l’adresse, les tarifs et les mentions légales complètes restent à renseigner avant une ouverture publique.</p><p>Ce site ne comporte aucun formulaire, aucun outil de mesure d’audience et aucun traceur ajouté par son code. Les liens vers d’autres sites vous font quitter ce site.</p><p>Textes de présentation et FAQ à relire et à valider par Jade avant publication publique.</p><p>Les visuels de l’identité graphique ont été fournis pour ce projet.</p></dialog>
</body></html>'''

PAGES = [
    ('/', 'Jade d’Albenas · Gestalt-thérapeute à Rennes', 'Un espace pour vous rencontrer autrement. Accompagnement individuel des adultes en Gestalt-thérapie à Rennes.', HOME),
    ('/therapie/', 'La thérapie · Jade d’Albenas', 'Découvrir la Gestalt, les accompagnements pour adultes et les réponses aux questions avant une première séance.', THERAPIE),
    ('/mon-approche/', 'Mon approche · Jade d’Albenas', 'Une présence attentive, une inspiration kintsugi et un accueil inclusif. Découvrir l’approche de Jade d’Albenas.', APPROCHE),
    ('/contact/', 'Me contacter · Jade d’Albenas à Rennes', 'Les informations pratiques sur le futur cabinet à Rennes, les séances et les coordonnées à venir.', CONTACT),
]
for path,title,description,content in PAGES:
    folder = DIST / path.strip('/')
    folder.mkdir(parents=True, exist_ok=True)
    html = page(path,title,description,content).replace('/assets/style.css', '/assets/style.css?v=2')
    if path == '/':
        html = html.replace('<body>', '<body class="home">').replace('</head>', '<link rel="stylesheet" href="/assets/home-v3.css?v=9"><script defer src="/assets/home-water.js?v=9"></script></head>')
    (folder/'index.html').write_text(html, encoding='utf-8')
(DIST/'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
(DIST/'404.html').write_text(page('', 'Page introuvable · Jade d’Albenas', 'Retrouver le site de Jade d’Albenas.', '<section class="page-hero wrap"><p class="eyebrow">PAGE INTROUVABLE</p><h1>Reprenons<br><em>le fil.</em></h1><p>Cette page n’existe pas ou a été déplacée.</p>'+button('Revenir à l’accueil','/')+'</section>').replace('/assets/style.css', '/assets/style.css?v=2'), encoding='utf-8')
print(f'{len(PAGES)} pages et une page 404 générées dans {DIST}')
