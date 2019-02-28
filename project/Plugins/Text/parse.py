from lxml import html
import requests

def parse():
    try:
        page = requests.get('https://funnysentences.com/sentence-generator/')
        tree = html.fromstring(page.content)
        quote = tree.xpath('//*[@id="sentencegen"]/text()')
        return ''.join(quote)
    except requests.exceptions.ConnectionError:
        return "lol you don't have internet"
