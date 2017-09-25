import urllib.request
import json
import time

def get_related_stocks(code):

    requestUrl = 'https://gw.wmcloud.com/irr/user/getStockKnowledgeGraph?stockId=' + code + '&date=' + time.strftime('%Y%m%d')

    response = urllib.request.urlopen(requestUrl)
    content = response.read().decode(response.headers.get_content_charset())

    ret = []
    for firstChild in json.loads(content)['data']['children']:
        for secondChild in firstChild['children']:
            for thirdChild in secondChild['children']:
                ret.append(thirdChild['info']['businessId'])

    return ret
