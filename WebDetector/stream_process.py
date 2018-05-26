import cv2
import subprocess


class Streamer:
    def __init__(self, src, output_url, fps, color_pattern):
        self.width = int(src.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(src.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.output_url = output_url
        self.dimension = '{}x{}'.format(self.width, self.height)
        self.fps = fps
        self.color_pattern = color_pattern

    def open_stream_process(self):
        """
        create a subprocess which streams the input numpy arrays formatted to string
        to ffserver in background
        :return: the reference of created subprocess
        """
        command = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', self.dimension,
            '-pix_fmt', self.color_pattern,
            '-r', self.fps,
            '-i', '-',
            '-an',
            '-vcodec', 'mpeg4',
            '-b:v', '5000k',
            self.output_url
        ]
        return subprocess.Popen(' '.join(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

