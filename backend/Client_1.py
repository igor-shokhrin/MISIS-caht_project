import requests
# dictToSend = {'cmd':'VK_Autorization', 'username' : "+79773947459", 'password':"pass"}
# dictToSend = {'cmd':'get_msg'} # Get messaging
# dictToSend = {'cmd':'send_msg', "text": "blabla", "id_dialog":"1", "id_user": "1"} #Write mess in DB
# dictToSend = {'cmd':'create_new_user', "first_name": "Ivan", "last_name": "Vanin", "pas": "Password", "login": "ivan", "D_birth":"24.11.1999", "age": "19", "sex": "Male", "city": "Moscow"} #Create new user
# dictToSend = {'cmd':'create_new_dialog', "Name": "Managers", "create_date":"29.04.2019", "capacity": "10"} # Create new dialog
# dictToSend = {'cmd':'get_users'} #Get users
dictToSend = {'cmd':'get_user_info', "id_user" : 8} #Get user info
# dictToSend = {'cmd':'get_dialogs'} #Get dialog
# dictToSend = {'cmd':'login', "pas": "Password1", "login": "ivan"} #Create new user
# dictToSend = {'cmd':'test'} #Get user
# res = requests.post('http://localhost:5000/tests/endpoint', json=dictToSend)

res = requests.post('http://192.168.31.195:5000/tests/endpoint', json=dictToSend)
print('response from server:', res.text)
dictFromServer = res.json()