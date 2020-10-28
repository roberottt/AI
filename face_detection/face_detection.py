import cv2
import sys

imagePath = sys.argv[1] # With this we'll read the first argument passed in the terminal
faceCascadePath = "haarcascade_frontalface_default.xml"
eyeCascadePath = "haarcascade_eye.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(faceCascadePath)
eyeCascade = cv2.CascadeClassifier(eyeCascadePath)

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # We read the image and then we pass it to gray scale

# Detect faces and eyes in the image
faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
eyes = eyeCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))

print("Found " + str(len(faces)) +" faces")
print("Found " + str(len(eyes)) + " eyes")

# Draw a rectangle around the faces and eyes
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

for (i, j, k, g) in eyes:
    cv2.rectangle(image, (i, j), (i+k, j+g), (0, 0, 255), 2)

cv2.imshow("Faces found", image)
cv2.waitKey(0)

"""
The detectMultiScale function is a general function that detects objects. Since we are calling it on the face cascade, that’s what it detects.

The first option is the grayscale image.

The second is the scaleFactor. Since some faces may be closer to the camera, they would appear bigger than the faces in the back. The scale factor compensates for this.

The detection algorithm uses a moving window to detect objects. minNeighbors defines how many objects are detected near the current one before it declares the face found. minSize, meanwhile, gives the size of each window.
"""