import hashlib
a=hashlib.md5("junfenghe".encode("utf-8")).hexdigest()

print(a)