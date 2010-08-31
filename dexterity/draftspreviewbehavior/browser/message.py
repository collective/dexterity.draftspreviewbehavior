"""preview.pt
   preview view to pick proper view for previewing drafts
   also provides button handlers to submit/edit/cancel draft"""

import zope.interface
from zope.viewlet.interfaces import IViewlet

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MessageViewlet(BrowserView):
    """The default preview viewlet for Dexterity content.  All it does is
    renders the form buttons and handlers for save/edit/cancel to redirect
    the request to the actual form.  The form handles save/cancel
    """

    zope.interface.implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(MessageViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.view = view
        self.manager = manager

    render = ViewPageTemplateFile("templates/message.pt")
