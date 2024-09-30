import data
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import methods


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = methods.UrbanRoutesPage(cls.driver)

    def teardown_method(self, method):
        self.driver.delete_all_cookies()  # Esto limpiará cookies y sesión
        self.driver.refresh()  # Refrescará la página para empezar desde cero

    #1
    def test_routes_page(self):
        self.routes_page.set_from(data.address_from)
        self.routes_page.set_to(data.address_to)
        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to

#2
    def test_select_comfort_tariff(self):
        self.routes_page.set_from(data.address_from)
        self.routes_page.set_to(data.address_to)
        self.routes_page.click_pedir_un_taxi_button()
        self.routes_page.click_comfort_button()
        comfort_tariff = self.driver.find_elements(*self.routes_page.comfort_button)
        assert "tcard" in self.driver.find_element(*methods.UrbanRoutesPage.
                                                   comfort_button).get_attribute("class")
        assert comfort_tariff[4].is_enabled()

#3
    def test_llenar_numero_telefono(self):
        self.routes_page.set_from(data.address_from)
        self.routes_page.set_to(data.address_to)
        self.routes_page.click_pedir_un_taxi_button()
        self.routes_page.click_comfort_button()
        self.routes_page.click_telefono_field()
        self.routes_page.set_phone_number()
        self.routes_page.click_next_button()
        code = methods.retrieve_phone_code(self.driver)
        self.routes_page.click_confirmar_button(code)
        phone_input_value = self.driver.find_element(*self.routes_page.phone_input).get_attribute("value")
        assert phone_input_value == data.phone_number

#4
    def test_add_credit_card(self):
        self.routes_page.set_from(data.address_from)
        self.routes_page.set_to(data.address_to)
        self.routes_page.click_pedir_un_taxi_button()
        self.routes_page.click_comfort_button()
        self.routes_page.click_telefono_field()
        self.routes_page.set_phone_number()
        self.routes_page.click_next_button()
        code = methods.retrieve_phone_code(self.driver)
        self.routes_page.set_codigo_field(code)
        self.routes_page.click_confirmar_button(code)
        self.routes_page.click_pago_button()
        self.routes_page.click_add_card()
        WebDriverWait(self.driver, 4).until(
            expected_conditions.element_to_be_clickable(self.routes_page.numero_tarjeta_field))
        self.routes_page.set_numero_tarjeta_field()
        WebDriverWait(self.driver, 4).until(
            expected_conditions.visibility_of_element_located(self.routes_page.codigo_tarjeta_field))
        self.routes_page.click_codigo_tarjeta_field()
        self.routes_page.set_codigo_tarjeta_field()
        self.routes_page.press_tab_key()
        WebDriverWait(self.driver, 4).until(
            expected_conditions.element_to_be_clickable(self.routes_page.agregar_field)
        )
        self.routes_page.click_agregar_field()
        card_input = self.driver.find_elements(*self.routes_page.card_added)[1]
        assert card_input.is_enabled()
        self.routes_page.click_card_close_button()

# 5
    def test_write_message(self):
        self.routes_page.set_from(data.address_from)
        self.routes_page.set_to(data.address_to)
        self.routes_page.click_pedir_un_taxi_button()
        self.routes_page.set_mensaje_buttton()
        assert self.driver.find_element(*self.routes_page.mensaje_conductor_button).get_property('value') == data.message_for_driver

# 6
    def test_request_blanket_and_scarves(self):
       self.routes_page.set_from(data.address_from)
       self.routes_page.set_to(data.address_to)
       self.routes_page.click_pedir_un_taxi_button()
       self.routes_page.click_comfort_button()
       comfort_tariff = self.driver.find_elements(*self.routes_page.comfort_button)
       assert "tcard" in self.driver.find_element(*methods.UrbanRoutesPage.
                                                  comfort_button).get_attribute("class")
       assert comfort_tariff[4].is_enabled()
       self.routes_page.click_abrir_seccion()
       self.routes_page.click_agregar_manta_slide()
       checkbox = self.driver.find_element(*methods.UrbanRoutesPage.switch_checkbox)
       assert checkbox.is_selected() == True


#7
    def test_request_two_ice_creams(self):
        self.routes_page.set_from(data.address_from)
        self.routes_page.set_to(data.address_to)
        self.routes_page.click_pedir_un_taxi_button()
        self.routes_page.click_comfort_button()
        comfort_tariff = self.driver.find_elements(*self.routes_page.comfort_button)
        assert "tcard" in self.driver.find_element(*methods.UrbanRoutesPage.
                                                   comfort_button).get_attribute("class")
        assert comfort_tariff[4].is_enabled()
        self.routes_page.click_abrir_seccion()
        element = methods.driver.find_element(By.XPATH, '//*[contains(text(), "Helado")]')
        methods.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.routes_page.click_agregar_helado_button()
        self.routes_page.click_agregar_helado_button()
        icecream_counter = self.driver.find_element(*methods.UrbanRoutesPage.icecream_counter)
        icecream_count = int(icecream_counter.text)
        assert icecream_count == 2

#8
    def test_aparece_pedir_taxi(self):
        self.routes_page.set_from(data.address_from)
        self.routes_page.set_to(data.address_to)
        self.routes_page.click_pedir_un_taxi_button()
        self.routes_page.click_comfort_button()
        self.routes_page.click_telefono_field()
        self.routes_page.set_phone_number()
        self.routes_page.click_next_button()
        code = methods.retrieve_phone_code(self.driver)
        self.routes_page.set_codigo_field(code)
        self.routes_page.click_confirmar_button(code)
        self.routes_page.click_pago_button()
        self.routes_page.click_add_card()
        WebDriverWait(self.driver, 4).until(
            expected_conditions.element_to_be_clickable(self.routes_page.numero_tarjeta_field))
        self.routes_page.set_numero_tarjeta_field()
        WebDriverWait(self.driver, 4).until(
            expected_conditions.visibility_of_element_located(self.routes_page.codigo_tarjeta_field))
        self.routes_page.click_codigo_tarjeta_field()
        self.routes_page.set_codigo_tarjeta_field()
        self.routes_page.press_tab_key()
        WebDriverWait(self.driver, 4).until(
            expected_conditions.element_to_be_clickable(self.routes_page.agregar_field)
        )
        self.routes_page.click_agregar_field()
        card_input = self.driver.find_elements(*self.routes_page.card_added)[1]
        self.routes_page.click_card_close_button()
        self.routes_page.set_mensaje_buttton()
        self.routes_page.click_abrir_seccion()
        self.routes_page.click_agregar_manta_slide()
        self.routes_page.click_order_a_taxi()
        WebDriverWait(self.driver, 40).until(
            expected_conditions.visibility_of_element_located(self.routes_page.modal_opcional)
        )
        assert self.driver.find_element(*self.routes_page.modal_opcional).is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()