killall ffserver
killall python3
python3 ./manage.py runserver 0.0.0.0:8000 &
python3 ./WebDetector/server.py &
ffserver -d -f ./WebDetector/ffserver.conf &
python3 ./WebDetector/facerec_from_video_file.py