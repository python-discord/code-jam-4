import requests
from lxml import html

from project import Stack
from project.ClipboardManager.ClipboardObject import TextClipboardObject
from project.Plugins import AbstractPlugin


class QuotePlugin(AbstractPlugin):

    def _get_quote(self):
        """Gets a quote from funnysentences.com API"""
        try:
            page = requests.get('https://funnysentences.com/sentence-generator/')
            tree = html.fromstring(page.content)
            quote = tree.xpath('//*[@id="sentencegen"]/text()')
            return ''.join(quote)
        except requests.exceptions.ConnectionError:
            self._logger.info('Fetching quote from API failed')
            return None

    @staticmethod
    def name() -> str:
        return "Quotes"

    @staticmethod
    def description() -> str:
        return "Adds a random quote to help you sound smarter."

    def onload(self):
        pass

    def unload(self):
        pass

    def on_copy(self, copied_input: any, stack: Stack):
        self._logger.debug(QuotePlugin.name() + " called: " + copied_input)
        # push the actual copied text first, then push the quote later
        stack.push_item(TextClipboardObject(copied_input))
        _quote = self._get_quote()
        if _quote is not None:
            stack.push_item(TextClipboardObject(_quote))

    def on_paste(self, stack: Stack):
        return stack
