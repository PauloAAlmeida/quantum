"""
    pip install selenium Pillow
    PDF será salvo como "pagina_capturada.pdf"
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time
import os
import math
import shutil

#config

URL = "https://cimatecead.senaicimatec.com.br/Ucs/inovapos/tecnicas-construcao-algoritmos-quanticos/ua1/ova-01/"

OUTPUT_PDF = "pagina_capturada.pdf"
TEMP_DIR = "temp_screenshots"

HEADLESS = False
WAIT_AFTER_LOAD = 5

# Aumente se ainda pular trechos
WAIT_BETWEEN_SCROLLS = 1.0

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080


SCROLL_ADVANCE_RATIO = 0.5




def setup_driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    return driver


def hide_fixed_elements(driver):
    
    script = """
    (function() {
        var all = document.querySelectorAll('*');
        var hidden = [];
        for (var i = 0; i < all.length; i++) {
            var el = all[i];
            var style = window.getComputedStyle(el);
            var position = style.position;
            
            // Esconde elementos fixos e sticky
            if (position === 'fixed' || position === 'sticky') {
                // Não esconde o container principal de scroll
                if (el.scrollHeight > el.clientHeight + 500) {
                    continue;
                }
                el.setAttribute('data-original-display', el.style.display);
                el.style.setProperty('display', 'none', 'important');
                hidden.push(el.tagName + '.' + (el.className || '').substring(0, 30));
            }
        }
        return hidden;
    })();
    """
    hidden = driver.execute_script(script)
    if hidden:
        print(f"\n  Elementos fixos escondidos ({len(hidden)}):")
        for h in hidden:
            print(f"    - {h}")
    else:
        print("\n  Nenhum elemento fixo encontrado.")
    return hidden


def remove_scrollbars(driver):
    
    driver.execute_script("""
        var style = document.createElement('style');
        style.textContent = `
            ::-webkit-scrollbar { display: none !important; }
            * { scrollbar-width: none !important; }
        `;
        document.head.appendChild(style);
    """)


def find_scrollable_container(driver):
    
    script = """
    function findScrollableElement() {
        var all = document.querySelectorAll('*');
        var candidates = [];
        
        for (var i = 0; i < all.length; i++) {
            var el = all[i];
            var style = window.getComputedStyle(el);
            var overflowY = style.overflowY;
            
            if (overflowY === 'scroll' || overflowY === 'auto') {
                if (el.scrollHeight > el.clientHeight + 50) {
                    candidates.push({
                        element: el,
                        scrollHeight: el.scrollHeight,
                        clientHeight: el.clientHeight,
                        diff: el.scrollHeight - el.clientHeight,
                        tag: el.tagName,
                        id: el.id,
                        className: el.className
                    });
                }
            }
        }
        
        candidates.sort(function(a, b) { return b.diff - a.diff; });
        
        if (candidates.length > 0) {
            var best = candidates[0];
            var el = best.element;
            el.setAttribute('data-capture-target', 'true');
            
            return {
                selector: el.id ? '#' + el.id : '[data-capture-target="true"]',
                scrollHeight: best.scrollHeight,
                clientHeight: best.clientHeight,
                tag: best.tag,
                info: best.tag + (el.id ? '#' + el.id : '') + '.' + (best.className || '').substring(0, 50)
            };
        }
        
        var bodyScroll = document.body.scrollHeight;
        var docScroll = document.documentElement.scrollHeight;
        var viewHeight = window.innerHeight;
        
        if (bodyScroll > viewHeight + 50 || docScroll > viewHeight + 50) {
            return {
                selector: null,
                scrollHeight: Math.max(bodyScroll, docScroll),
                clientHeight: viewHeight,
                tag: 'BODY',
                info: 'window scroll'
            };
        }
        
        return null;
    }
    return findScrollableElement();
    """
    return driver.execute_script(script)


def try_expand_container_to_fullscreen(driver, selector):

    if not selector:
        return
    
    script = f"""
    (function() {{
        var el = document.querySelector('{selector}');
        if (!el) return false;
        
        // Expande o container para ocupar a tela toda
        el.style.setProperty('position', 'fixed', 'important');
        el.style.setProperty('top', '0', 'important');
        el.style.setProperty('left', '0', 'important');
        el.style.setProperty('width', '100vw', 'important');
        el.style.setProperty('height', '100vh', 'important');
        el.style.setProperty('z-index', '999999', 'important');
        el.style.setProperty('background', 'white', 'important');
        
        return true;
    }})();
    """
    result = driver.execute_script(script)
    if result:
        print("  Container expandido para tela cheia.")


def get_scroll_pos(driver, selector):
    if selector:
        return driver.execute_script(
            f"var el = document.querySelector('{selector}'); return el ? el.scrollTop : 0;"
        )
    else:
        return driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")


def set_scroll_pos(driver, selector, position):
    if selector:
        driver.execute_script(
            f"var el = document.querySelector('{selector}'); if(el) el.scrollTop = {position};"
        )
    else:
        driver.execute_script(f"window.scrollTo(0, {position});")


def get_scroll_height(driver, selector):
    if selector:
        return driver.execute_script(
            f"var el = document.querySelector('{selector}'); return el ? el.scrollHeight : 0;"
        )
    else:
        return driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);"
        )


def get_client_height(driver, selector):
    if selector:
        return driver.execute_script(
            f"var el = document.querySelector('{selector}'); return el ? el.clientHeight : 0;"
        )
    else:
        return driver.execute_script("return window.innerHeight;")


def get_content_bbox(driver, selector):
 
    if not selector:
        return None
    
    result = driver.execute_script(f"""
        var el = document.querySelector('{selector}');
        if (!el) return null;
        var rect = el.getBoundingClientRect();
        return {{
            x: rect.x,
            y: rect.y,
            width: rect.width,
            height: rect.height
        }};
    """)
    return result


def capture_scrolling(driver, selector):
    
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Vai pro topo
    set_scroll_pos(driver, selector, 0)
    time.sleep(0.5)

    client_height = get_client_height(driver, selector)
    scroll_step = int(client_height * SCROLL_ADVANCE_RATIO)

    # Obtém a bounding box do container para recortar screenshots
    bbox = get_content_bbox(driver, selector)

    print(f"\n  Altura visível: {client_height}px")
    print(f"  Passo de scroll: {scroll_step}px ({SCROLL_ADVANCE_RATIO*100:.0f}% da tela)")
    if bbox:
        print(f"  Área de conteúdo: x={bbox['x']:.0f}, y={bbox['y']:.0f}, "
              f"w={bbox['width']:.0f}, h={bbox['height']:.0f}")

    screenshots = []
    target_scroll = 0
    last_actual_pos = -1
    stuck_count = 0
    max_iterations = 500

    for i in range(max_iterations):
        set_scroll_pos(driver, selector, target_scroll)
        time.sleep(WAIT_BETWEEN_SCROLLS)

        actual_pos = get_scroll_pos(driver, selector)
        total_height = get_scroll_height(driver, selector)

        # Screenshot da tela inteira
        full_screenshot_path = os.path.join(TEMP_DIR, f"full_{i:04d}.png")
        driver.save_screenshot(full_screenshot_path)

        # Recorta apenas a área do conteúdo se temos bbox
        screenshot_path = os.path.join(TEMP_DIR, f"screenshot_{i:04d}.png")
        
        if bbox:
            img = Image.open(full_screenshot_path)
            # Calcula o fator de escala (device pixel ratio)
            actual_width = img.size[0]
            dpr = actual_width / WINDOW_WIDTH
            
            crop_x = int(bbox['x'] * dpr)
            crop_y = int(bbox['y'] * dpr)
            crop_w = int(bbox['width'] * dpr)
            crop_h = int(bbox['height'] * dpr)
            
            # Garante que não ultrapassa os limites da imagem
            crop_x = max(0, crop_x)
            crop_y = max(0, crop_y)
            crop_right = min(img.size[0], crop_x + crop_w)
            crop_bottom = min(img.size[1], crop_y + crop_h)
            
            cropped = img.crop((crop_x, crop_y, crop_right, crop_bottom))
            cropped.save(screenshot_path)
            cropped.close()
            img.close()
        else:
            # Sem bbox, usa screenshot inteira
            os.rename(full_screenshot_path, screenshot_path)
        
        # Remove screenshot full se ainda existir
        if os.path.exists(full_screenshot_path):
            os.remove(full_screenshot_path)

        screenshots.append((screenshot_path, actual_pos))

        progress = (actual_pos + client_height) / total_height * 100 if total_height > 0 else 100
        print(f"  Screenshot {i+1:3d}: scroll={actual_pos:6.0f}px / {total_height}px  ({progress:5.1f}%)")

        if actual_pos + client_height >= total_height - 2:
            print("\n  Fim do conteúdo!")
            break

        if abs(actual_pos - last_actual_pos) < 2:
            stuck_count += 1
            if stuck_count >= 3:
                print("\n  Scroll travou. Fim detectado.")
                break
        else:
            stuck_count = 0

        last_actual_pos = actual_pos
        target_scroll += scroll_step

    return screenshots, client_height, total_height


def stitch_and_save_pdf(screenshots, viewport_height, total_height):
   
    if not screenshots:
        print("Nenhum screenshot capturado!")
        return

    first_img = Image.open(screenshots[0][0])
    img_width, img_height = first_img.size
    first_img.close()

    scale = img_height / viewport_height if viewport_height > 0 else 1
    final_height = int(total_height * scale)

    print(f"\n  Costurando: {img_width} x {final_height}px")

    final_img = Image.new("RGB", (img_width, final_height), (255, 255, 255))

    for idx, (path, scroll_pos) in enumerate(screenshots):
        img = Image.open(path)
        y_pos = int(scroll_pos * scale)

        if idx < len(screenshots) - 1:
            next_scroll = screenshots[idx + 1][1]
            usable_height = int((next_scroll - scroll_pos) * scale)
            usable_height = min(usable_height, img.size[1])
        else:
            usable_height = min(img.size[1], final_height - y_pos)

        if usable_height > 0:
            cropped = img.crop((0, 0, img_width, usable_height))
            final_img.paste(cropped, (0, y_pos))
        img.close()

    # Divide em páginas A4
    a4_ratio = 297 / 210
    page_width = img_width
    page_height = int(page_width * a4_ratio)
    num_pages = math.ceil(final_height / page_height)

    print(f"  Páginas A4: {num_pages}")

    pdf_pages = []
    for p in range(num_pages):
        y_start = p * page_height
        y_end = min(y_start + page_height, final_height)
        page_img = Image.new("RGB", (page_width, page_height), (255, 255, 255))
        crop = final_img.crop((0, y_start, page_width, y_end))
        page_img.paste(crop, (0, 0))
        pdf_pages.append(page_img.convert("RGB"))

    if pdf_pages:
        pdf_pages[0].save(
            OUTPUT_PDF,
            save_all=True,
            append_images=pdf_pages[1:],
            resolution=150,
        )
        print(f"\n  PDF salvo: {OUTPUT_PDF}")
        print(f"  Tamanho: {os.path.getsize(OUTPUT_PDF) / 1024 / 1024:.1f} MB")

    final_img.close()
    for p in pdf_pages:
        p.close()


def cleanup():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)


def main():
    print("=*" * 60)
    print("CAPTURADOR DE PÁGINA WEB PARA PDF - v4")
    print("=*" * 60)

    driver = setup_driver()

    try:
        print(f"\nAbrindo: {URL}")
        driver.get(URL)

        if not HEADLESS:
            print("\n" + "-" * 60)
            print("O navegador está aberto.")
            print("Faça LOGIN se necessário, depois volte aqui.")
            print("-" * 60)
            input("\nPressione ENTER para iniciar a captura...")
        else:
            time.sleep(WAIT_AFTER_LOAD)

        # 1. Detecta container de scroll
        print("\nAnalisando a página...")
        container_info = find_scrollable_container(driver)

        if not container_info:
            print("Nenhum container scrollável encontrado!")
            return

        selector = container_info['selector']
        print(f"  Container: {container_info['info']}")
        print(f"  Conteúdo: {container_info['scrollHeight']}px")
        print(f"  Visível: {container_info['clientHeight']}px")

        # 2. Esconde headers/menus fixos
        print("\nRemovendo elementos fixos (headers, menus, barras)...")
        hide_fixed_elements(driver)
        
        # 3. Remove scrollbars visuais
        remove_scrollbars(driver)
        
        time.sleep(0.5)

        # 4. Captura
        print("\nIniciando captura...")
        screenshots, vh, th = capture_scrolling(driver, selector)

        if len(screenshots) > 0:
            stitch_and_save_pdf(screenshots, vh, th)
        else:
            print("Nenhum screenshot capturado!")

    except KeyboardInterrupt:
        print("\n\nInterrompido.")
    finally:
        driver.quit()
        cleanup()

    print("\nConcluído!")


if __name__ == "__main__":
    main()
