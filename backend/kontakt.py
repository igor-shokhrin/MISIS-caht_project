import vk
#from PIL import Image, ImageDraw

vk_id = '6889284'
def get_circle_img(input_img, output_img):
    img = Image.open(input_img)
    bigsize = img.size[0] * 3, img.size[1] * 3
    mask = Image.new('L', bigsize, 0)

    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)

    mask = mask.resize(img.size, Image.ANTIALIAS)
    img.putalpha(mask)
    img.save(output_img)

def get_user_photo(login, password):
    session = vk.AuthSession(app_id="6889284", user_login=login, user_password=password)
    vkapi = vk.API(session)

    # return vkapi.users.get(fields="bdate, city, sex", v="2.0.2")
    return vkapi.users.get(fields="bdate, city, sex, photo_50", v="5.95")

    # return vkapi.users.get(fields="photo_200_orig",v="2.0.2")
# while(1):
#     try:
#         login = input("Enter username\n")
#         password = input("Enter password\n")
#         print(get_user_photo(login, password))
#         exit(0)
#     except Exception:
#         pass
#     print("Incorrect username or password, Please re enter\n")
