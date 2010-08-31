"""buttons.py
   drafts preview behavior buttons and handlers for dexterity types"""

import zope.interface
import zope.component
import zope.event
import zope.schema.interfaces
import zope.lifecycleevent

from plone.z3cform.buttonoverrides import ButtonAndHandlerSubscriber

from plone.dexterity.i18n import MessageFactory as _
from plone.dexterity.interfaces import IDexterityFTI

from z3c.form import button

from dexterity.draftspreviewbehavior.interfaces import IDraftPreviewBehavior


class AddPreviewDraftButtonAndHandlerSubscriber(ButtonAndHandlerSubscriber):
    """Add custom 'Preview' button in DefaultAddForm to allow drafts
    to function properly only if the content type supports
    plone.app.drafts.IDraftable
    """
    zope.interface.implements(IDraftPreviewBehavior)

    position = 400

    def __init__(self, form, event):
        super(AddPreviewDraftButtonAndHandlerSubscriber, self).__init__(form, event)
        fti = zope.component.queryUtility(IDexterityFTI, name=form.portal_type)
        if 'dexterity.draftspreviewbehavior.IDraftPreviewBehavior' in fti.behaviors:
            form.buttonsandhandlers[IDraftPreviewBehavior] = self

    @button.buttonAndHandler(_(u'Preview'), name='preview')
    def buttonHandler(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        view = '++draft++%s' % self.portal_type
        redirectURL = "%s/%s" % (self.getContent().absolute_url(), view)
        self.request.response.redirect(redirectURL)

    def updateActions(self):
        self.form.actions["preview"].addClass("standalone")


class EditPreviewDraftButtonAndHandlerSubscriber(ButtonAndHandlerSubscriber):
    """Add custom 'Preview' button in DefaultEditForm to allow drafts
    to function properly only if the content type supports
    plone.app.drafts.IDraftable
    """
    zope.interface.implements(IDraftPreviewBehavior)

    position = 400

    def __init__(self, form, event):
        super(EditPreviewDraftButtonAndHandlerSubscriber, self).__init__(form, event)
        fti = zope.component.queryUtility(IDexterityFTI, name=form.portal_type)
        if 'dexterity.draftspreviewbehavior.IDraftPreviewBehavior' in fti.behaviors:
            form.buttonsandhandlers[IDraftPreviewBehavior] = self

    @button.buttonAndHandler(_(u'Preview'), name='preview')
    def buttonHandler(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        view = '++draft++%s' % self.portal_type
        redirectURL = "%s/%s" % (self.getContent().absolute_url(), view)
        self.request.response.redirect(redirectURL)

    def updateActions(self):
        self.form.actions["preview"].addClass("standalone")
