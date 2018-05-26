import face_recognition
import cv2
import datetime
import random
import os
import websocket
import stream_process as sp


websocket.enableTrace(True)
ws = websocket.create_connection("ws://127.0.0.1:9999")

# Open the input video file
input_video = cv2.VideoCapture(os.getcwd() + "/static/short_hamilton_clip.mp4")
length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

# Load some sample pictures and learn how to recognize them.
lmm_image = face_recognition.load_image_file(os.path.abspath('.') + "/static/lin-manuel-miranda.png")
lmm_face_encoding = face_recognition.face_encodings(lmm_image)[0]

al_image = face_recognition.load_image_file(os.path.abspath('.') + "/static/alex-lacamoire.png")
al_face_encoding = face_recognition.face_encodings(al_image)[0]

known_faces = [
    lmm_face_encoding,
    al_face_encoding
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

frame_number = 0

output = "http://localhost:8090/feed1_480p.ffm"
fps = '200'
color_pattern = 'bgr24'
streamer = sp.Streamer(input_video, output, fps, color_pattern)
process = streamer.open_stream_process()

while True:

    # Grab a single frame of video
    ret, frame = input_video.read()
    frame_number += 1

    if not ret:
        break
    # Quit when the input video file ends
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

        # If you had more than 2 faces, you could make this logic a lot prettier
        # but I kept it simple for the demo
        name = None
        if match[0]:
            name = "Lin-Manuel Miranda"
        elif match[1]:
            name = "Alex Lacamoire"

        face_names.append(name)

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        static_dir = "/static/results/" + str(datetime.datetime.now().strftime('%Y-%m-%d'))

        dir_name = os.path.abspath('.') + static_dir
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        i = random.randint(0, 100000)

        img_name = str(datetime.datetime.now().strftime('%H-%M-%S-')) + str(i) + ".jpg"
        relative_img_name = static_dir + "/" + img_name
        full_img_name = dir_name + "/" + img_name

        # write the detected face image in disk
        cv2.imwrite(full_img_name, frame)
        # send the detected face image url to websocket server
        ws.send(relative_img_name)

    result = frame
    process.stdin.write(result.tostring())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

input_video.release()
cv2.destroyAllWindows()
process.stdin.close()
process.wait()
