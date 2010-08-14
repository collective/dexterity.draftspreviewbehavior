# Forward compatibility with CMF 2.2.
# XXX: Should be removed when Plone moves to CMF 2.2

################################################################################
#   1. Register the ++draft++ traversal adapter from CMF 2.2
#      Will return the draft object as context so views, etc can be applied to
#      it.
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts
from zope.traversing.interfaces import ITraversable

from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName

#from plone.app.drafts.dexterity import getDraftContext
from dexterity.draftspreviewbehavior.content import getDraftContext
from plone.app.drafts.interfaces import IDexterityDraft

from Products.Five.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse, NotFound

class PreviewTraverserOLD(BrowserView):
    """Preview for dexterity DefaultAddForm and DefaultEditForm
    """
    implements(IPublishTraverse)
    
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        
    def publishTraverse(self, request, name):
        pass
    
    def __call__(self):
        #ttool = getToolByName(self.context, 'portal_types')
        #ti = ttool.getTypeInfo(name)
        #if ti is not None:

        form = self.context.form_instance
        
        # Get draft 
        #from plone.app.dexterity.behaviors.drafts import draftRequestForm
        #draftRequestForm( form, None)
        
        form.update() #Should automatically get draft data via notify
        data, errors = form.extractData()
        if errors:
            return NotFound
        
        from plone.dexterity.utils import createContent
        object = createContent( form.portal_type )
        object.id = 'draft'
        #def _applyChanges( form, content, data ):
        
        import z3c.form.form
        z3c.form.form.applyChanges(form, object, data)
        for group in form.groups:
            z3c.form.form.applyChanges(group, object, data)
 
        object = object.__of__(self.context)
        import zope.component
        preview = zope.component.queryMultiAdapter( (object, self.request), name='preview' )
        #if preview is not None and not IDefaultPreview.providedBy(view): #Don't want recursion loop
            #preview.buttons = self.buttons
            #preview.actions = self.actions
            #return preview()

        if preview is not None:
            return preview()
        else:
            return NotFound
        
##        if preview is not None:
##            preview.ignoreContext = True
##            preview.ignoreRequest = False
##        
##            # Get draft 
##            from plone.app.dexterity.behaviors.drafts import draftRequestForm
##            draftRequestForm( form, None)
##            
##            #return preview.__of__(self.context)
##            return preview()

        #raise TraversalError(self.context, name)
        
class PreviewTraverser(object):
    """Preview for dexterity DefaultAddForm and DefaultEditForm
    """
    adapts(IFolderish, Interface)
    implements(ITraversable)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def traverse(self, name, ignored):       
        #ttool = getToolByName(self.context, 'portal_types')
        #ti = ttool.getTypeInfo(name)

        form = self.context.form_instance
        
        # Get draft 
        #from plone.app.dexterity.behaviors.drafts import draftRequestForm
        #draftRequestForm( form, None)
        
        form.update() #Should automatically get draft data via notify
        data, errors = form.extractData()
        if errors:
            return NotFound
        
        from plone.dexterity.utils import createContent
        object = createContent( form.portal_type )
        object.id = 'draft'
        #def _applyChanges( form, content, data ):
        
        import z3c.form.form
        z3c.form.form.applyChanges(form, object, data)
        for group in form.groups:
            z3c.form.form.applyChanges(group, object, data)
 
        object = object.__of__(self.context)
        import zope.component
        preview = zope.component.queryMultiAdapter( (object, self.request), name='preview' )
        #if preview is not None and not IDefaultPreview.providedBy(view): #Don't want recursion loop
            #preview.buttons = self.buttons
            #preview.actions = self.actions
            #return preview()

        if preview is not None:
            return preview()
        else:
            return NotFound
        
##        if preview is not None:
##            preview.ignoreContext = True
##            preview.ignoreRequest = False
##        
##            # Get draft 
##            from plone.app.dexterity.behaviors.drafts import draftRequestForm
##            draftRequestForm( form, None)
##            
##            #return preview.__of__(self.context)
##            return preview()

        #raise TraversalError(self.context, name)
    
class DraftTraverser(object):
    """Draft traverser.
    """
    adapts(IFolderish, Interface)
    implements(ITraversable)

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
            
                form.update() #Should automatically get draft data via notify
                data, errors = form.extractData()
                if errors:
                    # TODO: Put a message that can't preview; errors on page
                    # BUG: following does not work
                    return add_view.__of__(self.context) 
                
                from plone.dexterity.utils import createContent
                from Acquisition import aq_inner
                #content = createContent( form.portal_type )
                content = form.create(data)
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
                if len(self.request.path) == 0:
                    stack = self.request['TraversalRequestNameStack']
                    stack.append('preview')
                    self.request._hacked_path = 1
                return content
#
        raise TraversalError(self.context, name)

##class DraftTraverser(object):
##    """Draft traverser.
##    """
##    adapts(IFolderish, Interface)
##    implements(ITraversable)
##
##    def __init__(self, context, request):
##        self.context = context
##        self.request = request
##
##    def traverse(self, name, ignored):       
##        ttool = getToolByName(self.context, 'portal_types')
##        ti = ttool.getTypeInfo(name)
##        if ti is not None:
##            draft = getDraftContext(self.context, self.request, ti.factory)
##            
##            if draft is not None:
##                if IDexterityDraft.providedBy( draft ):
##                    self.context = draft
##                    
##                    if len(self.request.path) == 0:
##                        stack = self.request['TraversalRequestNameStack']
##                        stack.append('preview')
##                        self.request._hacked_path = 1
##                        
##                return self.context
##   
##        raise TraversalError(self.context, name)
