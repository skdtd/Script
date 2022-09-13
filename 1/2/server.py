import cv2
import pyautogui
from flask import Flask
from flask import request
import winsound

app = Flask(__name__)

UP = cv2.imread("pic/up.jpg", cv2.IMREAD_GRAYSCALE)
LEFT = cv2.imread("pic/left.jpg", cv2.IMREAD_GRAYSCALE)
DOWN = cv2.imread("pic/down.jpg", cv2.IMREAD_GRAYSCALE)
RIGHT = cv2.imread("pic/right.jpg", cv2.IMREAD_GRAYSCALE)
BOX = cv2.imread("pic/box.jpg", cv2.IMREAD_GRAYSCALE)
PIC_LIST = [UP, LEFT, DOWN, RIGHT]


@app.route("/pic", methods=["POST"])
def pic():
    image = request.files.get("files")
    file_path = "C:/Users/Administrator/Desktop/" + image.filename
    image.save(file_path)

    img = cv2.imread(file_path)
    img = cv2.Canny(img, 280, 400)
    img = img[180:350, 350:930]
    res = cv2.matchTemplate(img, BOX, cv2.TM_CCOEFF_NORMED)
    res = cv2.minMaxLoc(res)
    x, y = res[3]
    img = img[y + 10:y + 70, x + 20:x + 380]
    # cv2.imwrite("./output/test.jpg", img)
    content = ""
    for i in range(4):
        t = img[0:60, i * 90: (i + 1) * 90]
        # cv2.imwrite("./output/test_" + str(i) + ".jpg", t)
        index = -1
        max_score = -1
        try:
            for j in range(4):
                res = cv2.matchTemplate(t, PIC_LIST[j], cv2.TM_CCOEFF_NORMED)
                res = cv2.minMaxLoc(res)[1]
                if max_score < res:
                    index = j
                    max_score = res
            content = content + str(index)
        except cv2.error as e:
            print("9999")
            return "9999"
    print(content)
    return content


@app.route("/alarm", methods=["GET"])
def alarm():
    res = request.args
    # winsound.PlaySound("C:/Users/Administrator/Desktop/alarm.mp3", winsound.SND_ASYNC)
    winsound.Beep(500, 1500)
    pyautogui.alert("虚拟机：" + res.get("id"))
    return "OK"


print("API: /pic")
print("API: /alarm")
app.run("0.0.0.0", 8080)
