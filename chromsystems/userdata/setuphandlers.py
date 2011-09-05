from Products.CMFCore.utils import getToolByName

def setupGroups(portal):
    acl_users = getToolByName(portal, 'acl_users')
    gtool = getToolByName(portal, 'portal_groups')
    if not acl_users.searchGroups(name='Testgroup'):
        gtool.addGroup('Testgroup', roles=['Member'])

def importVarious(context):
    """Miscellanous import steps handler"""
    if context.readDataFile('chromsystems.userdata-various.txt') is None:
        return
    
    portal = context.getSite()
    
    setupGroups(portal)
    