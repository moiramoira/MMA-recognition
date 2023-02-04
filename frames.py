import json
import pafy
import cv2
import os
import math

# Opening JSON file
f = open('l.json')
data = json.load(f)

for i in data['links']:
    try:
        # creating a folder named data
        if not os.path.exists(i):
            os.makedirs(i[-9:])

    # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    url = i
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")

    currentframe = 0
    cap = cv2.VideoCapture(best.url)
    frameRate = cap.get(5)  # frame rate
    while True:
        frameId = cap.get(1)  # current frame number
        ret, frame = cap.read()

        if ret:
            if (frameId % math.floor(frameRate) == 0):
                name = i[-9:]+'/' + str(currentframe) + '.jpg'
                print('Creating...' + name)
                cv2.imwrite(name, frame)
                currentframe += 1
        else:
            break

# Closing file
f.close()