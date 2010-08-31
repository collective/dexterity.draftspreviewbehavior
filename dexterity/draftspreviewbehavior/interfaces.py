import zope.interface
import zope.schema

from plone.z3cform.interfaces import IButtonAndHandlerSubscriber

"""Custom Behavior Button Marker Interfaces
"""

class IDraftPreviewBehavior(IButtonAndHandlerSubscriber):
    """Marker interface to enable custom preview button and handler override
    This is set by an opt-in behavior statement
    """

"""Dexterity preview drafts related interfaces
"""

class IDraftPreview(zope.interface.Interface):
    """Marker interface to indicate draft state content type objects
    """

