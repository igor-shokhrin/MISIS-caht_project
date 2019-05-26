import requests
# dictToSend = {'cmd':'VK_Autorization', 'username' : "+79259033101", 'password':"abinia081294"}
# dictToSend = {'cmd':'get_msg'} # Get messaging
# dictToSend = {'cmd':'send_msg', "text": "TOP of the WORD", "id_dialog":"1", "id_user": "9"} #Write mess in DB
# dictToSend = {'cmd':'create_new_user', "first_name": "Admin", "last_name": "adminich", "pas": "admin", "login": "admin", "D_birth":"1.11.666", "age": "666", "sex": "Male", "city": "NY", "photo" : "", "status" : ""} #Create new user
# dictToSend = {'cmd':'create_new_dialog', "Name": "Managers", "create_date":"29.04.2019", "capacity": "10"} # Create new dialog
# dictToSend = {'cmd':'get_users'} #Get users
# dictToSend = {'cmd':'get_user_info', "id_user" : 8} #Get user info
# dictToSend = {'cmd':'get_dialogs'} #Get dialog
# dictToSend = {'cmd':'login', "pas": "admin", "login": "admin"} #Create new user
# dictToSend = {'cmd':'registration', "login" : "nagibator5000", "pas" : "123qwe"} #Get user
# dictToSend = {'cmd':'get_msg_from_dialog', "id_dialog": 1} #Get user
# dictToSend = {'cmd':'update_user_info', "id_user": 1, "first_name" : "Вася", "photo" : "photo"} #Get user
# dictToSend = {'cmd':'weather_now', "city": "Moscow"} #Get weather for now
# dictToSend = {'cmd':'weather_to_five_days', "city": "Moscow"} #Get weather for 5 days
# dictToSend = {'cmd':'test'} #Get user
dictToSend = {'cmd':'get_user_from_dialog', "id_dialog": 1} #Get user from dialogs


# res = requests.post('http://localh    ost:5000/tests/endpoint', json=dictToSend)
res = requests.post('http://192.168.31.195:5000/tests/endpoint', json=dictToSend)
# res = requests.post('http://192.168.43.33:5000/tests/endpoint', json=dictToSend)
print('response from server:', res.text)
dictFromServer = res.json()


