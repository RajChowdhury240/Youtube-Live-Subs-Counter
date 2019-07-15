import requests as rq
import json,cv2,bs4
import PySimpleGUI as sg

layout = [
              [sg.Text('Username', size=(15, 1)), sg.InputText()],
              [sg.Ok(bind_return_key=True)]
             ]

window = sg.Window('Youtube Live Sub Count', layout)
event, values = window.Read()

url = rq.get("https://www.youtube.com/user/"+values[0])
soup = bs4.BeautifulSoup(url.text,'html.parser')
name=soup.find('title')
url=soup.find('link',{'rel':'image_src'})
img_data = rq.get(url['href']).content
with open("youtube.jpg", 'wb+') as f:
    f.write(img_data)

text=name.text.strip()[:-11]

img = cv2.imread('youtube.jpg')
img = cv2.resize(img, (288, 288))
row, col= img.shape[:2]
bottom= img[row-2:row, 0:col]
mean= cv2.mean(bottom)[0]

bordersize=300
border=cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize+80, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[43,48,196] )

font = cv2.FONT_HERSHEY_SIMPLEX
# get boundary of this text
textsize = cv2.getTextSize(text, font, 1, 2)[0]

# get coords based on boundary
textX = (border.shape[1] - textsize[0]) / 2.5
textY = (border.shape[0] + textsize[1]) / 1.5

subX = (border.shape[1] - textsize[0]) / 1.8
subY = (border.shape[0] + textsize[1]) / 1.3

# add text centered on image
cv2.putText(border, text, (int(textX), int(textY) ), font, 1.5, (255, 255, 255), 2)

while True:
    b = border
    key = "AIzaSyBc-Qw6yQqmT7oTgzl7xjTAX1fj4cdYh4w"
    data = rq.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + values[0] + "&key=" + key)
    subs = json.loads(data.text)["items"][0]["statistics"]["subscriberCount"]
    print(subs)
    cv2.putText(border, subs, (int(subX), int(subY) ), font, 1.5, (255, 255, 255), 2)
    #cv2.imwrite('image.jpg', border)
    image = cv2.resize(border, (444, 484))
    cv2.imshow('subs', image)
    if cv2.waitKey(1) == ord('q'):
        break
    cv2.putText(border, subs, (int(subX), int(subY)), font, 1.5, (43,48,196), 2)
    border = b

# display image


