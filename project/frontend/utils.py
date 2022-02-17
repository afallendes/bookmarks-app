import random
import requests
import re
import base64
import html
import imghdr

from project.settings import env


def get_url_request(url):
    """
    Returns a URL request using a simple local randomized user-agent request. If that connection
    fails, due to exceeded requests or a server error, then tries with an external proxy service.
    """

    # 1) Try with simple local request

    user_agents = [
        # Some of the most common user-agents.
        # REF: https://developers.whatismybrowser.com/useragents/explore/operating_system_name/
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'VM280:1 Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'VM280:1 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'VM280:1 Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
        'VM280:1 Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)',
        'VM38:1 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko)',
        'VM38:1 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'VM38:1 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'VM38:1 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
    ]

    headers = {'User-Agent': random.choice(user_agents)}

    r = requests.get(url, headers=headers, allow_redirects=True)

    if r.status_code == 200:
        return r

    
    # 2) Try with proxy service

    proxy_url = env.str('PROXY_URL')
    proxy_apikey = env.str('PROXY_APIKEY')

    r = requests.get(proxy_url, params={"url": url}, headers={"apikey": proxy_apikey})
    
    return r


def get_url_title(url):
    """ Returns captured title from provided HTML source, else returns None. """

    r = get_url_request(url)
    
    if r.status_code == 200:

        pattern = re.compile(r'<title[^\>\<]*>(?P<title>[^\>\<]*)<\/title>', re.IGNORECASE)
        match = pattern.search(r.text)
        
        if match:
            return html.unescape(match.group('title')).strip()
    
    return ''


def get_url_favicon(url):
    """ Returns favicon from provided URL as base64 string. """

    # This uses a Google's 3rd-party service for simplecity.
    r = get_url_request(f'http://www.google.com/s2/favicons?domain={url}&sz=64')

    mime_type = imghdr.what('placeholder', h=r.content)
    if mime_type == 'ico':
        mime_type = 'x-icon'

    if r.status_code == 200:
        # If request is OK then capture filetype as prefix
        return f"data:image/{mime_type};base64,{base64.b64encode(r.content).decode('utf-8')}"
    
    return ''
