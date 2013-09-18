from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email.header import Header
from email import Encoders
import smtplib


class Message(object):
  """An email message"""

  def __init__(self):
    self._sender      = 'simplemail@example.com'
    self._recipients  = []
    self._subject     = ''
    self._format      = 'plain'
    self._body        = ''
    self._encoding    = 'utf-8'
    self._attachments = []

  def sender(self, sender=None):
    """Get or set email sending this message"""
    if sender is None:
      return self._sender
    else:
      self._sender = sender
      return self

  def recipients(self, recipients=None):
    """Get or set all recipients of this email"""
    if recipients is None:
      return self._recipients
    else:
      self._recipients = recipients
      return self

  def recipient(self, recipient):
    """Add a single recipient"""
    self._recipients.append(recipient)
    return self

  def subject(self, subject=None):
    """Set or get email's subject line"""
    if subject is None:
      return self._subject
    else:
      self._subject = subject
      return self

  def format(self, format=None):
    """`plain` or `html`"""
    if format is None:
      return self._format
    else:
      self._format = format
      return self
  def body(self, body=None):
    """Body text of email"""
    if body is None:
      return self._body
    else:
      self._body = body
      return self

  def encoding(self, encoding=None):
    """text encoding of email body (if not utf8)"""
    if encoding is None:
      return self._encoding
    else:
      self._encoding = encoding
      return self

  def attachments(self, attachments=None):
    """Set or get all attachments"""
    if attachments is None:
      return self._attachments
    else:
      self._attachments = attachments
      return self

  def attachment(self, attachment):
    """Add a single attachment"""
    self._attachments.append(attachment)
    return self

  def build(self):
    """build message string"""
    msg = MIMEMultipart()
    msg['From']     = self._sender
    msg['To']       = COMMASPACE.join(self._recipients)
    msg['Date']     = formatdate(localtime=True)
    msg['Subject']  = Header(self._subject, self._encoding)

    # add body of email
    msg.attach(MIMEText(
      self._body.encode(self._encoding),
      _subtype=self._format,
      _charset=self._encoding
    ))

    # add attachments
    for f in self._attachments:
      # was f a path or an actual file?
      is_path = isinstance(f, basestring)

      part = MIMEBase('application', 'octet-stream')
      if is_path:
        f = open(f, "rb")
        opened_locally = True
      part.set_payload( f.read() )
      Encoders.encode_base64(part)
      part.add_header('Content-Disposition', 'attachment; filename="%s"' % (f.name,))
      msg.attach(part)

      if is_path:
        f.close()
      else:
        f.seek(0)

    return msg.as_string()

  def __unicode__(self):
    s = []
    s.append(u"sender=%s" % self.sender())
    s.append(u"recipients=%s" % self.recipients())
    s.append(u"subject=%s" % self.subject())
    s.append(u"format=%s" % self.format())
    s.append(u"body=%s" % self.body())
    s.append(u"encoding=%s" % self.encoding())
    s.append(u"attachments=%s" % self.attachments())

    return u"Message(%s)" % (u", ".join(s))

  def __str__(self):
    return unicode(self).encode("ascii", "replace")

  def __repr__(self):
    return str(self)


class SMTP(object):
  """Connection to an SMTP service"""

  def __init__(self):
    self._host     = 'smtp.gmail.com'
    self._port     = None
    self._username = None
    self._password = None

  def host(self, host=None):
    """Set host; e.g. smtp.gmail.com"""
    if host is None:
      return self._host
    else:
      self._host = host
      return self

  def port(self, port=None):
    """Set post to connect to host

    Defaults to 25 if username/password is unset; else 587
    """
    if port is None:
      return self._port
    else:
      self._port = port
      return self

  def username(self, username=None):
    """Set username to login with"""
    if username is None:
      return self._username
    else:
      self._username = username
      return self

  def password(self, password=None):
    """Set password to login with"""
    if password is None:
      return self._password
    else:
      self._password = password
      return self

  def send(self, message):
    """Send a `Message` object"""
    # choose port
    if self._port is not None:
      port = self._port
    else:
      if self._username is not None and self._password is not None:
        port = 587
      else:
        port = 25

    smtp = smtplib.SMTP(self._host, port)
    if self._username is not None and self._password is not None:
      smtp.ehlo()
      smtp.starttls()
      smtp.ehlo()
      smtp.login(self._username, self._password)
    smtp.sendmail(message.sender(), message.recipients(), message.build())
    smtp.close()

  def __unicode__(self):
    s = []
    s.append(u"host=%s" % self.host())
    s.append(u"port=%s" % self.port())
    s.append(u"username=%s" % self.username())
    s.append(u"password=%s" % self.password())

    return u"SMTP(%s)" % (u", ".join(s))

  def __str__(self):
    return unicode(self).encode("ascii", "replace")

  def __repr__(self):
    return str(self)


class ChainmailException(Exception):
  pass
