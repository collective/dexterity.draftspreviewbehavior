"""buttons.py
   drafts preview behavior buttons and handlers for dexterity types"""

import zope.interface
import zope.component
import zope.event
import zope.schema.interfaces
import zope.lifecycleevent

from plone.z3cform.buttons import ButtonAndHandler

from plone.dexterity.i18n import MessageFactory as _
from plone.dexterity.interfaces import IDexterityFTI

import z3c.form.form
from z3c.form import button, interfaces

from plone.app.drafts.interfaces import IDraft

from dexterity.draftspreviewbehavior.interfaces import IDraftPreviewBehavior

class AddPreviewDraftButtonAndHandler(ButtonAndHandler):
    zope.interface.implements( IDraftPreviewBehavior )
    
    position = 400
    
    def __init__( self, form, event ):
        super(AddPreviewDraftButtonAndHandler,self).__init__(form,event)
        fti = zope.component.queryUtility( IDexterityFTI, name=form.portal_type )
        if 'dexterity.draftspreviewbehavior.IDraftPreviewBehavior' in fti.behaviors:
            form.buttonsandhandlers[ IDraftPreviewBehavior ] = self
 
    @button.buttonAndHandler(_(u'Preview'), name='preview')
    def buttonHandler(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        view = '++draft++%s' % self.portal_type
        redirect_url = "%s/%s" % ( self.getContent().absolute_url(), view )
        self.request.response.redirect( redirect_url ) 

    def updateActions(self):
        self.form.actions["preview"].addClass("standalone")
    
class EditPreviewDraftButtonAndHandler(ButtonAndHandler):
    zope.interface.implements( IDraftPreviewBehavior )
    zope.component.adapts( interfaces.IEditForm,
                           zope.interface.Interface,
                           IDraft)
    
    position = 400
    
    def __init__( self, form, event ):
        super(EditPreviewDraftButtonAndHandler,self).__init__(form,event)
        fti = zope.component.queryUtility( IDexterityFTI, name=form.portal_type )
        if 'dexterity.draftspreviewbehavior.IDraftPreviewBehavior' in fti.behaviors:
            form.buttonsandhandlers[ IDraftPreviewBehavior ] = self
 
    @button.buttonAndHandler(_(u'Preview'), name='preview')
    def buttonHandler(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        view = '++draft++%s' % self.portal_type
        redirect_url = "%s/%s" % ( self.getContent().absolute_url(), view )
        self.request.response.redirect( redirect_url ) 
        
    def updateActions(self):
        self.form.actions["preview"].addClass("standalone")
    