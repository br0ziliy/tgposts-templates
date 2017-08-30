# -*- coding: utf-8 -*-
class Template():

    def __init__(self):
        self.params = {'url': None, 'title': None, 'country': None } # "Country", "Link", "Title"]

    def get_params(self):
        return self.params

    def set_params(self, params):
        self.params = params

    def get_template(self, params):
        url = self.params['url']
        title = self.params['title'].encode('utf-8')
        country = self.params['country'].encode('utf-8')
        link = "<a href='{}'>{}</a>".format(url, title)
        template = "The article about #{}\n\n{}\n".format(country, link)
        return template
