from flask import render_template, jsonify, request
from contact import app
from contact.config import config
from urllib import request as http_request
import json


def authentic(ip, token):
    data = json.dumps({
        "id": config.VAPTCHA_VID,
        "secretkey": config.VAPTCHA_SECRETKEY,
        "scene": 2,
        "token": token,
        "ip": ip
    })
    data = data.encode('utf-8')
    req = http_request.Request('http://0.vaptcha.com/verify')
    req.add_header('Content-type', 'application/json')
    response = http_request.urlopen(req, data)
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    json_obj = json.loads(data.decode(encoding))
    if 'success' in json_obj and json_obj['success'] == 1:
        return True, ''
    else:
        return False, json_obj['msg']


def send_mail(form):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    msg = MIMEText(form.get('content', ''), 'html', 'utf-8')
    msg['Subject'] = Header('Message From ' + form.get('name'), 'utf-8',).encode()
    try:
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls()
        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        server.sendmail(config.FROM_ADDRESS, config.TO_ADDRESS, msg.as_string())
    except:
        return False
    server.quit()
    return True


def send_grid_api(form):
    value = """<p>{}</p></br>
    </br>
    {}</br>
    {}
    """.format(form.get('content'), form.get('name'), form.get('contact'))
    data = json.dumps({
        "personalizations": [{"to": [{"email": config.TO_ADDRESS, 'name': form.get('name')}]}],
        "from": {"email": config.FROM_ADDRESS, "name": "ContactMe"},
        "subject": 'Message From ' + form.get('name'),
        "content": [{"type": "text/html", "value": value}]
    })

    data = data.encode('utf-8')

    req = http_request.Request('https://api.sendgrid.com/v3/mail/send')
    req.add_header('Authorization', 'Bearer {}'.format(config.API_KEY))
    req.add_header('Content-type', 'application/json')
    try:
        http_request.urlopen(req, data)
    except:
        return False

    return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    form = request.form
    ip_addr = request.headers.get('X-Real-IP', request.remote_addr)
    if 'token' not in form:
        return jsonify(status='fail', message='Need Authentic')
    success, msg = authentic(ip_addr, form['token'])
    if not success:
        return jsonify(status='fail', message="Authentic Failed:"+msg)
    if config.SMTP:
        success = send_mail(form)
    elif config.SENDGRID:
        success = send_grid_api(form)
    if not success:
        return jsonify(status='fail', message="Send EMail Fail")
    else:
        return jsonify(status='success')
