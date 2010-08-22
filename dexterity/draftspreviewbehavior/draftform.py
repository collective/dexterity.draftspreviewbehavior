import zope.component

from Acquisition import aq_inner, aq_base
from Acquisition.interfaces import IAcquirer

from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.browser.base import DexterityExtensibleForm
from plone.app.dexterity.behaviors.drafts import addBegun

from z3c.form.form import Form, applyChanges

class DefaultDraftForm(DexterityExtensibleForm, Form):
    """ DefaultDraftForm is used by draft traverser to populate
    the request.form and populate the temporary (not saved in ZODB) content
    object
    """
 
    ignoreContext = True
    ignoreRequest = False
    
    def update(self):
        addBegun( self, None )
        super(DefaultDraftForm, self).update()

    def populateContextFromDraft(self):
        data, errors = self.extractData()
        if errors:
            return None
        
        fti = zope.component.getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        content = zope.component.createObject(fti.factory)
        
        if hasattr(content, '_setPortalTypeName'):
            content._setPortalTypeName(fti.getId())

        # Acquisition wrap temporarily to satisfy things like vocabularies
        # depending on tools
        if IAcquirer.providedBy(content):
            content = content.__of__(container)

        applyChanges(self, content, data)
        for group in self.groups:
            applyChanges(group, content, data)
                    
        return aq_base(content)
