import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from difflib import SequenceMatcher
from selenium.webdriver import ActionChains
from selenium.webdriver.support.relative_locator import locate_with

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

class TestPuntoA:
    def test_punto_i(self, driver):
        driver.get('https://translate.google.com.ar/?hl=es')
        wait = WebDriverWait(driver,10)

        btn_espanol = driver.find_element(By.ID,'i10')
        btn_espanol.click()
        wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='i13' and @aria-selected='true']")))
        txt_ingles = driver.find_element(By.CLASS_NAME,'er8xn')
        txt_ingles.send_keys('Hola Mundo')

        wait.until(EC.presence_of_element_located((By.CLASS_NAME,'ryNqvb')))
        txt_traducido = driver.find_element(By.CLASS_NAME,'ryNqvb')      
        assert 'Hello World' in txt_traducido.text

    def test_punto_ii(self, driver):
        driver.get('https://translate.google.com.ar/?hl=es')
        wait = WebDriverWait(driver,5)
        
        #Se busca el botón de español y se lo hace click
        btn_espanol = driver.find_element(By.ID,'i10')
        btn_espanol.click()
        
        #Se espera que aparezca el teclado y se le hace click. Luego se espera a que aparezca
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.ita-kd-inputtools-div')))
        btn_teclado = driver.find_element(By.CSS_SELECTOR,'.ita-kd-inputtools-div')
        btn_teclado.click()
        wait.until(EC.visibility_of_element_located((By.ID,'kbd')))
        text = 'Hola Mundo'
        
        #Se va leyendo caracter por caracter y buscando los mismos en el teclado
        for i in range(len(text)):
            caracter = text[i].lower()
            if caracter.isspace():
                btn_teclado = driver.find_element(By.ID,'K32')
            else:
                btn_teclado = driver.find_element(By.XPATH,"//span[text()='"+caracter+"']")
            btn_teclado.click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,'ryNqvb')))
        txt_traducido = driver.find_element(By.CLASS_NAME,'ryNqvb')        
        assert 'Hello World' in txt_traducido.text

    def test_punto_iii(self, driver):
        driver.get('https://translate.google.com.ar/?hl=es')
        
        #Se busca el botón de español y se lo hace click
        btn_espanol = driver.find_element(By.ID,'i10')
        btn_espanol.click()
        
        #Se carga el texto que va a ser traducido
        text = 'Hola Mundo'
        long_text = str(len(text))
        txt_ingles = driver.find_element(By.CLASS_NAME,'er8xn')
        txt_ingles.send_keys(text)
        
        #Se busca donde se carga el contador
        contador = driver.find_element(By.XPATH,"//span[@jsname='qKMVIf']")
        assert long_text == contador.text
    
    def test_punto_iv(self, driver):
        driver.get('https://translate.google.com.ar/?hl=es')
        wait = WebDriverWait(driver,20)
        
        #Se busca el botón de español y se lo hace click
        btn_espanol = driver.find_element(By.ID,'i10')
        btn_espanol.click()

        #Se carga el texto que va a ser contado
        text = 'a'
        for i in range(2501):
            text += 'a'
        txt_ingles = driver.find_element(By.CLASS_NAME,'er8xn')
        txt_ingles.send_keys(text)
        
        #Se selecciona, copia y pega el texto que haya para poder forzar el error
        txt_ingles.send_keys(Keys.CONTROL + 'a')
        txt_ingles.send_keys(Keys.CONTROL + 'c')
        txt_ingles.click()
        txt_ingles.send_keys(Keys.CONTROL + 'v')
        assert wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'ef1twd')))


##################################################################################################


