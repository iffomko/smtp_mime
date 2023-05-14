import sys

from cli_parser.Parser import Parser
from smtp.smtp_server import SmtpServer


def main():
    settings = Parser().parse(args=sys.argv)

    if settings.get('help'):
        print(settings.get('help_text'))
        return

    try:
        SmtpServer(settings).send_message()
    except ConnectionRefusedError as e:
        print(e)


if __name__ == '__main__':
    main()
