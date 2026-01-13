import requests


def purge_urls(urls, server_host):
if not isinstance(urls, (list, tuple)):
urls = [urls]
purge_value = ','.join(urls)
response = requests.request(
'PURGE', server_host,
headers={'X-LiteSpeed-Purge': purge_value}
)
return response.status_code