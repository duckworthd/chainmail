from bs4.dammit             import UnicodeDammit
from email                  import encoders
from email.header           import Header
from email.mime.application import MIMEApplication
from email.mime.audio       import MIMEAudio
from email.mime.base        import MIMEBase
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText
from email.utils            import COMMASPACE, formatdate
import mimetypes
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
    # There can be only ONE ENCODING TO RULE THEM ALL!! MUWAHAHAHA
    subject, body = map(
        lambda x: UnicodeDammit(x).unicode_markup,
        [self._subject, self._body]
      )

    msg = MIMEMultipart()
    msg['From']     = self._sender
    msg['To']       = COMMASPACE.join(self._recipients)
    msg['Date']     = formatdate(localtime=True)
    msg['Subject']  = Header(subject, 'utf-8')

    # add body of email
    msg.attach(MIMEText(
      body,
      _subtype=self._format,
      _charset='utf-8',
    ))

    # add attachments
    for f in self._attachments:
      msg.attach(_build_attachment(f))

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


def _build_attachment(f):
  """Construct appropriate MIME message part for a multi-part email.

  Parameters
  ----------
  f : str or file
      path to content or content itself. Must have a `name` attribute.

  Returns
  -------
  part : MIMEBase or subclass thereof
      content ready to be attached to a `MIMEMultipart`
  """
  is_path = isinstance(f, basestring)

  if is_path:
    # open path as a file
    f = open(f, 'rb')
  else:
    # return to this position later
    position = f.tell()

  ctype, encoding = mimetypes.guess_type(f.name)
  if ctype is None or encoding is not None:
    ctype = 'application/octet-stream'
  maintype, subtype = ctype.split('/', 1)
  if maintype == 'text':
    # Note: we should handle calculating the charset
    content = UnicodeDammit(f.read()).unicode_markup
    part = MIMEText(content, _subtype=subtype, _charset='utf-8')
  elif maintype == 'image':
    part = MIMEImage(f.read(), _subtype=subtype)
  elif maintype == 'audio':
    part = MIMEAudio(f.read(), _subtype=subtype)
  elif maintype == 'application':
    part = MIMEApplication(f.read(), _subtype=subtype)
  else:
    part = MIMEBase(maintype, subtype)
    part.set_payload(f.read())
    encoders.encode_base64(part)

  part.add_header('Content-Disposition', 'attachment', filename=f.name)

  if is_path:
    f.close()
  else:
    f.seek(position)

  return part
