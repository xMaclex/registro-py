import os
import django
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registro.settings')
django.setup()

from gestion.models import ResultadoProceso

def registrar_resultado(paso, exito, mensaje):
    ResultadoProceso.objects.create(paso=paso, exito=exito, mensaje=mensaje)

driver = webdriver.Chrome()

try:
    driver.get("http://127.0.0.1:8000/")
    driver.find_element(By.NAME, "username").send_keys("macle")
    driver.find_element(By.NAME, "password").send_keys("elmejorde1")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(5)

    print("Login exitoso")
    registrar_resultado("Inicio de sesión", True, "Login exitoso")

    driver.find_element(By.LINK_TEXT, "Agregar Persona").click()
    driver.find_element(By.NAME, "nombre").send_keys("Cristiano Ronaldo")
    driver.find_element(By.NAME, "edad").send_keys("40")
    driver.find_element(By.NAME, "correo").send_keys("elbicho@gmail.com")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(3)

    print(" Persona creada exitosamente")
    registrar_resultado("Crear persona", True, "Persona creada exitosamente")

    personas = driver.find_elements(By.TAG_NAME, "tr")
    encontrada = False
    for p in personas:
        if "Michael Jordan" in p.text:
            encontrada = True
            print(" Persona encontrada: ", p.text)
            registrar_resultado("Verificar persona", True, f"Persona encontrada: {p.text}")
            break
    if not encontrada:
        print(" Persona no encontrada en la lista")
        registrar_resultado("Verificar persona", False, "Persona no encontrada en la lista")

    driver.find_element(By.LINK_TEXT, "Editar").click()
    edad_field = driver.find_element(By.NAME, "edad")
    edad_field.clear()
    edad_field.send_keys("30")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(3)

    print(" Persona editada exitosamente")
    registrar_resultado("Editar persona", True, "Persona editada exitosamente")

    driver.find_element(By.LINK_TEXT, "Eliminar").click()
    driver.switch_to.alert.accept()
    time.sleep(4)

    print(" Persona eliminada exitosamente")
    registrar_resultado("Eliminar persona", True, "Persona eliminada exitosamente")

    print("Pruebas automatizadas completadas.")

except Exception as e:
    print(f"Error durante la ejecución: {e}")
    registrar_resultado("Error general", False, f"Error durante la ejecución: {e}")

finally:
    driver.quit()
