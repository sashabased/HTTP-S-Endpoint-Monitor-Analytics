import urllib.parse as prs

url = str(input())

url_validation = prs.urlparse(url)
print(url_validation)
if url_validation.scheme not in ('http', 'https'):
    print('Not valid url!')
else:
    if url_validation.path in ('', '/'):
        response = url.strip('/') 
        print("this is correct url ->", response)
    else:
        print("URL was sended with endpoint")