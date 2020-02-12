import gbvision as gbv
import streamlink as sl
import numpy as np
from collections import deque
import abc

FPS = 30
MATCH_TIME = 2.5 * 60
extra_time = 0


def get_stream_url(twitch_id = 'firstinspires', youtube_id = None, quality):
    """
    get stream url by twitch id or youtube video id (NOT URL)

    :param twitch_id: Twitch channel id
    :param youtube id: Youtube video id (youtube.com/watch? *ID*)
    :param quality: quality of the stream, options are: 160p, 360p, 480p, 720p, best, wrost

    :return: video stream url
    """
    stream_url = ''
    if youtube_id != None: #we are using youtube
        stream_url = f'https://www.youtube.com/watch?{youtube_id}'
        
    else: #we are using twitch
        stream_url = f'https://www.twitch.tv/{twitch_id}'

    try:
        stream = sl.streams(stream_url)[quality].url
    except KeyError:
        print ("Stream is not online or quality is not correct")
        return -1
    return stream
        
class StreamRecorder(abc.ABC):
    def __init__(self, seconds_buffer, extra_seconds, stream_url):
        """
        abstract class for stream recorder

        :param seconds_buffer: How much time you enter into the buffer
        :param extra_seconds: How much time to record directly into the recorder
        """
        self.stream = gbv.USBCamera(stream_url)
        self.recorder = gbv.OpenCVRecorder(f"video/match{i}.mp4", FPS)
        self.buffer = deque(maxlen = seconds_buffer)
        self.extra_seconds = extra_seconds

    @abc.abstractmethod    
    def trigger(self):
        pass
    def run(self):
        """
        Run the recorder for a game
        """
        while True:
            _,frame = self.stream.read()
            self.buffer.append(frame)
            if self.trigger():
                for f in reversed(self.buffer):
                    self.recorder.record(frame)
                for _ in range(self.extra_seconds):
                    _,frame = self.stream.read()
                    self.recorder.record(frame)
                break

class EndRecorder(StreamRecorder):
    def __init__(self, stream_url):
        """
        Recorder that is taking signal only at the end of the game and then dumps the buffer desired time backwards

        :param stream_url: stream_url taken from helper function
        """
        super().__init__((MATCH_TIME + extra_time) * FPS, extra_time * FPS)

    def trigger(): #TODO implement vision
        pass
        

class StartRecorder():
    def __init__(self, stream_url):
        """
        Recorder that is taking signal at the start of the game and then records the game with the extra time

        :param stream_url: stream_url taken from helper function
        """
        super().__init__(extra_time * FPS, (MATCH_TIME +extra_time) * FPS)

    def trigger(): #TODO implement vision
        pass

        
        

def main():
    #TODO: implement game loop
