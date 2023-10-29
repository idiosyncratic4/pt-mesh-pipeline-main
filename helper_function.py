import requests

def extract_jsessionid(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.9999.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    set_cookie_header = response.headers.get('Set-Cookie', '')
    cookie_parts = set_cookie_header.split(';')
    jsessionid = [part for part in cookie_parts if part.startswith('JSESSIONID=')]

    if jsessionid:
        jsessionid = jsessionid[0].split('=')[1]
    else:
        jsessionid = None
    
    return jsessionid