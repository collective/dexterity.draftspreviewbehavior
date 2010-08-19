"""preview.pt
   preview view to pick proper view for previewing drafts
   also provides button handlers to submit/edit/cancel draft"""

import zope.interface
from zope.viewlet.interfaces import IViewlet

from Acquisition import aq_parent, aq_inner

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.dexterity.interfaces import IAddBegunEvent, IEditBegunEvent
from plone.dexterity.i18n import MessageFactory as _
    
from z3c.form.form import Form
from z3c.form import button

class IButtons(zope.interface.Interface):
    save = button.Button(title=_('Save'))
    edit = button.Button(title=_('Edit'))
    cancel = button.Button(title=_('Cancel'))
    
class PreviewViewButtons(Form):
    """The default preview viewlet for Dexterity content.  All it does is
    renders the form buttons and handlers for save/edit/cancel to redirect
    the request to the actual form.  The form handles save/cancel
    """
    
    zope.interface.implements(IViewlet)
    
    buttons = button.Buttons(IButtons)
    
    def __init__(self, context, request, view, manager):
        super( PreviewViewButtons, self ).__init__(context, request)

    render = ViewPageTemplateFile( "templates/buttons.pt" )

    def updateActions(self):
        super( PreviewViewButtons, self ).updateActions()
        self.actions["save"].addClass("context")
        self.actions["edit"].addClass("standalone")
        self.actions["cancel"].addClass("standalone")
        
    def formURL(self):
        content = aq_inner( self.getContent() )
        container = aq_parent( aq_inner( content ) )

        if IAddBegunEvent.providedBy( self.request ):
            view = '++add++%s' % content.portal_type
            url = '%s/%s' % (container.absolute_url_path(), view) 
        elif IEditBegunEvent.providedBy( self.request ):
            view = 'edit' 
            url = '%s/%s' % (container.absolute_url_path(), view) 
        else:
            url = self.request.getURL() # Page would get stuck though
            
        return url