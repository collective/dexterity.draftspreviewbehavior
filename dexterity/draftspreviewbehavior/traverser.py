#  Register the ++draft++ traversal adapter from CMF 2.2
#  Will return the draft object as context so views, etc can be applied to it.

from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts
from zope.traversing.interfaces import ITraversable
from zope.traversing.interfaces import TraversalError

from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName

#from plone.app.drafts.dexterity import getDraftContext
#from dexterity.draftspreviewbehavior.content import getDraftContext
from plone.app.drafts.interfaces import IDraft

from Products.Five.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse, NotFound

from dexterity.draftspreviewbehavior.interfaces import IDraftPreview
from plone.dexterity.i18n import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

class DraftTraverser(object):
    """Draft traverser.
    """
    adapts(IFolderish, Interface)
    implements(ITraversable)

    previewMessage = _(u'This is a preview.  Click "Save" to publish, "Edit" to edit or "Cancel" to cancel and delete')
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignored):       
        import zope.component
        ttool = getToolByName(self.context, 'portal_types')
        ti = ttool.getTypeInfo(name)
        if ti is not None:
            # TODO:  Consider best way to get form; maybe just add ++draft++ to edit/++add++
            #
            # Use addFrom here to help populate object since it will ignoreContext
            # as well as provides an applyChanges method.  AddForm also contains
            # notify hook to populate the request form from draft
            #
            add_view = zope.component.queryMultiAdapter((self.context, self.request, ti),
                                         name=ti.factory)
            if add_view is None:
                add_view = zope.component.queryMultiAdapter((self.context, self.request, ti))
            if add_view is not None:
                add_view.__name__ = ti.factory
            
                form = add_view.form_instance
                
                
                # Reset buttons and handlers since we don't want action
                # buttons to be able to invoke them from here
                #import z3c.form.button
                #form.buttons = z3c.form.button.Buttons()
                #form.handlers = z3c.form.button.Handlers()
            
                #form.ignoreButtons = True
                #form.ignoreHandlers = True
                form.update() #Should automatically get draft data via notify
                
                # Popluate request.form with draft
                #from plone.app.dexterity.behaviors.drafts import draftRequestForm
                #draftRequestForm( form, None )
                
                # update form widgets
                #form.updateWidgets()
                #form.updateActions()
                #form.actions.update()
                
                data, errors = form.extractData()
                if errors:
                    # TODO: Put a message that can't preview; errors on page
                    # BUG: following does not work
                    return add_view.__of__(self.context) 
                
                from plone.dexterity.utils import createContent
                from Acquisition import aq_inner
                from plone.dexterity.interfaces import IAddBegunEvent, IEditBegunEvent
                
##                if IAddBegunEvent.providedBy( self.request ):
##                    notifier = 'add'
##                elif IEditBegunEvent.providedBy( self.request ):
##                    notifier = 'edit'
##                else:
##                    # Don't know what type of form was used to create draft
##                    #
##                    # TODO: Put a message that can't preview; errors on page
##                    # BUG: following does not work
##                    return add_view.__of__(self.context) 
                    
                content = form.create(data)
                #content.id = '++draft%s++%s' % (notifier, form.portal_type)
                content.id = '++draft++%s' % form.portal_type
                content.__parent__ = aq_inner( self.context )
                
                #import z3c.form.form
                #z3c.form.form.applyChanges(form, content, data)
                #for group in form.groups:
                #    z3c.form.form.applyChanges(group, content, data)
    
                #from Acquisition.interfaces import IAcquirer
                #if IAcquirer.providedBy(content):
                #    content = content.__of__(form.context)

                # TODO:  logic should go in here is custom content type
                #        view exists; instead of default; then use view instead
                #        if append ??
                #if len(self.request.path) == 0:
                #    stack = self.request['TraversalRequestNameStack']
                #    stack.append('preview')
                #    self.request._hacked_path = 1
                
                IStatusMessage(self.request).addStatusMessage( self.previewMessage, "info")
                zope.interface.alsoProvides( content, IDraftPreview )
                return content
#
        raise TraversalError(self.context, name)
