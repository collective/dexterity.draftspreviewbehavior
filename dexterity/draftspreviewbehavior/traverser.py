#  Register the ++draft++ traversal adapter from CMF 2.2
#  Will return the draft object as context so views, etc can be applied to it.

import zope.component
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts
from zope.traversing.interfaces import ITraversable
from zope.traversing.interfaces import TraversalError

from Acquisition import aq_inner

from Products.statusmessages.interfaces import IStatusMessage

from plone.dexterity.i18n import MessageFactory as _

from dexterity.draftspreviewbehavior.interfaces import IDraftPreview
from dexterity.draftspreviewbehavior.draftform import DefaultDraftForm

class DraftTraverser(object):
    """Draft traverser.
    """
    implements(ITraversable)

    previewMessage = _(u'This is a preview.  Click "Save" to publish, "Edit" to edit or "Cancel" to cancel and delete')
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignored):       
        form = DefaultDraftForm( self.context, self.request )
        form.portal_type = name
        form.update() #Should automatically get draft data via notify
        
        content = form.populateContextFromDraft()
        
        if content is None:
            raise TraversalError(self.context, name)
        
        content.id = '++draft++%s' % form.portal_type
        content.__parent__ = aq_inner( self.context )
        
        self.request['disable_border'] = True
        IStatusMessage(self.request).addStatusMessage( self.previewMessage, "info")
        
        zope.interface.alsoProvides( content, IDraftPreview )
        
        return content

        #raise TraversalError(self.context, name)
