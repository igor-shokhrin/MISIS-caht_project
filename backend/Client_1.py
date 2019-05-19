import requests
# dictToSend = {'cmd':'VK_Autorization', 'username' : "+79773947459", 'password':"pass"}
# dictToSend = {'cmd':'get_msg'} # Get messaging
# dictToSend = {'cmd':'send_msg', "text": "blabla", "id_dialog":"1", "id_user": "1"} #Write mess in DB
# dictToSend = {'cmd':'create_new_user', "first_name": "Admin", "last_name": "adminich", "pas": "admin", "login": "admin", "D_birth":"1.11.666", "age": "666", "sex": "Male", "city": "NY"} #Create new user
# dictToSend = {'cmd':'create_new_dialog', "Name": "Managers", "create_date":"29.04.2019", "capacity": "10"} # Create new dialog
dictToSend = {'cmd':'get_users'} #Get users
# dictToSend = {'cmd':'get_user_info', "id_user" : 8} #Get user info
# dictToSend = {'cmd':'get_dialogs'} #Get dialog
# dictToSend = {'cmd':'login', "pas": "admin", "login": "admin"} #Create new user
# dictToSend = {'cmd':'test'} #Get user
# dictToSend = {'cmd':'get_user_from_dialog', "id_dialog": 1} #Get user from dialogs
# res = requests.post('http://localhost:5000/tests/endpoint', json=dictToSend)

res = requests.post('http://192.168.31.195:5000/tests/endpoint', json=dictToSend)
print('response from server:', res.text)
dictFromServer = res.json()