"""Vérifie les pixels : mouvement de repos, grande onde au clic, pause et secours."""
from io import BytesIO
from pathlib import Path
import json
from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / '.sites-runtime' / 'qa'
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'http://127.0.0.1:8792/'

def capture(page):
    return Image.open(BytesIO(page.locator('.home-hero').screenshot())).convert('RGB')

def difference(a, b, area, threshold=2):
    pixels = ImageChops.difference(a.crop(area), b.crop(area))
    return sum(1 for rgb in pixels.get_flattened_data() if max(rgb) > threshold)

def mean_difference(a, b, area):
    return sum(ImageStat.Stat(ImageChops.difference(a.crop(area), b.crop(area))).mean) / 3

report = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for width in [390, 1440]:
        page = browser.new_page(viewport={'width': width, 'height': 1000}, has_touch=width == 390)
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.add_init_script("window.__waterDraws = 0; window.__waveFrames = 0; const draw = CanvasRenderingContext2D.prototype.drawImage; const put = CanvasRenderingContext2D.prototype.putImageData; CanvasRenderingContext2D.prototype.drawImage = function(...a) { window.__waterDraws++; return draw.apply(this,a); }; CanvasRenderingContext2D.prototype.putImageData = function(...a) { window.__waveFrames++; return put.apply(this,a); };")
        page.goto(BASE)
        page.wait_for_selector('.home-water-canvas.is-ready')
        page.wait_for_timeout(200)
        first = capture(page)
        page.wait_for_timeout(700)
        second = capture(page)
        w, h = first.size
        top_area = (0, 0, w, int(h * .50))
        foliage_area = (int(w * .55), int(h * .55), w - 5, int(h * .76))
        water_area = (20, int(h * .83), w - 20, h - 65)
        top = difference(first, second, top_area)
        idle = difference(first, second, water_area)
        local_area = (max(20, int(w * .56 - 180)), int(h * .83), min(w - 20, int(w * .56 + 180)), h - 65)
        idle_mean = mean_difference(first, second, local_area)
        foliage_changes = difference(first, second, foliage_area)
        assert foliage_changes > 20, (width, 'Feuillages immobiles', foliage_changes)
        assert top == 0, (width, 'Le haut du paysage bouge', top)
        assert idle > 50, (width, 'Eau immobile', idle)
        before_click = capture(page)
        rect = page.locator('.home-hero').bounding_box()
        click_x, click_y = rect['x'] + w * .56, rect['y'] + h * .90
        if width == 390:
            page.touchscreen.tap(click_x, click_y)
        else:
            page.mouse.click(click_x, click_y)
        page.wait_for_timeout(230)
        clicked = capture(page)
        strong = difference(before_click, clicked, water_area, threshold=8)
        strong_mean = mean_difference(before_click, clicked, local_area)
        assert strong > 200, (width, 'Onde peu visible', strong)
        assert strong_mean > idle_mean * 1.6, (width, 'Onde trop faible par rapport au repos', idle_mean, strong_mean)
        assert difference(before_click, clicked, top_area) == 0, 'Le clic ne doit pas déformer les montagnes'
        clicked.save(OUT / f'onde-clic-{width}.png')
        page.get_by_role('button', name='Mettre les animations du paysage en pause').click()
        page.wait_for_timeout(100)
        paused = capture(page)
        paused_count = page.evaluate('window.__waterDraws')
        page.wait_for_timeout(900)
        assert page.evaluate('window.__waterDraws') == paused_count
        assert difference(paused, capture(page), (0, 0, w, h)) == 0
        assert page.locator('.water-toggle').get_attribute('aria-pressed') == 'true'
        # Le bouton d'eau est utilisable au clavier et relance une image en pause.
        page.get_by_role('button', name='Créer une grande onde dans l’eau').focus()
        page.keyboard.press('Enter')
        assert page.locator('.water-toggle').get_attribute('aria-pressed') == 'false'
        page.wait_for_timeout(5500)
        # Après amortissement, retour aux bandes légères du mouvement de repos.
        count = page.evaluate('window.__waveFrames')
        page.wait_for_timeout(250)
        calls_after_fade = page.evaluate('window.__waveFrames') - count
        assert calls_after_fade == 0, (width, 'Onde forte non amortie', calls_after_fade)
        page.evaluate('window.scrollTo(0, 1200)')
        page.wait_for_timeout(150)
        snapshot = page.evaluate('window.__waterDraws')
        page.wait_for_timeout(400)
        assert page.evaluate('window.__waterDraws') == snapshot
        page.evaluate('window.scrollTo(0, 0)')
        page.emulate_media(reduced_motion='reduce')
        assert not page.locator('.water-toggle').is_visible()
        assert not page.locator('.water-splash').is_visible()
        assert not page.locator('canvas').is_visible()
        assert not errors, errors
        report.append({'width': width, 'interaction': 'toucher' if width == 390 else 'clic', 'sky_and_mountains_changed_pixels': top, 'foliage_changed_pixels': foliage_changes, 'idle_mean_difference': idle_mean, 'click_mean_difference': strong_mean, 'strong_wave_pixels': strong, 'pause_all_effects': True, 'keyboard': True, 'fade_out': True, 'offscreen_stops': True, 'reduced_motion': True})
        page.close()
    page = browser.new_page(viewport={'width': 390, 'height': 900}, reduced_motion='reduce')
    page.goto(BASE)
    assert not page.locator('.water-toggle').is_visible()
    assert not page.locator('.home-water-canvas').get_attribute('class').endswith('is-ready')
    page.close()
    page = browser.new_page(viewport={'width': 390, 'height': 900})
    page.add_init_script("const original = HTMLCanvasElement.prototype.getContext; HTMLCanvasElement.prototype.getContext = function(type, ...args) { return type.includes('webgl') ? null : original.call(this, type, ...args); };")
    page.goto(BASE)
    page.wait_for_selector('.home-water-canvas.is-ready')
    assert page.locator('.water-splash').is_visible(), 'Effet requis même sans WebGL'
    page.get_by_role('button', name='Créer une grande onde dans l’eau').focus()
    page.keyboard.press('Space')
    page.close()
    page = browser.new_page(viewport={'width': 390, 'height': 900})
    page.add_init_script("HTMLCanvasElement.prototype.getContext = () => null;")
    page.goto(BASE)
    assert not page.locator('.water-toggle').is_visible()
    assert page.locator('.home-landscape').evaluate('(i) => i.complete && i.naturalWidth > 0')
    page.close()
    page = browser.new_page(viewport={'width': 390, 'height': 900}, java_script_enabled=False)
    page.goto(BASE)
    assert page.locator('h1').is_visible()
    assert not page.locator('.water-toggle').is_visible()
    page.close()
    browser.close()
result = {'animation': report, 'initial_reduced_motion': True, 'works_without_webgl': True, 'without_canvas': True, 'without_javascript': True}
(OUT/'water-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
