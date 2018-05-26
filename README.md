#@ WebDetector

### Application Points
Streaming detected results in nearly real time to browser so that the managers of some facilities are able to access the monitoring view In any place through Internet or LAN.
![img](http://p9cfwszun.bkt.clouddn.com/wd1.PNG)
![img](http://p9cfwszun.bkt.clouddn.com/wd2.PNG)

### Environment
Make sure that the following pacages have been installed in your working machine

- FFServer
- twisted
- websocket-client
- opencv
- Django
- dlib
- face_recornition

### Quick Start
U can start the project simply by running the following shell script. in the case, the stream that ffserver going to receive is from a video file,if U perfer face recornition from a camera, just change the argument in the last command line in `start.sh` from `facerec_from_video_file.py` to `webcam.py`
```shell
sh startup.sh
```

### Usage
After the ffserver started, you can push your stream from a video file
or from a camera,and once the HTTP connection established, the front ground will pull and showthe stream.
U can also acess the result page in a different host, just ensure that you two machines are under the same LAN,and just type a url as follow
```
http://serverIP:8000
```

### Advanced
WebDetector is just a way to show real-time stream through B/S, with MaskRCNN.etc, you can amplify its meaning.
![img](http://p9cfwszun.bkt.clouddn.com/Screenshot%20from%202018-05-24%2022-35-17_LI.jpg)
