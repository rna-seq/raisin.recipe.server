# -*- coding: utf-8 -*-
"""Recipe raisin.recipe.server"""

from raisin.recipe.server import server


class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

    def install(self):
        staging = self.buildout['transform']['staging']
        buildout_directory = self.buildout['buildout']['directory']
        server.main(self.buildout, buildout_directory, staging)

    def update(self):
        return self.install()
