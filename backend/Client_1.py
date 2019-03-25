import requests
dictToSend = {'cmd':'VK_Autorization', 'username' : "+79773947459", 'password':"123as"}
res = requests.post('http://localhost:5000/tests/endpoint', json=dictToSend)
print('response from server:',res.text)
dictFromServer = res.json()