"""preview.pt
   preview view to pick proper view for previewing drafts
   also provides button handlers to submit/edit/cancel draft"""

import zope.interface
from zope.viewlet.interfaces import IViewlet

from Acquisition import aq_parent, aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#from plone.dexterity.interfaces import IAddBegunEvent, IEditBegunEvent


class PreviewViewButtons(BrowserView):
    """The default preview viewlet for Dexterity content.  All it does is
    renders the form buttons and handlers for save/edit/cancel to redirect
    the request to the actual form.  The form handles save/cancel
    """

    zope.interface.implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(PreviewViewButtons, self).__init__(context, request)
        self.__parent__ = view
        self.view = view
        self.manager = manager

    render = ViewPageTemplateFile("templates/buttons.pt")

    def formURL(self):
        """Return the URL of the original add/edit form
        """
        content = aq_inner(self.context)
        container = aq_parent(aq_inner(content))

        formType = self.request['DRAFT']._form_type
        if formType == 'add':
            view = '++add++%s' % content.portal_type
            url = '%s/%s' % (container.absolute_url_path(), view)
        elif formType == 'edit':
            view = 'edit'
            url = '%s/%s' % (container.absolute_url_path(), view)
        else:
            url = self.request.getURL()  # Page would get stuck though

        return url
