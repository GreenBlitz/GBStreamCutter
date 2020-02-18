from telegram.ext import Updater, CommandHandler, JobQueue
import telegram
from os import listdir
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
class MyBot:
    def __init__(self, TOKEN):
        self.updater = Updater(TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.i = 0
        start_handler = CommandHandler('start', self.start)
        update_handler = CommandHandler('update', self.update_videos_wrapper)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(update_handler)

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="start")
        self.updater.job_queue.run_repeating(self.update_videos, first=0, interval=180, context=update.message.chat_id)

    def update_videos(self, context):
        length = len(listdir('video'))
        if length > self.i and length > 0:
            file_name = listdir('video')[self.i]
            file_name = file_name[:-4]
            subprocess.call(
                ['ffmpeg', '-i', f'video/{file_name}.avi', '-vcodec', 'libx265', '-crf', '23', f'comp/{file_name}.mp4'])
            self.i += 1
            context.bot.send_video("@GBmatches", open(f'comp/{file_name}.mp4', 'rb'), timeout=60)
            print('sent')

    def update_videos_wrapper(self, context, update):
        self.update_videos(context)

    def run(self):
        self.updater.start_polling()


telebot = MyBot('')
telebot.run()
