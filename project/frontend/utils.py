import imp
import random
import requests
import re
import base64
import html


def get_url_request(url):
    """ Returns a URL request with randomized user-agent. """

    # Some of the most common user-agents.
    # REF: https://developers.whatismybrowser.com/useragents/explore/operating_system_name/
    
    user_agents = [
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

    return requests.get(url, headers={'User-Agent': random.choice(user_agents)})


def get_url_title(url):
    """ Returns captured title from provided HTML source, else returns None. """

    r = get_url_request(url)
    
    if r.status_code == 200:

        pattern = re.compile(r'<title\s*.*>(?P<title>\s*.*)<\/title>', re.IGNORECASE)
        match = pattern.search(r.text)
        
        if match:
            return html.unescape(match.group('title'))
    
    return ''


def get_url_favicon(url):
    """ Returns favicon from provided URL as base64 string. """

    # This uses a Google's 3rd-party service for simplecity.
    r = get_url_request(f'http://www.google.com/s2/favicons?domain={url}&sz=64')

    if r.status_code == 200:
        # If request is OK then capture filetype as prefix
        print('>>>', 'content-type', r.headers.get('content-type'))

        print(base64.b64encode(r.content).decode('utf-8'))

        return f"data:image/png;base64,{base64.b64encode(r.content).decode('utf-8')}"
    return ''
