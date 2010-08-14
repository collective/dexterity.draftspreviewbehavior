import zope.component
from zope.interface import alsoProvides

from Acquisition.interfaces import IAcquirer
from Acquisition import aq_inner

from plone.app.drafts.utils import syncDraft
from plone.app.drafts.utils import getCurrentDraft
 
from plone.dexterity.interfaces import IDexterityContainer, IDexterityItem
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import createContent

from plone.app.drafts.interfaces import IDexterityDraft
from plone.app.dexterity.behaviors.drafts import IDexterityDraftSubmitBehavior
from plone.app.dexterity.behaviors.drafts import IDexterityDraftCancelBehavior

from dexterity.draftspreviewbehavior.interfaces import IDexterityDraftAdding
from dexterity.draftspreviewbehavior.interfaces import IDexterityDraftEditing
from dexterity.draftspreviewbehavior.interfaces import IDexterityDraftContainer
from dexterity.draftspreviewbehavior.interfaces import IDexterityDraftItem
from plone.app.drafts.dexterity import beginDrafting


# NOT YET USED
class DexterityDraftError( Exception ):
    """
    """
    pass


#def getDraftContext(context, request, portal_type, view_name=None):
def getDraftContext(context, request, portal_type, view_name='add'):
    """Returns a dexterity draft object if the behavior IDexterityDraftable is
       set; otherwise will return original context.  If a draft does not already
       exist, one will be created"""
    
    fti = zope.component.queryUtility( IDexterityFTI, name=portal_type )
    if not 'plone.app.drafts.interfaces.IDexterityDraftable' in fti.behaviors:
        return context
        
    context = aq_inner( context ) # New
    beginDrafting( context, request, None )
    
    #request = getattr(context, 'REQUEST', None)
    if request is None:
        return context
    
    draft = getCurrentDraft(request)
    if draft is None:
        # Don't allow a draft to be created if view_name is None
        # It should be 'add' or 'edit'
        if view_name is None:
            return context

        new_context = createDraftContext( context, portal_type, view_name )
        #if new_context is None:
        #    return context
    else:
        #new_context = getattr( draft, 'context', None )
        if hasattr( draft, '_content' ):
            new_context = getattr( draft, '_content', None )
        elif view_name is not None:
            new_context = createDraftContext( context, portal_type, view_name )
        
    if new_context is None:
        return context

    if IAcquirer.providedBy(new_context):
        new_context = new_context.__of__( context )
    
    return new_context

def createDraftContext(context, portal_type, view_name):
    context = aq_inner(context) #NEW
    request = getattr(context, 'REQUEST', None)
    if request is None:
        return None
    
    draft = getCurrentDraft(request, create=True)
    if draft is None:
        return None
    
    new_context = createContent( portal_type )
    
    alsoProvides( new_context, IDexterityDraft )
    alsoProvides( new_context, IDexterityDraftSubmitBehavior )
    alsoProvides( new_context, IDexterityDraftCancelBehavior )
    
    if IDexterityContainer.providedBy( new_context ):
        alsoProvides( new_context, IDexterityDraftContainer )
    elif IDexterityItem.providedBy( new_context ):
        alsoProvides( new_context, IDexterityDraftItem )

    if view_name == 'add':
        alsoProvides( new_context, IDexterityDraftAdding )
    elif view_name == 'edit':
        alsoProvides( new_context, IDexterityDraftEditing )
        
    new_context.id = '++%s_draft++%s' % (view_name, portal_type)
    new_context.__parent__ = aq_inner( context )
    setattr( draft, '_content', new_context )
    
    if IDexterityDraftEditing.providedBy( new_context ):
        # sync the draft up via data from original context
        syncDraft(context, new_context)
    
    return new_context
