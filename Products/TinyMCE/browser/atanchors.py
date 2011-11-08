from Products.Five.browser import BrowserView
from Products.TinyMCE.browser.interfaces.anchors import IAnchorView
# Not available in xml.etree
from elementtree import HTMLTreeBuilder
from zope.interface import implements


class ATAnchorView(BrowserView):
    implements(IAnchorView)

    def listAnchorNames(self, fieldname=None):
        """Return a list of Anchor names"""
        results = []
        tree = HTMLTreeBuilder.TreeBuilder()
        if not fieldname:
            field = self.context.getPrimaryField()
        else:
            field = self.context.getField(fieldname)

        htmlsnippet = field.getAccessor(self.context)()
        try:
            tree.feed('<root>%s</root>' % htmlsnippet)
        except AssertionError:
            return results
        rootnode = tree.close()
        for x in rootnode.getiterator():
            if x.tag == "a":
                if "name" in x.keys():
                    results.append(x.attrib['name'])
        return results
