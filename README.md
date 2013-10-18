chainmail
=========

`chainmail` is a Python library for constructing and sending email.

Installation
============

```bash
$ pip install chainmail
```

Usage
=====

```python
import chainmail

message = (
  chainmail.Message()
  .sender("source@example.com")
  .recipient("destination@example.com")
  .subject(u"実例")                 # look Ma, unicode "just works"!
  .body(u"これはテストなんですよ")
  .attachment("chainmail.py")
  .attachment("test.py")
)

smtp = (
  chainmail.SMTP()
  .host("smtp.example.com")
  .port(587)
  .username("USER")
  .password("PASSWORD")
)

print message
print smtp

smtp.send(message)
```

Text Encoding
=============

All text is forcibly encoded as unicode via BeautifulSoup's `UnicodeDammit`
class. If your message is looking garbled, try encoding it unicode before
attaching it.
