import StringIO
import csv
from five import grok
from zope import schema
from plone.directives import form
from z3c.form import button, field
from Acquisition import aq_inner
from plone.namedfile.field import NamedFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from chromsystems.userdata import _

class IMemberImport(form.Schema):
    """Member import schema"""
    
    csvfile = NamedFile(
        title=_(u"File Upload"),
        description=_(u"Please uplaod a file in csv format containing the user information to be imported."),
        required=True,
    )
    
class MemberImportForm(form.SchemaForm):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('member-import-form')
    
    schema = IMemberImport
    ignoreContext = True
    
    label =_(u"Member Import Form")
    description = _(u"Upload existing member information by supplying a csv file.")
    
    @button.buttonAndHandler(_(u"Import Users"))
    def handleImportUsers(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        
        # Process uplaoded file and import member records
        userdata = data['csvfile'].data
        member_records = self.processMemberRecordsFile(userdata)
        if member_records is not None:
            IStatusMessage(self.request).addStatusMessage(_(u"Imported member records: ") + unicode(member_records), "info")
    
    def processMemberRecordsFile(self, data):
        """ Process the uploaded file and import member records
        """
        context = aq_inner(self.context)
        io = StringIO.StringIO(data)
        reader = csv.reader(io, delimiter=';', dialect="excel", quotechar='"')
        header = reader.next()
        regtool = getToolByName(context, 'portal_registration')
        processed_records = 0
        for row in reader:
            uid = self.getSpecificRecord(header, row, name='username')
            pwd = self.getSpecificRecord(header, row, name='password')
            firstname = self.getSpecificRecord(header, row, name='firstname')
            lastname = self.getSpecificRecord(header, row, name='lastname')
            fullname = ' '.join(firstname, lastname)
            email = self.getSpecificRecord(header, row, name='email')
            properties = {
                'username'  :   uid,
                'fullname'  :   fullname.encode('utf-8'),
                'email'     :   email
            }
            try:
                member = regtool.addMember(uid, pwd, properties=properties)
            except ValueError, e:
                IStatusMessage(self.request).addStatusMessage(_(u"Culd not create user:") + unicode(e), "error")
                return None
            processed_records += 1
        
        return processed_records
    
    def getSpecificRecord(header, row, name):
        """ Process a specific record in the import file accessing
            a specific cell by its name
        """
        assert type(name) == unicode
        index = None
        for i in range(0, len(header)):
            if header[i].decode("utf-8") == name:
                index = i
        if index is None:
            raise RuntimeError("Uploaded file does not have the column:" + name)
        
        return row[index].decode("utf-8")
    