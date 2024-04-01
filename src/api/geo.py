import http.client

from django.contrib.gis.geoip2 import GeoIP2
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from geopy.distance import geodesic as gd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# from config import settings
from events.models import EventLocation
from users.models import UserLocation

# Адрес сайта "Яндекс.Карты"
URL_YANDEX_MAPS = "https://yandex.ru/maps"


def get_geo_event(city, address):
    """Получение геолокации по Яндекс.Картам."""
    # Время ожидания
    delay = 3
    # Подключение драйвера Google
    options = Options()
    # if not settings.DEBUG:
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    # Переход на сайт
    driver.get(URL_YANDEX_MAPS)
    # Поиск формы ввода на сайте
    elem_search_string = WebDriverWait(driver, delay).until(
        ec.presence_of_element_located(
            (By.XPATH, "//input[@class='input__control _bold']")
        )
    )
    # Вписываем данные в форму
    elem_search_string.send_keys(f"{city}, {address}")
    # Запускаем поиск
    elem_search_string.send_keys(Keys.ENTER)
    # Поиск координат на сайте
    try:
        elem_search = WebDriverWait(driver, delay).until(
            ec.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@class='toponym-card-title-view__coords-badge']",
                )
            )
        )
        # Возврат координат адреса
        if elem_search.text:
            return list(map(float, elem_search.text.split(", ")))
    except TimeoutException:
        pass
    return None


def get_current_ip():
    """Получение текущего IP-адреса."""
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    return conn.getresponse().read().decode("utf-8")


def get_geo_ip():
    """Получение текущей геолокации."""
    try:
        g = GeoIP2()
        address = get_current_ip()
        return g.city(address)
    except ObjectDoesNotExist:
        return None


def save_user_location(user):
    """Сохранение геолокации пользователя."""
    if user and user.is_authenticated and user.is_geoip_allowed:
        data = get_geo_ip()
        if data:
            values_for_update = {
                "lon": data["longitude"],
                "lat": data["latitude"],
            }
            UserLocation.objects.update_or_create(
                user=user, defaults=values_for_update
            )


def get_user_location(user):
    """Получение координат пользователя."""
    if user and user.is_authenticated and user.is_geoip_allowed:
        data = get_object_or_404(UserLocation, user=user)
        return {"latitude": data.lat, "longitude": data.lon}
    return None


def get_user_distance(user1, user2, location2=None):
    """Получение расстояния между пользователями."""
    data1 = get_user_location(user1)
    if location2 is None:
        data2 = get_user_location(user2)
        if data2:
            location2 = (data2["latitude"], data2["longitude"])
    else:
        if not (user2 and user2.is_authenticated and user2.is_geoip_allowed):
            location2 = None
    if data1 and location2:
        return {
            "distance": round(
                gd((data1["latitude"], data1["longitude"]), location2).km, 3
            )
        }
    return None


def save_event_location(event, validated_data):
    """Сохранение геолокации мероприятия."""
    if event:
        if "city" in validated_data:
            city = validated_data["city"]
        else:
            city = event.city
        if "address" in validated_data:
            address = validated_data["address"]
        else:
            address = event.address
        data = None
        if city and address:
            data = get_geo_event(city, address)
            if data:
                values_for_update = {"lon": data[1], "lat": data[0]}
                EventLocation.objects.update_or_create(
                    event=event, defaults=values_for_update
                )


def get_event_location(event):
    """Получение координат мероприятия."""
    if event:
        data = get_object_or_404(EventLocation, event=event)
        return {"latitude": data.lat, "longitude": data.lon}
    return None


def get_event_distance(user, event, location2=None):
    """Получение расстояния между пользователем и мероприятием."""
    data1 = get_user_location(user)
    if location2 is None:
        data2 = get_event_location(event)
        if data2:
            location2 = (data2["latitude"], data2["longitude"])
    else:
        if not event:
            location2 = None
    if data1 and location2:
        return {
            "distance": round(
                gd((data1["latitude"], data1["longitude"]), location2).km, 3
            )
        }
    return None
