import cv2
import gbvision as gbv
import streamlink as sl
from collections import deque
import abc

FPS = 30
MATCH_TIME = 2.5 * 60
extra_time = 10


THRESHOLD = gbv.ColorThreshold([[0, 22], [0, 20], [234, 255]], 'BGR')


class StreamNotFound(Exception):
    """
    Rasied if stream was not found
    """
    pass


def get_stream_url(twitch_id='firstinspires', youtube_id=None, quality='480p'):
    """
    get stream url by twitch id or youtube video id (NOT URL)

    :param twitch_id: Twitch channel id
    :param youtube_id: Youtube video id (youtube.com/watch? *ID*)
    :param quality: quality of the stream, options are: 160p, 360p, 480p, 720p, best, worst

    :return: video stream url, -1 if stream not found
    """
    if youtube_id is not None:  # we are using youtube
        stream_url = f'https://www.youtube.com/watch?{youtube_id}'

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


class EndRecorder(StreamRecorder):
    def __init__(self, stream_url, filename):
        """
        Recorder that is taking signal only at the end of the game and then dumps the buffer desired time backwards

        :param stream_url: stream_url taken from helper function
        """
        super().__init__(int((MATCH_TIME + extra_time) * FPS), int(extra_time * FPS), stream_url, filename)

    def trigger(self):
        new_frame = gbv.crop(self.frame, 522, 618, 78, 17)
        after_threshold = THRESHOLD(new_frame)
        print (after_threshold)
        if after_threshold.min() == 255:
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
    i = 0
    while True:
        recorder = EndRecorder('match.mp4', f'match{i}')
        recorder.run()
        i += 1
        del recorder


if __name__ == '__main__':
    main()
