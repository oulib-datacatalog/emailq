from celery.task import task
from celery.utils.mail import Message, Mailer
from ConfigParser import ConfigParser
 

config = ConfigParser()
config.read('cybercom.cfg')

mailer = Mailer(
    host=config.get('email', 'host'),
    port=config.getint('email', 'port'),
    user=config.get('email', 'user'),
    password=config.get('email', 'pass'),
    use_tls=config.getboolean('email', 'use_tls')
)


@task()
def sendmail(to, subject=None, body=None):
    """
    Sendmail Task
    
    Sends an email.

    args:
      to: email address to send to
      subject: subject line of email
      body: body text of email
    """

    message = Message(
        to=to,
        sender=config.get('email', 'user'),
        subject=subject,
        body=body
    )
    mailer.send(message)
    return True