class TestPuntoB:
    def test_punto_i(self, driver):
        cuenta = ''
        password = ''
        driver.get('https://www.youtube.com/')
        wait = WebDriverWait(driver,10)

        #Entrar a la cuenta
        wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="end"]//a[@aria-label="Acceder"]//div[@class="yt-spec-touch-feedback-shape yt-spec-touch-feedback-shape--touch-response"]')))
        boton = driver.find_element(By.XPATH,'//div[@id="end"]//a[@aria-label="Acceder"]//div[@class="yt-spec-touch-feedback-shape yt-spec-touch-feedback-shape--touch-response"]')
        boton.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'identifierNext')))
        input = driver.find_element(By.ID,'identifierId')
        input.send_keys(cuenta)
        input.send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.ID, 'passwordNext')))
        input = driver.find_element(By.XPATH,'//div[@id="password"]//input[@class="whsOnd zHQkBf"]')
        input.send_keys(password)
        input.send_keys(Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.XPATH,'//input[@id="search"]')))

        #Buscar algo en el buscador
        buscador = driver.find_element(By.XPATH,'//input[@id="search"]')
        buscador.send_keys('duck')
        buscador.send_keys(Keys.ENTER)
        wait.until(EC.title_contains('duck'))

        #Se selecciona el botón de menú de opciones del primer video
        boton = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/div/ytd-menu-renderer/yt-icon-button/button/yt-icon')
        boton.click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'tp-yt-iron-dropdown .style-scope.ytd-popup-container')))
        
        #Se selecciona el botón de salvar para mirar luego
        boton = driver.find_element(By.XPATH,'//yt-formatted-string[text()="Save to Watch later"]')
        boton.click()

        #Se espera que aparezca la notificación de que fue guardado para mirar luego
        assert wait.until(EC.visibility_of_element_located((By.XPATH, '//yt-formatted-string[text()="Saved to Watch later"]')))

    def test_punto_ii(self, driver):
        config_xpath = '//yt-icon-button[@id="button"]'
        desing_xpath = '//ytd-toggle-theme-compact-link-renderer[@class="style-scope yt-multi-page-menu-section-renderer"]'
        txt_to_search = 'Tema oscuro'
        driver.get('https://www.youtube.com/')
        wait = WebDriverWait(driver,10)

        #Se localiza el botón de configuración y se lo presiona
        wait.until(EC.visibility_of_element_located((By.XPATH, config_xpath)))
        boton = driver.find_element(By.XPATH, config_xpath)
        boton.click()

        #Se localiza el botón donde se encuentra las opciones de diseño y se lo presiona
        wait.until(EC.presence_of_element_located((By.XPATH, desing_xpath)))
        boton = driver.find_element(By.XPATH, desing_xpath)
        boton.click()
        wait.until(EC.presence_of_element_located((By.ID,'submenu')))
        
        #Se elige como el tema oscuro como diseño
        boton = driver.find_element(By.XPATH,'//yt-formatted-string[text()="' + txt_to_search + '"]')
        boton.click()
        
        #Se localiza el botón de configuración y se lo presiona
        wait.until(EC.visibility_of_element_located((By.XPATH, config_xpath)))
        boton = driver.find_element(By.XPATH, config_xpath)
        boton.click()
        
        #se localiza el botón donde se encuentra las opciones de diseño y se lo presiona
        wait.until(EC.visibility_of_element_located((By.XPATH, desing_xpath)))
        boton = driver.find_element(By.XPATH, desing_xpath)
        boton.click()
        wait.until(EC.presence_of_element_located((By.ID,'submenu')))
        
        #Se encuentra donde se encuentra el check ubicado y luego el div que se encuentre a la derecha del mismo
        img_check = driver.find_element(By.XPATH,'//div[@id="submenu"]//div[@id="content-icon" and not(@hidden)]')
        selected = driver.find_element(locate_with(By.ID,'primary-text-container').to_right_of(img_check))
        
        assert txt_to_search in selected.text


##################################################################################################


class TestPuntoC:
    def test_punto_i(self, driver):
        driver.get('https://ugd.edu.ar/')
        wait = WebDriverWait(driver,10)
        text = 'ingenieria'
        prueba = False
        
        #Se espera a que se cargue el div donde está el carrusel
        wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class=' col-lg-12 col-md-12 col-sm-12 col-xs-12']")))
        
        #Se busca la palabra en el buscador
        buscador = driver.find_element(By.ID,'mod-search-searchword')
        buscador.send_keys(text)
        buscador.send_keys(Keys.ENTER)
        
        #Se espera que se cargue el formulario de búsqueda y se busca el contador
        wait.until(EC.presence_of_element_located((By.ID,'searchForm')))
        
        #Si lo buscado no respeta los valores límites de la búsqueda no se continúa con la prueba 
        if len(text) < 3 or len(text) > 200:
            prueba = True
        else:
            contador = driver.find_element(By.XPATH,"//span[@class='badge badge-info']")
            #Si es 0 significa que no encontró resultados
            if contador.text == '0':
                prueba = True
            else:
                #Se encuentran todos los resultados y se los deja en minúscula
                resultados = driver.find_elements(By.CLASS_NAME,'highlight')
                text = text.lower()
                text2 = resultados[0].text.lower()
                #La similitud debe ser superior al 66% por si se busca con el mínimo (3 letras), lo que
                #significa que sólo una letra no puede ser igual a lo encontrado
                if SequenceMatcher(a=text,b=text2).ratio() > 0.66:
                    prueba = True
        assert prueba
    
    def test_punto_ii(self, driver):
        driver.get('https://ugd.edu.ar/')
        wait = WebDriverWait(driver,10)
        
        #Se hace click en el botón para cambiar el idioma y se selecciona el inglés
        driver.find_element(By.XPATH,'//a[@class="btn dropdown-toggle"]').click()
        driver.find_element(By.XPATH,'//a[@href="/en/"]').click()
        
        #Se espera que se cargue el nav donde se encuentran los elementos traducidos
        wait.until(EC.visibility_of_all_elements_located((By.ID,'t3-mainnav')))
        
        #Se busca el li donde se encuentra contenido cada elemento traducido a analizar
        university = driver.find_element(By.XPATH,"//li[@data-id='1065']")
        studies = driver.find_element(By.XPATH,"//li[@data-id='1270']")
        inc_stu = driver.find_element(By.XPATH,"//li[@data-id='1297']")
        contact = driver.find_element(By.XPATH,"//li[@data-id='1306']")
        assert university.text == 'UNIVERSITY' and studies.text == 'STUDIES' and inc_stu.text == 'INCOMING STUDENTS' and contact.text == 'CONTACT'


