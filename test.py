url = "http://git.com"
endpoint = "me/user"

val_endp = endpoint.strip('/')
print(val_endp)
val_endp = ('/' + val_endp)
print(val_endp)

print(url + val_endp)