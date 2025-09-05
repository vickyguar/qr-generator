import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr

def send_email(sender_email: str, 
               password: str, 
               sender_name: str, 
               recipient_email: str, 
               subject: str,
               body: str, 
               attachment_path: str) -> None:
    """
    Given a recipient and an attachment, send an email with the attachment to the recipient.
    Args are self-explanatory.
    """
    # Create the email message
    message = MIMEMultipart()
    message['From'] = formataddr((sender_name, sender_email))
    message['To'] = recipient_email
    message['Subject'] = subject

    # Cuerpo del mensaje en UTF-8
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    # Attach the file
    with open(attachment_path, 'rb') as attachment_file:
        attachment = MIMEApplication(attachment_file.read(), _subtype='png')
        attachment.add_header('Content-Disposition', 'attachment', filename=attachment_path)
        message.attach(attachment)

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, password)
            smtp.sendmail(sender_email, recipient_email, message.as_string())
        print(f'Email to {recipient_email} sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')