##################################################################################################


@pytest.fixture
def ingreso(driver):
        driver.get('https://campusvirtual.ugd.edu.ar/')
        driver.find_element(By.ID,'username').send_keys('')     #usuario
        driver.find_element(By.ID,'password').send_keys('')     #contraseña
        driver.find_element(By.XPATH,'//input[@type="submit"]').click()
        return driver

class TestPuntoD:
    #Para los puntos i a iii cambiar las credenciales en el fixture ingreso
    def test_punto_i(self, ingreso):      
        #Se ingresa al campus
        navegador = ingreso
        wait = WebDriverWait(navegador,10)
        
        #Se espera a que se cargue donde se encuentra "Todos los cursos" para darle click
        wait.until(EC.visibility_of_all_elements_located((By.XPATH,'//ul[@class="nav"]')))
        navegador.find_element(By.XPATH,'//a[@title="Todos los Cursos"]').click()
        
        #Se espera a que aparezca donde se encuentra el buscador para poder enviarle el string a buscar
        wait.until(EC.visibility_of_element_located((By.ID,'navsearchbox')))
        buscador = navegador.find_element(By.ID,'navsearchbox')
        buscador.send_keys('gestion de calidad')
        buscador.send_keys(Keys.ENTER)
        
        #Se espera a que aparezca el resultado de la búsqueda para luego hacer click en el aula
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'main')))
        navegador.find_element(By.XPATH,'//a[@href="https://campusvirtual.ugd.edu.ar/moodle/course/view.php?id=64"]').click()
        assert 'GESTION DE LA CALIDAD Y AUDITORIA' in navegador.title
    
    def test_punto_ii(self, ingreso):
        #Se ingresa al campus
        navegador = ingreso
        wait = WebDriverWait(navegador,10)
        
        #Se espera a que aparezca el div que contiene al tag donde se encuentra el mensaje
        wait.until(EC.visibility_of_element_located((By.ID,'yui_3_9_1_3_1660762677544_1057')))
        divMensaje = navegador.find_element(By.ID,'yui_3_9_1_3_1660762677544_1057')
        assert 'no deberá registrar deuda luego del día 10 de cada mes.' in divMensaje.text
    
    def test_punto_iii(self, ingreso):
        #Se ingresa al campus
        navegador = ingreso
        wait = WebDriverWait(navegador,10)
        wait.until(EC.visibility_of_all_elements_located((By.ID,'page-footer')))
        original_window = navegador.current_window_handle
        
        #Se scrollea hasta el footer y se hace el click en los horarios
        footer = navegador.find_element(By.TAG_NAME, "footer")
        ActionChains(navegador)\
            .scroll_to_element(footer)\
            .perform()
        navegador.find_element(By.XPATH,'//a[@href="https://www.ugd.edu.ar/la-universidad/alumnos/horarios-de-catedra"]').click()
        
        #Se espera a que haya dos pestañas y se cambia el driver a la nueva
        wait.until(EC.number_of_windows_to_be(2))
        for window_handle in navegador.window_handles:
            if window_handle != original_window:
                navegador.switch_to.window(window_handle)
                break
        
        #Se espera a que la página esté cargada para hacer el assert
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,'html')))
        assert 'Horarios de cátedra' in navegador.title
    
    def test_punto_iv(self, driver):
        driver.get('https://campusvirtual.ugd.edu.ar/')
        wait = WebDriverWait(driver,10)
        
        #Se intenta ingresar al campus
        driver.find_element(By.ID,'username').send_keys('00000')
        driver.find_element(By.ID,'password').send_keys('a')
        driver.find_element(By.XPATH,'//input[@type="submit"]').click()
        
        #Se espera a que aparezca el span donde se encuentra el mensaje de error
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,'error')))
        spanError = driver.find_element(By.CLASS_NAME,'error')
        msgError = 'Datos erróneos, por favor intentelo de nuevo. '
        msgError += 'Recuerde que el usuario se bloquea al adeudar la cuota el día 17 del mes vigente o más cuotas.'
        
        #Pasa la prueba si el span se encuentra visible y si el mensaje está bien escrito
        assert spanError.is_displayed() and msgError == spanError.text