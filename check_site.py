"""Contrôles navigateur à lancer avec un serveur local sur le port 8792."""
import json
from pathlib import Path
from urllib.parse import urlsplit, unquote
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8792'
OUT = Path(__file__).parent / '.sites-runtime' / 'qa'
OUT.mkdir(parents=True, exist_ok=True)
routes = ['/', '/therapie/', '/mon-approche/', '/contact/']
errors, requests_failed, results = [], [], []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('requestfailed', lambda r: requests_failed.append(r.url))
    for width in [320, 390, 768, 1024, 1280, 1440]:
        page.set_viewport_size({'width': width, 'height': 900})
        for route in routes:
            response = page.goto(BASE + route)
            assert response.status == 200, (route, response.status)
            assert page.locator('h1').count() == 1
            assert page.locator('html').get_attribute('lang') == 'fr'
            assert page.locator('main p:not(.eyebrow):not(.hero-meta):not(.home-location):not(.small-note):not(.quote-signature)').evaluate_all('(els) => els.every(e => parseFloat(getComputedStyle(e).fontSize) >= 18)'), (route, width, 'paragraphes trop petits')
            assert page.locator('summary, .button, .text-link, .legal-open, .scene-next').evaluate_all('(els) => els.every(e => parseFloat(getComputedStyle(e).fontSize) >= 16)'), (route, width, 'contrôles trop petits')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (route, width, page.evaluate("Array.from(document.querySelectorAll('body *')).filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>({tag:e.tagName,cls:e.className,right:e.getBoundingClientRect().right,width:e.getBoundingClientRect().width})).slice(0,15)"))
            page.locator('img').evaluate_all('(images) => images.forEach(i => i.loading = "eager")')
            page.wait_for_function('Array.from(document.images).every(i => i.complete)')
            assert page.locator('img').evaluate_all('(images) => images.every(i => i.complete && i.naturalWidth > 0)'), route
            if width in [390, 1440]:
                slug = route.strip('/') or 'accueil'
                page.screenshot(path=str(OUT / f'{slug}-{width}.png'), full_page=True)
            results.append({'route': route, 'viewport': width, 'http': response.status, 'overflow': False})
    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto(BASE)
    toggle = page.get_by_role('button', name='Menu', exact=True)
    toggle.focus()
    page.keyboard.press('Enter')
    assert toggle.get_attribute('aria-expanded') == 'true'
    page.keyboard.press('Escape')
    assert toggle.get_attribute('aria-expanded') == 'false'
    assert toggle.evaluate('(el) => document.activeElement === el')
    toggle.click()
    page.locator('#navigation').get_by_role('link', name='La thérapie', exact=True).click()
    assert page.url == BASE + '/therapie/'
    summary = page.locator('summary').first
    summary.focus()
    page.keyboard.press('Enter')
    assert page.locator('details').first.get_attribute('open') is not None
    page.get_by_role('button', name='Informations du site').click()
    assert page.locator('dialog').is_visible()
    page.keyboard.press('Escape')
    assert not page.locator('dialog').is_visible()
    assert page.get_by_role('button', name='Informations du site').evaluate('(el) => document.activeElement === el')
    for route in routes:
        page.goto(BASE + route)
        links = page.locator('a[href^="/"]').evaluate_all('(links) => [...new Set(links.map(l => l.getAttribute("href")))]')
        for href in links:
            url = urlsplit(href)
            target = Path(__file__).parent/'dist'/url.path.lstrip('/')/'index.html'
            assert target.is_file(), (route, href)
            if url.fragment:
                assert f'id="{unquote(url.fragment)}"' in target.read_text(encoding='utf-8'), (route, href)
    assert not errors, errors
    assert not requests_failed, requests_failed
    zoom_page = browser.new_page(viewport={'width': 640, 'height': 450}, device_scale_factor=2)
    for route in routes:
        zoom_page.goto(BASE + route)
        assert zoom_page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (route, 'reflow 200%')
    zoom_page.goto(BASE)
    zoom_page.screenshot(path=str(OUT / 'accueil-equivalent-zoom-200.png'), full_page=True)
    page.set_viewport_size({'width': 1440, 'height': 1080})
    page.goto(BASE)
    page.locator('img').evaluate_all('(images) => images.forEach(i => i.loading = "eager")')
    page.wait_for_function('Array.from(document.images).every(i => i.complete)')
    page.screenshot(path=str(OUT / 'accueil-haut-v3.png'))
    browser.close()
report = {'pages': results, 'interactions': ['menu clavier', 'menu navigation', 'FAQ clavier', 'dialogue Échap et focus', 'liens et ancres internes', 'images'], 'javascript_errors': errors, 'requests_failed': requests_failed}
(OUT/'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
