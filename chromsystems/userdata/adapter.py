from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """
    def get_salutation(self):
        return self.context.getProperty('salutation', '')
    def set_salutation(self, value):
        return self.context.setMemberProperties({'salutation': value})
    salutation = property(get_salutation, set_salutation)
    
    def get_firstname(self):
        return self.context.getProperty('firstname', '')
    def set_firstname(self, value):
        return self.context.setMemberProperties({'firstname': value})
    firstname = property(get_firstname, set_firstname)

    def get_lastname(self):
        return self.context.getProperty('lastname', '')
    def set_lastname(self, value):
        return self.context.setMemberProperties({'lastname': value})
    lastname = property(get_lastname, set_lastname)

    def get_customer(self):
        return self.context.getProperty('customer', '')
    def set_customer(self, value):
        return self.context.setMemberProperties({'customer': value})
    customer = property(get_customer, set_customer)

    def get_company(self):
        return self.context.getProperty('company', '')
    def set_company(self, value):
        return self.context.setMemberProperties({'company': value})
    company = property(get_company, set_company)

    def get_street(self):
        return self.context.getProperty('street', '')
    def set_street(self, value):
        return self.context.setMemberProperties({'street': value})
    street = property(get_street, set_street)

    def get_city(self):
        return self.context.getProperty('city', '')
    def set_city(self, value):
        return self.context.setMemberProperties({'city': value})
    city = property(get_city, set_city)

    def get_zipcode(self):
        return self.context.getProperty('zipcode', '')
    def set_zipcode(self, value):
        return self.context.setMemberProperties({'zipcode': value})
    zipcode = property(get_zipcode, set_zipcode)

    def get_country(self):
        return self.context.getProperty('country', '')
    def set_country(self, value):
        return self.context.setMemberProperties({'country': value})
    country = property(get_country, set_country)

    def get_phone(self):
        return self.context.getProperty('phone', '')
    def set_phone(self, value):
        return self.context.setMemberProperties({'phone': value})
    phone = property(get_phone, set_phone)

    def get_fax(self):
        return self.context.getProperty('fax', '')
    def set_fax(self, value):
        return self.context.setMemberProperties({'fax': value})
    fax = property(get_fax, set_fax)

    def get_comment(self):
        return self.context.getProperty('comment', '')
    def set_comment(self, value):
        return self.context.setMemberProperties({'comment': value})
    comment = property(get_comment, set_comment)

    def get_accept(self):
        return self.context.getProperty('accept', '')
    def set_accept(self, value):
        return self.context.setMemberProperties({'accept': value})
    accept = property(get_accept, set_accept)


