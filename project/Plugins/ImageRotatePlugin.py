# from PyQt5.QtGui import QPixmap
#
# from project import Stack
# from project.ClipboardManager.ClipboardObject import TextClipboardObject
# from project.Plugins import AbstractPlugin
#
#
# def _rotate_pixmap(pixmap: QPixmap):
#
#
# class ImageRotatePlugin(AbstractPlugin):
#
#     @staticmethod
#     def name() -> str:
#         return "SpellingMistakes"
#
#     @staticmethod
#     def description() -> str:
#         return "To help you sound more natural when writing."
#
#     def onload(self):
#         pass
#
#     def unload(self):
#         pass
#
#     def on_copy(self, copied_input: any, stack: Stack):
#         self._logger.debug(ImageRotatePlugin.name() + " called: " + copied_input)
#         # push the actual copied text first, then push the quote later
#         stack.push_item(TextClipboardObject(copied_input))
#         _quote = self._get_quote()
#         if _quote is not None:
#             stack.push_item(TextClipboardObject(_quote))
#
#     def on_paste(self, stack: Stack):
#         return stack
