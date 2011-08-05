from zope.interface import Interface, implements
from zope import schema

from chromsystems.userdata import _
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema

def validateAccept(value):
    if not value == True:
        return False
    return True

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema

class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    salutation = schema.Choice(
        title=_(u'label_salutation', default=u'Salutation'),
        description=_(u'help_salutation',
                      default=u"Are you a girl or a boy?"),
        values = [
            _(u'Miss'), 
            _(u'Mister'),
            ],
        required=True,
        )
    firstname = schema.TextLine(
        title=_(u'label_firstname', default=u'First name'),
        description=_(u'help_firstname',
                      default=u"Fill in your given name."),
        required=False,
        )
    lastname = schema.TextLine(
        title=_(u'label_lastname', default=u'Last name'),
        description=_(u'help_lastname',
                      default=u"Fill in your surname or your family name."),
        required=False,
        )
    customer = schema.TextLine(
        title=_(u'label_customer', default=u'Customer'),
        description=_(u'help_customer', 
            default=u'Please enter your customer identification.'),
        required=False,
        )
    company = schema.TextLine(
        title=_(u'label_company', default=u'Company'),
        description=_(u'help_company', 
            default=u'Please enter your company name.'),
        required=False,
        )
    street = schema.TextLine(
        title=_(u'label_street', default=u'Street'),
        description=_(u'help_street',
                      default=u"Fill in the street you live in."),
        required=False,
        )
    city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        description=_(u'help_city',
                      default=u"Fill in the city you live in."),
        required=False,
        )
    zipcode = schema.TextLine(
        title=_(u'label_zipcode', default=u'Zipcode'),
        description=_(u'help_zipcode',
                      default=u'Please enter your zipcode.')
        )
    country = schema.TextLine(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country',
                      default=u"Fill in the country you live in."),
        required=False,
        )
    phone = schema.TextLine(
        title=_(u'label_phone', default=u'Telephone number'),
        description=_(u'help_phone',
                      default=u"Leave your phone number so we can reach you."),
        required=False,
        )
    fax = schema.TextLine(
        title=_(u'label_fax', default=u'Fax number'),
        description=_(u'help_fax',
                      default=u"Leave your fax number so we can reach you."),
        required=False,
        )
    comments = schema.Text(
        title=_(u'label_comments', default=u'Comments'),
        description=_(u'help_comments',
                      default=u"If you have any comments concerning your registration, please "
                        "leave them here."),
        required=False,
        )
    accept = schema.Bool(
        title=_(u'label_accept', default=u'Accept terms of use'),
        description=_(u'help_accept',
                      default=u"Tick this box to indicate that you have found,"
                      " read and accepted the terms of use for this site. "),
        required=True,
        constraint=validateAccept,
        )

