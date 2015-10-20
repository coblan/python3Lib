import urllib
text = urllib.urlopen("https://docs.python.org/2/library/ssl.html").read()
print(text)