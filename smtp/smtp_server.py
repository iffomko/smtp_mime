import getpass
import logging
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class SmtpServer:
    def __init__(self, settings: dict):
        self.__settings = settings
        self.__server = None
        self.__extensions = [
            'jpeg',
            'jpg',
            'png',
            'gif',
            'pdf',
            'svg',
            'bmp'
        ]

    @staticmethod
    def find_last_dot(name: str) -> int:
        index = -1

        for i in range(0, len(name)):
            if name[i] == '.':
                index = i

        return index

    def __send(self):
        message = MIMEMultipart()
        message['From'] = self.__settings['from']
        message['To'] = self.__settings['to']
        message['Subject'] = self.__settings['subject']

        self.__attach_images(self.__settings['directory'], message)

        self.__server.send_message(message)

    def __attach_images(self, directory: str, message: MIMEMultipart):
        for file in os.listdir(directory):
            path = os.path.join(directory, file)

            index_last_dot = self.find_last_dot(file)

            if index_last_dot == -1:
                continue

            extension = file[(index_last_dot+1):len(file)]

            if (os.path.isfile(path)) and (extension in self.__extensions):
                with open(path, 'rb') as image:
                    img = MIMEImage(image.read())
                    img.add_header('Content-Disposition', 'attachment', filename=file)
                    message.attach(img)

    def send_message(self):
        if self.__settings['ssl']:
            self.__server = smtplib.SMTP_SSL(self.__settings.get('ip'), self.__settings.get('port'))
        else:
            self.__server = smtplib.SMTP(self.__settings.get('ip'), self.__settings.get('port'))

        self.__server.ehlo()
        self.__server.starttls()
        self.__server.ehlo()

        if self.__settings['verbose']:
            logging.basicConfig(level=logging.DEBUG)
            self.__server.set_debuglevel(1)

        if self.__settings.get('auth'):
            password = getpass.getpass('Введите пароль: ')

            try:
                self.__server.login(self.__settings['from'], password)
            except smtplib.SMTPAuthenticationError as e:
                print(e)
            except smtplib.SMTPRecipientsRefused as e:
                print(e)

        self.__send()
        self.__server.close()
