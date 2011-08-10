from five import grok
from zope import schema
from plone.directives import form
from z3c.form import button, field
from plone.namedfile import field as namedfile
from Products.CMFCore.interfaces import ISiteRoot
from chromsystems.userdata import _

class IMemberImport(form.Schema):
    """Member import schema"""
    
class MemberImportForm(form.schemaForm):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('member-import-form')
    
    schema = IMemberImport
    ignoreContext = True
    
    label =_(u"Member Import Form")
    description = _(u"Upload existing member information by supplying a csv file.")
    