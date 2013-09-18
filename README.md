chainmail
=========

`chainmail` is a Python library for constructing and sending email.

Usage
=====

```python
import chainmail

message = (
  chainmail.Message()
  .sender("duckworthd@gmail.com")
  .recipient("dux@premise.com")
  .subject(u"実例")                 # look Ma, unicode "just works"!
  .body(u"これはテストなんですよ")
  .attachment("chainmail.py")
  .attachment("test.py")
)

smtp = (
  chainmail.SMTP()
  .host("smtp.gmail.com")
  .port(587)
  .username("USER")
  .password("PASSWORD")
)

print message
print smtp

smtp.send(message)
```
