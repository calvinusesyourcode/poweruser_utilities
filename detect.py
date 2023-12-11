import cv2

def detect_faces(image_path):
    # Load Haar Cascade Classifiers
    frontal_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    profile_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise Exception("Image not found or unable to load.")

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # First try detecting frontal faces
    faces = frontal_face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    print("1Found {0} faces!".format(len(faces)))
    # If no frontal faces detected, try detecting profile faces
    if len(faces) == 0:
        faces = profile_face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        print("2Found {0} faces!".format(len(faces)))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Output the result
    cv2.imshow("Faces Detected", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detect_faces('testface4.png')
