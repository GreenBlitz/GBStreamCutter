import cv2
import time
import gbvision as gbv
import streamlink as sl
from collections import deque
import abc

YOUTUBE_ID = None
TWITCH_ID = 'testingthetestin'

FPS = 30
MATCH_TIME = 2.5 * 60
extra_time = 10

THRESHOLD = gbv.ColorThreshold([[28, 68], [27, 67], [214, 254]], 'BGR')


class StreamNotFound(Exception):
    """
    Rasied if stream was not found
    """
    pass


def get_stream_url(twitch_id=TWITCH_ID, youtube_id=YOUTUBE_ID, quality='480p'):
    """
    get stream url by twitch id or youtube video id (NOT URL)

    :param twitch_id: Twitch channel id
    :param youtube_id: Youtube video id (youtube.com/watch? *ID*)
    :param quality: quality of the stream, options are: 160p, 360p, 480p, 720p, best, worst

    :return: video stream url, -1 if stream not found
    """
    if youtube_id is not None:  # we are using youtube
        stream_url = f'https://www.youtube.com/watch?v={youtube_id}'

    else:  # we are using twitch
        stream_url = f'https://www.twitch.tv/{twitch_id}'

    try:
        stream = sl.streams(stream_url)[quality].url
    except KeyError:
        raise StreamNotFound
    return stream


class StreamRecorder(abc.ABC):
    def __init__(self, seconds_buffer, extra_seconds, stream_url, filename):
        """
        abstract class for stream recorder

        :param seconds_buffer: How much time you enter into the buffer
        :param extra_seconds: How much time to record directly into the recorder
        """
        self.stream = gbv.USBCamera(stream_url)
        self.recorder = gbv.OpenCVRecorder(f"video/{filename}.avi", FPS)
        self.buffer = deque(maxlen=seconds_buffer)
        self.extra_seconds = extra_seconds
        self.status = self.stream.read()[0]
        self.frame = self.stream.read()[1]

    @abc.abstractmethod
    def trigger(self):
        pass

    def run(self):
        """
        Run the recorder for a game
        """
        while True:
            self.status, self.frame = self.stream.read()
            self.buffer.append(self.frame)
            if self.status:
                if self.trigger():
                    for f in self.buffer:
                        self.recorder.record(f)
                    for _ in range(self.extra_seconds):
                        self.status, self.frame = self.stream.read()
                        self.recorder.record(self.frame)
                    break
            else:
                print('status not')
                self.stream = gbv.USBCamera(get_stream_url())
                self.status, self.frame = self.stream.read()


class EndRecorder(StreamRecorder):
    def __init__(self, stream_url, filename):
        """
        Recorder that is taking signal only at the end of the game and then dumps the buffer desired time backwards

        :param stream_url: stream_url taken from helper function
        """
        super().__init__(int((MATCH_TIME + extra_time) * FPS), int(extra_time * FPS), stream_url, filename)

    def trigger(self):
        new_frame = gbv.crop(self.frame,
                             int(0.411 * self.stream.get_width()),
                             int(0.852 * self.stream.get_height()),
                             50, 15) #THIS IS VALID FOR 480P ONLY
        after_threshold = THRESHOLD(new_frame)
        if after_threshold.min()== 255:
            print('Found match')
            return True
        return False


class StartRecorder(StreamRecorder):
    def __init__(self, stream_url, filename):
        """
        Recorder that is taking signal at the start of the game and then records the game with the extra time

        :param stream_url: stream_url taken from helper function
        """
        super().__init__(extra_time * FPS, (MATCH_TIME + extra_time) * FPS, stream_url, filename)

    def trigger(self):  # TODO implement vision
        pass


def main():
    i = 1
    while True:
        recorder = EndRecorder(get_stream_url(), f'match{i}')
        recorder.run()
        while recorder.trigger():
            time.sleep(1)
        i += 1
        del recorder



if __name__ == '__main__':
    main()
