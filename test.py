string = 'username=CookieMonster;%20password=TWUgd2FKSE='
password = string.replace('%20', '').split(';')[1][9:]
print(password)