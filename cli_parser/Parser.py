import os


class Parser:
    @staticmethod
    def parse(args: list) -> dict:
        settings = dict()

        if '-h' in args or '--help' in args:
            settings['help'] = True
            settings['help_text'] = '-h/--help - справка\n' \
                                    '--ssl - разрешить использование ssl, если сервер поддерживает ' \
                                    '(по умолчанию не использовать)\n' \
                                    '-s/--server - адрес (или доменное имя) SMTP-сервера в формате адрес[:порт] ' \
                                    '(порт по умолчанию 25)\n' \
                                    '-t/--to - почтовый адрес получателя письма\n' \
                                    '-f/--from - почтовый адрес отправителя (по умолчанию <>)\n' \
                                    '--subject - необязательный параметр, задающий тему письма, ' \
                                    'по умолчанию тема “Happy Pictures”\n' \
                                    '--auth - запрашивать ли авторизацию (по умолчанию нет), ' \
                                    'если запрашивать, то сделать это после запуска, без отображения пароля\n' \
                                    '-v/--verbose - отображение протокола работы (команды и ответы на них), ' \
                                    'за исключением текста письма\n' \
                                    '-d/--directory - каталог с изображениями (по умолчанию $pwd)\n'
            return settings

        settings['help'] = False

        if '-s' not in args and '--server' not in args:
            print('Вы не ввели ip и порт для сервера')
            return dict()

        server_key = '-s'

        if '--server' in args:
            server_key = '--server'

        if '-t' not in args and '--to' not in args:
            print('Вы не указали email получателя')
            return dict()

        to_key = '-t'

        if '--to' in args:
            to_key = '--to'

        # ssl

        if '--ssl' in args:
            settings['ssl'] = True

        settings['ssl'] = False

        # server ip and port

        server = args[args.index(server_key) + 1]

        double_dot_index = server.find(':')

        if double_dot_index == -1:
            settings['ip'] = server
            settings['port'] = 25
        else:
            settings['ip'] = server[0:server.find(':')]
            settings['port'] = int(server[(server.find(':') + 1):len(server)])

        # to email

        settings['to'] = args[args.index(to_key) + 1]

        # from email

        settings['from'] = '<>'

        from_key = None

        if '--from' in args:
            from_key = '--from'

        if '-f' in args:
            from_key = '-f'

        if from_key is not None:
            settings['from'] = args[args.index(from_key) + 1]

        # subject

        settings['subject'] = 'Happy Pictures'

        if '--subject' in args:
            settings['subject'] = args[args.index('--subject') + 1]

        # auth

        settings['auth'] = False

        if '--auth' in args:
            settings['auth'] = True

        # verbose

        settings['verbose'] = False

        if '-v' in args or '--verbose' in args:
            settings['verbose'] = True

        # directory

        settings['directory'] = os.getcwd()

        dir_key = None

        if '-d' in args:
            dir_key = '-d'

        if '--directory' in args:
            dir_key = '--directory'

        if dir_key is not None:
            settings['directory'] = args[args.index(dir_key) + 1]

        return settings
