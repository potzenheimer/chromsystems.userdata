import StringIO
import csv
from five import grok
from zope import schema
from plone.directives import form
from z3c.form import button, field
from Acquisition import aq_inner
from plone.namedfile import field as namedfile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.statusmessages.interfaces import IStatusMessage
from chromsystems.userdata import _

class IMemberImport(form.Schema):
    """Member import schema"""
    
    csvfile = namedfile.NamedFile(
        title=_(u"File Upload"),
        description=_(u"Please upload a file in csv format containing the user information to be imported."),
        required=True,
    )
    
class MemberImportForm(form.SchemaForm):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('user-import')
    
    schema = IMemberImport
    ignoreContext = True
    
    label =_(u"Member Import Form")
    description = _(u"Upload existing member information by supplying a csv file.")
    
    def update(self):
        self.request.set('disable_border', True)
        super(MemberImportForm, self).update()
    
    @button.buttonAndHandler(_(u"Import"))
    def handleApply(self, action):
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
        groups_tool = getToolByName(context, 'portal_groups')
        processed_records = 0
        for row in reader:
            uid = self.getSpecificRecord(header, row, name=u'username')
            pwd = self.getSpecificRecord(header, row, name=u'password')
            firstname = self.getSpecificRecord(header, row, name=u'first_name')
            lastname = self.getSpecificRecord(header, row, name=u'last_name')
            fullname = self.getSpecificRecord(header, row, name=u'name')
            email = self.getSpecificRecord(header, row, name=u'email')
            street = self.getSpecificRecord(header, row, name=u'address')
            zipcode = self.getSpecificRecord(header, row, name=u'zip')
            city = self.getSpecificRecord(header, row, name=u'city')
            company = self.getSpecificRecord(header, row, name=u'company')
            customer = self.getSpecificRecord(header, row, name=u'customerid')
            phone = self.getSpecificRecord(header, row, name=u'telephone')
            fax = self.getSpecificRecord(header, row, name=u'fax')
            country = self.getSpecificRecord(header, row, name=u'static_info_country')
            comment = self.getSpecificRecord(header, row, name=u'comments')
            groups = self.getSpecificRecord(header, row, name=u'usergroup')
            gender = self.getSpecificRecord(header, row, name=u'gender')
            if gender == '1':
                salutation = u'Frau'
            else:
                salutation = u'Herr'
            properties = {
                'username'  :   uid.lower(),
                'fullname'  :   fullname.encode('utf-8'),
                'email'     :   email,
                'firstname' :   firstname,
                'lastname'  :   lastname,
                'street'    :   street,
                'zipcode'   :   zipcode,
                'city'      :   city,
                'company'   :   company,
                'comment'   :   comment,
                'salutation':   salutation,
                'groups'    :   groups,
            }
            import pdb; pdb.set_trace( )
            try:
                member = regtool.addMember(uid, pwd, properties=properties)
            except ValueError, e:
                IStatusMessage(self.request).addStatusMessage(_(u"Could not create user:") + unicode(e), "error")
                return None
            if groups:
                groups_tool.addPrincipalToGroup(member.getUserName(), "companies")
            processed_records += 1
        
        return processed_records
    
    def getSpecificRecord(self, header, row, name):
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
    