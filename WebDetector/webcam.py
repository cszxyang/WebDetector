import face_recognition
import cv2
import os
import stream_process as sp
import websocket
import datetime
import random

websocket.enableTrace(True)
ws = websocket.create_connection("ws://127.0.0.1:9999")

video_capture = cv2.VideoCapture(0)

output = "http://localhost:8090/feed1_480p.ffm"
fps = '200'
color_pattern = 'bgr24'
streamer = sp.Streamer(video_capture, output, fps, color_pattern)
process = streamer.open_stream_process()

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file(os.path.abspath('.') + "/static/lin-manuel-miranda.png")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file(os.path.abspath('') + "/static/alex-lacamoire.png")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "lin-manuel-miranda",
    "alex-lacamoire"
]

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        static_dir = "/static/results/" + str(datetime.datetime.now().strftime('%Y-%m-%d'))

        dir_name = os.path.abspath('.') + static_dir
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        i = random.randint(0, 100000)

        img_name = str(datetime.datetime.now().strftime('%H-%M-%S-')) + str(i) + ".jpg"
        relative_img_name = static_dir + "/" + img_name
        full_img_name = dir_name + "/" + img_name

        cv2.imwrite(full_img_name, frame)
        ws.send(relative_img_name)

    # Display the resulting image
    cv2.imshow('Video', frame)
    result = frame
    process.stdin.write(result.tostring())
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
process.stdin.close()
process.wait()