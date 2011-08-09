from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.app.users.browser.register import RegistrationForm
from plone.app.users.browser.register import CantChoosePasswordWidget
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.browser.radio import RadioWidget
from chromsystems.userdata import _

class CustomRegistrationForm(RegistrationForm):
    """ Subclass the standard registration form to provide
        custom widgets for our custom form fields.
    """
    
    label = _(u'heading_registration_form', default=u'Registration form')
    description = _(u"Please fill in the registration form details.")
    template = ViewPageTemplateFile('register_form.pt')

    @property
    def showForm(self):
        """The form should not be displayed to the user if the system is
           incapable of sending emails and email validation is switched on
           (users are not allowed to select their own passwords).
        """
        portal = getUtility(ISiteRoot)
        ctrlOverview = getMultiAdapter((portal, self.request), name='overview-controlpanel')

        # hide form iff mailhost_warning == True and validate_email == True
        return not (ctrlOverview.mailhost_warning() and portal.getProperty('validate_email', True))

    @property
    def form_fields(self):
        if not self.showForm:
            # We do not want to spend time calculating fields that
            # will never get displayed.
            return []
        portal = getUtility(ISiteRoot)
        defaultFields = super(CustomRegistrationForm, self).form_fields
        # Can the user actually set his/her own password?
        if portal.getProperty('validate_email', True):
            # No? Remove the password fields.
            defaultFields = defaultFields.omit('password', 'password_ctl')
            # Show a message indicating that a password reset link
            # will be mailed to the user.
            defaultFields['mail_me'].custom_widget = CantChoosePasswordWidget
        else:
            # The portal is not interested in validating emails, and
            # the user is not interested in getting an email with a
            # link to set his password if he can set this password in
            # the current form already.
            defaultFields = defaultFields.omit('mail_me')
        #defaultFields['salutation'].custom_widget = CustomRadioWidget
        return defaultFields

def CustomRadioWidget(self, field, request):
    """Widget for salutation field.
    """
    request = self.request
    widget = RadioWidget(field, request)
    return widget