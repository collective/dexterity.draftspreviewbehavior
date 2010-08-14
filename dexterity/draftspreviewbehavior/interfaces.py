import zope.interface
import zope.schema

from zope.component.interfaces import IObjectEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from plone.dexterity.i18n import MessageFactory as _

from plone.z3cform.interfaces import IButtonAndHandler


"""Custom Behavior Button Marker Interfaces
"""

class IDexterityDraftPreviewBehavior(IButtonAndHandler):
    """Marker interfac to enable custom preview button and handler override
    This is set by an opt-in behavior statement
    """

"""Dexterity preview drafts related interfaces
"""

class IDexterityDraftItem(zope.interface.Interface):
    """
    """

class IDexterityDraftContainer(zope.interface.Interface):
    """
    """

class IDexterityDraftAdding(zope.interface.Interface):
    """
    """
    
class IDexterityDraftEditing(zope.interface.Interface):
    """
    """
    
class IDefaultPreview(zope.interface.Interface):
    """
    """
    
