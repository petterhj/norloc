from random import randint

from markdown.extensions.footnotes import FootnoteExtension


class UniqueFootnoteExtension(FootnoteExtension):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unique_prefix = randint(1000, 9999)

    def makeFootnoteId(self, id):
        return 'fn%s%d-%s' % (self.get_separator(), self.unique_prefix, id)

    def makeFootnoteRefId(self, id, found=False):
        return self.unique_ref('fnref%s%d-%s' % (self.get_separator(), self.unique_prefix, id), found)
