import lxml.html
import urllib.request
import sys
from urllib.error import HTTPError


def identify(html):
    """
    Identify a WordPress version
    """
    # Get meta tags with name attributes with the value of 'generator'
    meta = lxml.html.fromstring(html).xpath(
        '/html/head/meta[@name="generator"]')
    # If the value starts with WordPress, return the value
    for m in meta:
        c = m.attrib['content']
        if c.upper().strip().startswith('WORDPRESS'):
            return c

def enumerate_users(url, start=0, end=30, more=10):
    """ 
    Enumerate WordPress users

    We iterate through the range of numbers based on the start and end
    provided. The more keyword tells us how many more users to look for
    if one has been found.
    """
    # If this is true, we look for more users after going through our range
    do_more = False
    for i in range(start, end):
        try:
            # Create the new URL and get the path in the URL
            u = url + "?author={0}".format(i)
            u_path = urllib.parse.urlsplit(u).path
            # Get the HTTP Response and the path for the returned URL
            resp = urllib.request.urlopen(u)
            r_path = urllib.parse.urlsplit(resp.geturl()).path
            # If the paths don't match, we've been redirected
            if u_path != r_path:
                # Make sure it is a legitimate URL
                if resp.geturl().endswith("/"):
                    yield resp.geturl().split("/")[-2]
        except HTTPError:
            pass

    if do_more:
        for u in enumerate_users(url, start=end, end=end + more):
            yield(u)

def main():
    url = sys.argv[1]
    html = urllib.request.urlopen(url).read().decode('utf-8')
    print(identify(html))

    # If the url doesn't end with /, change it
    if not url.endswith('/'):
        url = url + "/"
    for user in enumerate_users(url):
        print(user)


if __name__ == "__main__":
    main()