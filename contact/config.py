class Config:
    TITLE = 'Contact Me'

    SMTP = False
    SMTP_SERVER = 'smt_server'
    SMTP_PORT = '25'
    SMTP_USERNAME = 'user'
    SMTP_PASSWORD = 'password'

    SENDGRID = True
    API_KEY = 'SGKEY'

    FROM_ADDRESS = ''
    TO_ADDRESS = ''

    VAPTCHA_VID = ''
    VAPTCHA_SECRETKEY = ''

    @staticmethod
    def init_app(app):
        pass


config = Config
