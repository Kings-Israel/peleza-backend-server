import urllib


def build_url(baseurl, path, args_dict={}):
    url_parts = list(urllib.parse.urlparse(baseurl))
    url_parts[2] = path
    url_parts[4] = urllib.parse.urlencode(args_dict)
    return urllib.parse.urlunparse(url_parts)
