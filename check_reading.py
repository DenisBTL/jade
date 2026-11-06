"""Contrôles des repères de lecture, de la navigation et de son onde de départ."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8792/'
OUT = Path(__file__).parent / '.sites-runtime' / 'qa'
OUT.mkdir(parents=True, exist_ok=True)
report = []


def landed(page, target):
    page.wait_for_function('(id) => location.hash === "#" + id && document.activeElement.id === id', arg=target)
    assert page.evaluate('(id) => Math.abs(scrollY - Math.max(0, Math.min(document.documentElement.scrollHeight - innerHeight, document.getElementById(id).offsetTop - 24))) < 3', target), target


with sync_playwright() as p:
    browser = p.chromium.launch()
    for width in [320, 390, 768, 1440, 1920]:
        page = browser.new_page(viewport={'width': width, 'height': 900}, has_touch=width < 700)
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.add_init_script('''window.__waveFrames = 0;
        const draw = CanvasRenderingContext2D.prototype.drawImage;
        CanvasRenderingContext2D.prototype.drawImage = function(...a) {
          const main = document.querySelector('.home-water-canvas');
          if (a[0] instanceof HTMLCanvasElement && main && a[0].width === main.width) window.__waveFrames++;
          return draw.apply(this, a);
        };''')
        page.goto(BASE)
        page.wait_for_selector('.home-water-canvas.is-ready')
        page.wait_for_timeout(100)
        assert page.locator('.water-toggle,.water-splash').count() == 0
        assert page.locator('.scene-next').count() == 5
        assert page.locator('.scene-nav').is_visible() == (width >= 1340)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert page.locator('#readbar-fill').evaluate('(e) => getComputedStyle(e).transform') == 'matrix(0, 0, 0, 1, 0, 0)'
        hero = page.locator('.home-hero').bounding_box()
        ring = page.locator('.scene-next-water .scene-next-ring').bounding_box()
        assert ring['y'] + ring['height'] / 2 > hero['height'] * .85
        first = page.locator('.scene-next-water')
        if width < 700:
            first.tap()
        else:
            first.focus()
            page.keyboard.press('Enter')
        page.wait_for_timeout(200)
        assert page.evaluate('scrollY') == 0, 'Laisser le temps de voir l’onde'
        assert page.evaluate('window.__waveFrames') > 0, 'Le chevron doit déclencher l’onde'
        landed(page, 'accompagnements')
        for target in ['approche', 'questions', 'informations', 'accueil']:
            page.locator(f'.scene-next[href="#{target}"]').click()
            landed(page, target)
            if target == 'informations':
                assert page.locator('.scene-nav a[aria-current]').get_attribute('href') == '#informations'
        # Interrompre avant le départ annule aussi le déplacement différé.
        first.click()
        page.wait_for_timeout(100)
        page.mouse.wheel(0, 120)
        page.wait_for_timeout(1300)
        assert page.evaluate('0 < scrollY < 200')
        assert page.evaluate('location.hash') == '#accueil'
        # Interrompre pendant une descente ne vole pas le focus ensuite.
        page.evaluate('scrollTo(0,0)')
        first.click()
        page.wait_for_timeout(600)
        page.mouse.wheel(0, 10)
        page.wait_for_timeout(120)
        position = page.evaluate('scrollY')
        page.wait_for_timeout(1200)
        assert abs(page.evaluate('scrollY') - position) < 3
        assert page.evaluate('location.hash') == '#accueil'
        if width >= 1340:
            for target in ['questions', 'accueil']:
                page.locator(f'.scene-nav a[href="#{target}"]').click()
                landed(page, target)
                assert page.locator('.scene-nav a[aria-current]').get_attribute('href') == '#' + target
        page.evaluate('scrollTo(0,document.documentElement.scrollHeight)')
        page.wait_for_timeout(100)
        assert page.locator('#readbar-fill').evaluate('(e) => getComputedStyle(e).transform') == 'matrix(1, 0, 0, 1, 0, 0)'
        assert page.locator('.scene-nav a[aria-current]').get_attribute('href') == '#informations'
        assert not errors, errors
        report.append({'width': width, 'water_cue': True, 'all_scenes_focus': True, 'scroll_cancel': True, 'progress': True, 'javascript_errors': errors})
        page.close()
    for mode in ['reduced', 'no_canvas', 'no_javascript']:
        page = browser.new_page(viewport={'width': 390, 'height': 900}, reduced_motion='reduce' if mode == 'reduced' else 'no-preference', java_script_enabled=mode != 'no_javascript')
        if mode == 'no_canvas':
            page.add_init_script('HTMLCanvasElement.prototype.getContext = () => null;')
        page.goto(BASE)
        if mode == 'no_javascript':
            assert not page.locator('.readbar').is_visible()
        if mode == 'reduced':
            assert page.locator('.scene-next-water svg').evaluate('(e) => getComputedStyle(e).animationName') == 'none'
        page.locator('.scene-next-water').click()
        if mode == 'no_javascript':
            page.wait_for_function('location.hash === "#accompagnements"')
        else:
            # Sans animation, pas de délai supplémentaire avant le déplacement.
            page.wait_for_timeout(120)
            assert page.evaluate('scrollY') > 0
            landed(page, 'accompagnements')
        page.close()
    # Échap ferme le menu sans suspendre le paysage.
    page = browser.new_page(viewport={'width': 390, 'height': 900})
    page.goto(BASE)
    page.wait_for_selector('.home-water-canvas.is-ready')
    menu = page.get_by_role('button', name='Menu', exact=True)
    menu.click()
    page.keyboard.press('Escape')
    assert menu.get_attribute('aria-expanded') == 'false'
    assert page.locator('canvas').get_attribute('data-motion-state') == 'running'
    page.keyboard.press('Escape')
    assert page.locator('canvas').get_attribute('data-motion-state') == 'paused'
    page.locator('.scene-next-water').click()
    assert page.locator('canvas').get_attribute('data-motion-state') == 'running'
    landed(page, 'accompagnements')
    browser.close()
result = {'navigation': report, 'reduced_motion': True, 'without_canvas': True, 'without_javascript': True, 'menu_escape': True, 'wave_resumes_landscape': True}
(OUT / 'reading-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
