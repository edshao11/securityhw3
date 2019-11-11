import re

comment = '<script>window.open("http://127.0.0.1:1338/csrf_target/secretmessagelol");</script>'
print(comment)
comment = re.sub(r'<[a-z]*>', '', comment, flags=re.IGNORECASE)
print(comment)
