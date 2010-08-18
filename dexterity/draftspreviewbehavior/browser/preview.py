"""preview.pt
   preview view to pick proper view for previewing drafts
   also provides button handlers to submit/edit/cancel draft"""

import zope.interface

from zope.component import getUtility

from zope.schema.fieldproperty import FieldProperty

from Acquisition import aq_parent, aq_inner

from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.view import WidgetsView

from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.interfaces import IAddBegunEvent, IEditBegunEvent
from plone.dexterity.utils import resolveDottedName
from plone.dexterity.i18n import MessageFactory as _

from z3c.form import button, interfaces

from Products.statusmessages.interfaces import IStatusMessage

from plone.app.drafts.archetypes import discardDraftsOnCancel



#class NotFound(object):
#    """
#    """
    
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.form import Form
from zope.viewlet.interfaces import IViewlet
class PreviewViewButtons(Form):
    """The default preview for Dexterity content. This uses a WidgetsView and
    renders all widgets in display mode.
    """
    
    zope.interface.implements(IViewlet)
    
    def __init__(self, context, request, view, manager):
        super( PreviewViewButtons, self ).__init__(context, request)
        self.template = None

#    render = ViewPageTemplateFile('templates/buttons.pt')
    def render(self):
        # template will contain template for redirect to add / edit form
        if self.template:
            return self.template()
        
##        IStatusMessage(self.request).addStatusMessage( self.previewMessage, "info")
##
##        #
##        # maybe I shoudl do a specific lookup here by interface? (view first)
##        # or figure out how we were called?
##        # Hmm, will still have problem with custom views??
##        #
##        view = zope.component.queryMultiAdapter( (self.context, self.request), name='preview' )
##        if view is not None and not IDefaultPreview.providedBy(view): #Don't want recursion loop
##            # NOTE: preview view should handle its own buttons and actions
##            #       and IDefaultPreview should not be provided.
##            #       the render method SHOULD BE IMPLEMENTED by custom 'preview' view
##            return view()
##        
##        from plone.autoform.interfaces import IWidgetsView
##        view = zope.component.queryMultiAdapter( (self.context, self.request), name='view' )
##        # Bad Hack...  think of other way to do this
##        # Make sure we don't use the default autoplone view here; only want custom ones
##        if view is not None and view.__module__ != 'Products.Five.metaclass': 
##            view.buttons = self.buttons
##            view.actions = self.actions
##            return view()
##        
        # Fallthrough to default 'preview' view
        if getattr(self, 'index', None) is not None:
            return self.index()
        raise NotImplemented("You must implement the 'render' method")
    
    #@property
    #def action(self):
    #    """See interfaces.IInputForm"""
    #    return self.request.getURL()
    
    def update(self):
        #self.portal_type = self.context.portal_type
        self.updateActions()
        self.actions.execute()
        if self.refreshActions:
            self.updateActions()
        
    def updateActions(self):
        self.actions = zope.component.getMultiAdapter(
            (self, self.request, self.getContent()), interfaces.IActions)
        self.actions.update()
        self.actions["save"].addClass("context")
        self.actions["edit"].addClass("standalone")
        self.actions["cancel"].addClass("standalone")
        
    #@property
    #def schema(self):
    #    fti = getUtility(IDexterityFTI, name=self.context.portal_type)
    #    return fti.lookupSchema()
    
    #@property
    #def additionalSchemata(self):
    #    fti = getUtility(IDexterityFTI, name=self.context.portal_type)
    #    for behavior_name in fti.behaviors:
    #        try:
    #            behavior_interface = resolveDottedName(behavior_name)
    #        except ValueError:
    #            continue
    #        if behavior_interface is not None:
    #            behavior_schema = IFormFieldProvider(behavior_interface, None)
    #            if behavior_schema is not None:
    #                yield behavior_schema 

    def setTemplate(self):
        content = aq_inner( self.getContent() )
        container = aq_parent( aq_inner( content ) )

        if IAddBegunEvent.providedBy( self.request ):
            view = '++add++%s' % content.portal_type
            path = '%s/%s' % (container.absolute_url_path(), view) 
            self.template = self.request.traverse( path )
            #self.request.response.redirect(path)
        elif IEditBegunEvent.providedBy( self.request ):
            view = 'edit' 
            path = '%s/%s' % (container.absolute_url_path(), view) 
            self.template = self.request.traverse( path )
            #self.request.response.redirect(path)
        else:
            return
            
##        # Need to provide form data to add/edit form in request
##        for name, widget in self.w.items(): 
##            attr = getattr( content, name, NotFound )
##            if attr is not NotFound:
##                widget_name = widget.name
##                self.template.request.form[widget_name] = attr

    # Buttons
    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        self.setTemplate()
    
    @button.buttonAndHandler(_(u'Edit'), name='edit')
    def handleEdit(self, action):
        content = self.getContent()
        container = aq_parent( aq_inner( content ) )
        if IAddBegunEvent.providedBy( self.request ):
            view = '++add++%s' % content.portal_type
            redirect_url = '%s/%s' % (container.absolute_url(), view)
            self.request.response.redirect( redirect_url )
        elif IEditBegunEvent.providedBy( self.request ):
            view = 'edit'
            redirect_url = '%s/%s' % (container.absolute_url_path(), view)
            self.request.response.redirect( redirect_url )

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        self.setTemplate()
        
 

