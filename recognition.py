import cv2
import numpy as np
from yolov5Detect import Detector
detector = Detector()
detector.load()
import easyocr
import math
import json

# Opening JSON file
f = open('yolo_classes.json')
classes = json.load(f)
f.close()


reader = easyocr.Reader(['en'], gpu=True)


def recognition(img):
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    targetBoxes = detector.detect_bbox(img)
    results = []
    for targetBox in targetBoxes:
        # Extract the class, confidence, and bounding box coordinates
        class_id =classes[str(int(targetBox[5]))]
        confidence = targetBox[4]
        x1, y1, x2, y2 = targetBox[:4]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Draw a box around the object if the confidence is high enough
        if confidence > 0.8:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(img, str(class_id), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


            #crop area and recognize
            x = int(min(targetBox[0], targetBox[2]))
            w = int(abs(targetBox[2] - targetBox[0]))
            y = int(min(targetBox[1], targetBox[3]))
            h = int(abs(targetBox[3] - targetBox[1]))

            image_part = img[y:y + h, x:x + w]
            text = reader.readtext(image_part)
            if class_id == "name" or class_id == "country":
                results.append({"class_id": class_id, "text": text, "color": color(image_part)})
            else:
                results.append({"class_id": class_id, "text": text})

    return img, results


def color(img):
    #define a color
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    blue_lower = np.array([100, 50, 50])
    blue_upper = np.array([140, 255, 255])

    red_lower = np.array([0, 50, 50])
    red_upper = np.array([20, 255, 255])

    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    red_mask = cv2.inRange(hsv, red_lower, red_upper)

    blue_pixels = cv2.countNonZero(blue_mask)
    red_pixels = cv2.countNonZero(red_mask)

    color_dict = {'blue': blue_pixels, 'red': red_pixels}
    most_dominant_color = max(color_dict, key=color_dict.get)
    return most_dominant_color


count = 0
def json_loader(results, res, count):
    for i in results:
        try:
            if i['class_id'] == "overview":
                for j in range(1, len(i["text"]), 3):
                    res["fighter1"][i["text"][j][1]] = i["text"][j - 1][1]
                    res["fighter2"][i["text"][j][1]] = i["text"][j + 1][1]

            if i["class_id"] == "country":
                if i["color"] == 'red':
                    res["fighter1"]["country"] = i['text'][-1][1]
                    res["fighter1"]["name"] = i['text'][0][1] + ' '+ i['text'][1][1]
                    res["fighter1"]["color"] = "red"
                if i["color"] == 'blue':
                    res["fighter2"]["country"] = i['text'][-1][1]
                    res["fighter2"]["name"] = i['text'][0][1] + ' '+ i['text'][1][1]
                    res["fighter2"]["color"] = "blue"

            if i["class_id"] == "time":
                time_str = i['text'][0][1]
                if time_str == '4.52':
                    count += 1
                res["round"] = math.ceil(count / 25)

            if i["class_id"] == "winner":
                res["winner"] = i['text'][0][1]

        except:
            pass

    return res


def digitize(url):
    cap = cv2.VideoCapture(url)

    res = {"fighter1": {},
           "fighter2": {},
           "round": {}}

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    while (cap.isOpened()):
        # Capture frame-by-frame

        ret, frame = cap.read()
        if ret == True:
            recog = recognition(frame)

            r = json_loader(recog[1], res, count)


            # Show the output frame
            cv2.imshow("frame", recog[0])

            # Break the loop if the "q" key is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        else:
            break

    # Release the resources
    cap.release()
    cv2.destroyAllWindows()

    return r


def ann(url, path):
    r = digitize(url)
    json_object = json.dumps(r, indent=4)
    with open(str(path), "w") as outfile:
        outfile.write(json_object)




