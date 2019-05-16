import requests
# dictToSend = {'cmd':'VK_Autorization', 'username' : "+79773947459", 'password':"IgorEK1997"}
# dictToSend = {'cmd':'get_msg'} # Get messaging (Not Working for now:))
# dictToSend = {'cmd':'send_msg', "text": "blabla", "id_dialog":"1", "id_user": "1"} #Write mess in DB
# dictToSend = {'cmd':'create_new_user', "Name": "Andrew", "D_birth":"24.11.1999", "age": "19", "sex": "Male", "city": "Moscow"} #Create new user
# dictToSend = {'cmd':'create_new_dialog', "Name": "Managers", "create_date":"29.04.2019", "capacity": "10"} # Create new dialog
# dictToSend = {'cmd':'get_users'} #Get user
dictToSend = {'cmd':'get_dialogs'} #Get dialog
res = requests.post('http://localhost:5000/tests/endpoint', json=dictToSend)
print('response from server:', res.text)
dictFromServer = res.json()