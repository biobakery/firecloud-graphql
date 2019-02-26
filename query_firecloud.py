
# Code to query the firecloud api

from firecloud import api

def call_api(url):
    """ Use the firecloud api module to query firecloud """
    result = api.__get(url)
    api._check_response_code(result, 200)
    return result.json()
