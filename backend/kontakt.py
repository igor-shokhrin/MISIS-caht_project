
# Импортируем нужные модули
from urllib.request import urlretrieve
import vk, os, time, math

# Авторизация

login = ''
password = ''
vk_id = '6889284'

session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password)

vkapi = vk.API(session)

print(vkapi.users.get(fields="photo_200_orig",v="2.0.2",))