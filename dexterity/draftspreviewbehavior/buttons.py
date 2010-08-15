"""buttons.py
   drafts preview behavior buttons and handlers for dexterity types"""

from types import InstanceType

import zope.interface
import zope.event
import zope.component
import zope.schema.interfaces
import zope.lifecycleevent
from zope.schema import getFields

from Acquisition import aq_parent, aq_inner
from ZPublisher.HTTPRequest import FileUpload
from Products.statusmessages.interfaces import IStatusMessage

from plone.z3cform.interfaces import IButtonAndHandler

import z3c.form.form
from z3c.form import button, interfaces
from z3c.form.interfaces import IAddForm

#from plone.z3cform.buttons import ButtonAndHandler, CustomButtonsAndHandlers
from plone.z3cform.buttons import ButtonAndHandler

from plone.namedfile.interfaces import INamedField

from plone.dexterity.i18n import MessageFactory as _
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.interfaces import IDexterityFTI

from plone.app.drafts.interfaces import IDraft, IDraftSyncer
from plone.app.drafts.dexterity import discardDraftsOnCancel
from plone.app.drafts.dexterity import beginDrafting
from plone.app.drafts.utils import getCurrentDraft
 
#from plone.app.dexterity.behaviors.drafts import _applyChanges

from dexterity.draftspreviewbehavior.interfaces import IDraftPreviewBehavior
#from dexterity.draftspreviewbehavior.content import getDraftContext

################################################################################

def _applyChanges( form, content, data ):
    z3c.form.form.applyChanges(form, content, data)
    for group in form.groups:
        z3c.form.form.applyChanges(group, content, data)

################################################################################

class AddPreviewDraftButtonAndHandler(ButtonAndHandler):
    zope.interface.implements( IDraftPreviewBehavior )
    
    def __init__( self, form, event ):
        super(AddPreviewDraftButtonAndHandler,self).__init__(form,event)
        fti = zope.component.queryUtility( IDexterityFTI, name=form.portal_type )
        if 'dexterity.draftspreviewbehavior.IDraftPreviewBehavior' in fti.behaviors:
            form.buttonsandhandlers[ IDraftPreviewBehavior ] = self
 
    @button.buttonAndHandler(_(u'Preview'), name='preview')
    def buttonHandler(self, action):
        
        #content = self.getContent()
        #content = getDraftContext(self.context, self.request, self.portal_type, 'add')
        #_applyChanges(self, content, data)
        
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        view = '++draft++%s' % self.portal_type
        redirect_url = "%s/%s" % ( self.getContent().absolute_url(), view )
        self.request.response.redirect( redirect_url ) 
        
        #view = '%s/@@preview' % content.id
        #redirect_url = "%s/%s" % (aq_parent( aq_inner(content) ).absolute_url(), view)
        # 
        # Store current request URL on draft so preview know how to come back
        #content._returnURL = self.request.getURL()
        #self.request.response.redirect( redirect_url ) 

    def updateActions(self):
        self.form.actions["preview"].addClass("standalone")
    

class EditPreviewDraftButtonAndHandler(ButtonAndHandler):
    zope.interface.implements( IDraftPreviewBehavior )
    zope.component.adapts( interfaces.IEditForm,
                           zope.interface.Interface,
                           IDraft)
    
    def __init__( self, form, event ):
        super(EditPreviewDraftButtonAndHandler,self).__init__(form,event)
        fti = zope.component.queryUtility( IDexterityFTI, name=form.portal_type )
        if 'dexterity.draftspreviewbehavior.IDraftPreviewBehavior' in fti.behaviors:
            #zope.interface.alsoProvides( form.request, IDraftPreviewBehavior )
            form.buttonsandhandlers[ IDraftPreviewBehavior ] = self
 
    @button.buttonAndHandler(_(u'Preview'), name='preview')
    def buttonHandler(self, action):
##        #content = self.getContent()
##        content = getDraftContext(self.context, self.request, self.portal_type, 'edit')
##        data, errors = self.extractData()
##        _applyChanges(self, content, data)
##        
##        if errors:
##            self.status = self.formErrorsMessage
##            return
##
##        view = '%s/@@preview' % content.id
##        redirect_url = "%s/%s" % (aq_parent( aq_inner(content) ).absolute_url(), view)
##        
##        # Store current request URL on draft so preview know how to come back
##        content._returnURL = self.request.getURL()
##        self.request.response.redirect( redirect_url ) 

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        view = '++draft++%s' % self.portal_type
        redirect_url = "%s/%s" % ( self.getContent().absolute_url(), view )
        self.request.response.redirect( redirect_url ) 
        
    def updateActions(self):
        self.form.actions["preview"].addClass("standalone")
    
