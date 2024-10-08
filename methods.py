import data
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import json
import time
from selenium.common import WebDriverException

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    pedir_un_taxi_button = (By.XPATH, '//*[contains(text(), "Pedir un taxi")]')
    comfort_tariff_button = (By.XPATH, "*//div[contains(@class, ' tcard active') and .//dic[text()='Comfort']*)")
    comfort_button = (By.XPATH, "//div[@class='tcard-title' and normalize-space()='Comfort']")
    telefono_field = (By.CLASS_NAME, 'np-button')
    phone_input = (By.ID, 'phone')
    next_button = (By.XPATH, '//*[contains(text(), "Siguiente")]')
    codigo_field = (By.ID, 'code')
    confirmar_button = (By.XPATH, '//*[contains(text(), "Confirmar")]')
    pago_button = (By.CLASS_NAME, 'pp-text')
    card_added = (By.CLASS_NAME, 'pp-row')
    add_card = (By.XPATH, '//*[contains(text(), "Agregar tarjeta")]')
    numero_tarjeta_field =  (By.NAME,'number')
    codigo_tarjeta_field = (By.NAME, 'code')
    agregar_field = (By.XPATH, "//button[@type='submit' and text()='Agregar']")
    card_close_button = (By.CSS_SELECTOR, '.payment-picker.open .modal .section.active .close-button')
    mensaje_conductor_button = (By.ID, 'comment')
    agregar_manta_slide = (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[contains(@class, 'r-sw')]//span[@class='slider round']")
    open_helado = (By.XPATH, "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div//div[@class='counter-plus']")
    counter_plus_disabled = (By.XPATH, "(//div[@class='counter-plus'])[1]")
    counter_value = (By.CLASS_NAME, "counter-value")
    order_a_taxi = (By.CLASS_NAME, "smart-button-wrapper")
    modal_opcional = (By.XPATH, '//*[contains(text(), "El conductor llegará en")]')
    switch_checkbox = (By.CLASS_NAME, "switch-input")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver,45)

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(data.address_from)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(data.address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_pedir_un_taxi_button(self):
        self.driver.find_element(*self.pedir_un_taxi_button).click()

    def click_comfort_button(self):
        comfort_tariff_button = WebDriverWait(self.driver, 4).until(expected_conditions.element_to_be_clickable(self.comfort_button))
        comfort_tariff_button.click()

    def is_comfort_tariff_selected(self):
        try:
            self.driver.find_element(*self.comfort_button)
            return True
        except:
            return False

    def click_telefono_field(self):
        self.driver.find_element(*self.telefono_field).click()

    def set_phone_number(self):
        self.driver.find_element(*self.phone_input).send_keys(data.phone_number)

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def set_codigo_field(self, code):
        self.driver.find_element(*self.codigo_field).send_keys(code)

    def click_confirmar_button(self, code):
        self.driver.find_element(*self.confirmar_button).click()

    def click_pago_button(self):
        self.driver.find_element(*self.pago_button).click()

    def click_add_card(self):
        self.driver.find_element(*self.add_card).click()

    def click_numero_tarjeta_field(self):
        self.driver.find_element(*self.numero_tarjeta_field).click()

    def set_numero_tarjeta_field(self):
        self.driver.find_element(*self.numero_tarjeta_field).send_keys(data.card_number)

    def click_codigo_tarjeta_field(self):
        self.driver.find_element(*self.codigo_tarjeta_field).click()

    def set_codigo_tarjeta_field(self):
        codigo_tarjeta_field = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.codigo_tarjeta_field)
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", codigo_tarjeta_field)
        codigo_tarjeta_field.send_keys(data.card_code)

    def press_tab_key(self):
        WebDriverWait(self.driver, 4).until(
            expected_conditions.visibility_of_element_located(self.codigo_tarjeta_field)
        )
        self.driver.find_element(*self.codigo_tarjeta_field).send_keys(Keys.TAB)

    def click_agregar_field(self):
        self.driver.find_element(*self.agregar_field).click()

    def click_card_close_button(self):
        self.driver.find_element(*self.card_close_button).click()

    def set_mensaje_buttton(self):
        self.driver.find_element(*self.mensaje_conductor_button).send_keys(data.message_for_driver)

    def click_agregar_manta_slide(self):
        self.driver.find_element(*self.agregar_manta_slide).click()

    def click_open_helado(self):
        self.driver.find_element(*self.open_helado).click()

    def double_click_counter_plus_disabled(self, clicks=2):  # Agrega un parámetro por defecto
        WebDriverWait(self.driver, 40
                      ).until(
        expected_conditions.element_to_be_clickable(self.counter_plus_disabled)
        )
        for _ in range(clicks):
            self.driver.find_element(*self.counter_plus_disabled).click()

    def get_agregar_helado_buttton(self):
        value_element = self.wait.until(expected_conditions.visibility_of_element_located(self.counter_value))
        value = value_element.text.strip()
        return int(value) if value else 0

    def wait_opcional_modal(self):
        self.driver.find_element(*self.modal_opcional)

    def click_order_a_taxi(self):
        self.driver.find_element(*self.order_a_taxi).click()

