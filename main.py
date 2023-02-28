import pandas as pd
import smtplib
from email.message import EmailMessage


def format_mail(template, keywords, recipient_row) -> str:
    for key in keywords:
        to_replace = f'[{key}]'
        new_value = str(recipient_row[str(key)])
        template = template.replace(to_replace, new_value)
    return template

def send_mail(email) -> bool:
    import config

    try:
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(config.email,config.password)
            smtp.send_message(email)
    except smtplib.SMTPException:
        return False
    
    return True


if __name__ == '__main__':
    template = ''
    template_path = 'mail.txt'

    with open(template_path) as f:
        template = f.read()
    
    recipients = []
    recipients_path = 'recipients.csv'

    df = pd.read_csv(recipients_path, delimiter=';')
    keywords = df.columns.values.tolist()

    for _, recipient_row in df.iterrows():
        info = recipient_row.to_dict()
        mail_text = format_mail(
            template, 
            keywords, 
            info
        )
        email = EmailMessage()
        email['from'] = info['from']
        email['to'] = info['receiver_email']
        email['subject'] = info['subject']
        email.set_content(mail_text)
        if not send_mail(email):
            print(f'[Error with] {info["receiver_email"]}')

    print('Done!')
