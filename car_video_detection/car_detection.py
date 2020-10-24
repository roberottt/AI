import cv2

video = cv2.VideoCapture('video1.avi')

car_cascade = cv2.CascadeClassifier('cars.xml')

while True:
    retorned, frames = video.read() # read() function returns true if a frame is correctly loaded and false if it's not 
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    for(x,y,w,h) in cars:
        cv2.rectangle(frames,(x,y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imshow('Cars', frames)

    if(cv2.waitKey(33) == 27):
        break

cv2.destroyAllWindows()