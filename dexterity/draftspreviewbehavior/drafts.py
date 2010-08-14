import zope.component

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.dexterity.behaviors.drafts import AddButtonsAndHandlers

from dexterity.draftspreviewbehavior.interfaces import IDraftPreviewBehavior

# TODO
# add import to __init__ so not needing to refer to .interfaces
# 

# Event Handlers
def addBegun(form, event):
    fti = zope.component.queryUtility( IDexterityFTI, name=form.portal_type )
    if not 'plone.app.drafts.interfaces.IDraftable' in fti.behaviors:
        return
    
    # Will provide 'Preview' button
    if 'dexterity.draftspreviewbehavior.IDraftPreviewBehavior' in fti.behaviors:
        zope.interface.alsoProvides( form.request, IDraftPreviewBehavior )
    
    if IDraftPreviewBehavior not in AddButtonsAndHandlers.button_interfaces:
        AddButtonsAndHandlers.button_interfaces.append( IDraftPreviewBehavior )

def editBegun(form, event):
    fti = zope.component.queryUtility( IDexterityFTI, name=form.portal_type )
    if not 'plone.app.drafts.interfaces.IDraftable' in fti.behaviors:
        return

    # Will provide 'Preview' button
    if 'dexterity.draftspreviewbehavior.IDraftPreviewBehavior' in fti.behaviors:
        zope.interface.alsoProvides( form.request, IDraftPreviewBehavior )

    if IDraftPreviewBehavior not in AddButtonsAndHandlers.button_interfaces:
        AddButtonsAndHandlers.button_interfaces.append( IDraftPreviewBehavior )
