from flask import Flask, jsonify, request

import smtplib

app = Flask(__name__)

# SET EMAIL LOGIN REQUIREMENTS
gmail_user = 'acusltdco@gmail.com'
gmail_app_password = 'nfifkbnrnwoedoth'

# Endpoint to trigger the email sending
@app.route('/send_email', methods=['GET'])
def send_email():
    # Get parameters from the query string
    sent_to = request.args.getlist('to', type=str)
    sent_subject = request.args.get('subject', default='Default Subject', type=str)
    sent_body = request.args.get('body', default='Default Body', type=str)

    # SET THE INFO ABOUT THE SAID EMAIL
    sent_from = gmail_user

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text)
        server.close()

        response = {'status': 'success', 'message': 'Email sent!'}
    except Exception as exception:
        response = {'status': 'error', 'message': f'Error: {exception}'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
