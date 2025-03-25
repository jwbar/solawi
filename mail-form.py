from flask import Flask, render_template, request, flash, redirect
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Initialize SendGrid client with your API key
sg = SendGridAPIClient('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')

@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Verify reCAPTCHA first
        recaptcha_response = request.form.get('g-recaptcha-response')
        recaptcha_secret = '6LdjxdoqAAAAAC904axqt8pSGl4QWkkF90dIlICr'
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_verification = requests.post(verify_url, data={
            'secret': recaptcha_secret,
            'response': recaptcha_response
        })
        result = recaptcha_verification.json()

        if not result.get('success'):
            flash('reCAPTCHA failed. Please try again.', 'danger')
            return redirect('/')

        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        topic = request.form.get('topic')
        message = request.form.get('message')

        # Create the email content
        email_content = f"Name: {name}\nEmail: {email}\nTopic: {topic}\nMessage:\n{message}"
        msg = Mail(
            from_email='fresh@katari.farm',  # Sender's email address
            to_emails='katarifarms22@gmail.com',  # Recipient's email address
            subject=f"Contact Form Submission: {topic}",
            plain_text_content=email_content
        )

        try:
            response = sg.send(msg)
            app.logger.info(f"Response Status Code: {response.status_code}")
            app.logger.info(f"Response Body: {response.body}")
            app.logger.info(f"Response Headers: {response.headers}")
            flash('Message sent successfully.', 'success')
        except Exception as e:
            app.logger.error(f"Failed to send message. Error: {str(e)}")
            flash(f'Failed to send message. Error: {str(e)}', 'error')

        return redirect('/')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5003)
