"""
Test for raisin.recipe.transformation
"""

import os
import unittest
import shutil
from pkg_resources import get_provider
from raisin.recipe.server.server import get_profiles
from raisin.recipe.server.server import get_projects
from raisin.recipe.server.server import projects_ini
from raisin.recipe.server.server import get_dbs
from raisin.recipe.server.server import databases_ini
from raisin.recipe.server.server import get_project_users
from raisin.recipe.server.server import pyramid_projects_ini
from raisin.recipe.server.server import get_parameters
from raisin.recipe.server.server import misc_parameters_ini
from raisin.recipe.server.server import get_project_parameters
from raisin.recipe.server.server import misc_project_parameters_ini
from raisin.recipe.server.server import connections_mysql_ini
from raisin.recipe.server.server import pyramid_development_ini
from raisin.recipe.server.server import restish_development_ini
from raisin.recipe.server.server import restish_raisin_restish_ini
from raisin.recipe.server.server import pyramid_users_ini
from raisin.recipe.server.server import supervisord_conf

PROVIDER = get_provider('raisin.recipe.server')
SANDBOX = PROVIDER.get_resource_filename("", 'tests/sandbox/')
PATH = os.path.join(SANDBOX, 'buildout')


class RecipeTests(unittest.TestCase):
    """
    Test the main method in database.py
    """

    def setUp(self):  # pylint: disable=C0103
        pass
        
    def test_get_profiles(self):
        """
        Test getting the profiles
        """
        staging = SANDBOX
        self.failUnless(get_profiles(staging) == None)

    def test_get_projects(self):
        """
        Test getting the projects
        """
        profiles = None
        self.failUnless(get_projects(profiles) == None)

    def test_projects_ini(self):
        """
        Test configuring the projects.ini
        """
        buildout_directory = SANDBOX
        projects = None
        self.failUnless(projects_ini(buildout_directory, projects) == None)

    def test_get_dbs(self):
        """
        Test getting the dbs
        """
        profiles = None
        self.failUnless(get_dbs(profiles) == None)
    
    def test_databases_ini(self):
        """
        Test configuring the databases.ini
        """
        buildout_directory = SANDBOX 
        dbs = None
        self.failUnless(databases_ini(buildout_directory, dbs) == None)

    def test_get_project_users(self):
        """
        Test getting the project users
        """
        buildout = None
        self.failUnless(get_project_users(buildout) == None)

    def test_pyramid_projects_ini(self):
        """
        Test configuring the pyramid projects.ini
        """
        buildout_directory = SANDBOX
        projects = None
        project_users = None
        self.failUnless(pyramid_projects_ini(buildout_directory, projects, project_users) == None)
    
    def test_get_parameters(self):
        """
        Test getting the parameters
        """
        buildout = None
        self.failUnless(get_parameters(buildout) == None)
    
    def test_misc_parameters_ini(self):
        """
        Test configuring misc parameters.ini
        """
        buildout = None
        self.failUnless(misc_parameters_ini(buildout_directory, parameters) == None)
    
    def test_get_project_parameters(self):
        """
        Test getting the project parameters
        """
        buildout = None
        self.failUnless(get_project_parameters(buildout) == None)

    def test_misc_project_parameters_ini(self):
        """
        Test configuring the project parameters.ini
        """
        buildout_directory = SANDBOX
        project_parameters = None
        self.failUnless(misc_project_parameters_ini(buildout_directory, project_parameters) == None)
    
    def test_connections_mysql_ini(self):
        """
        Test configuring the connections mysql.ini
        """
        buildout_directory = SANDBOX
        self.failUnless(connections_mysql_ini(buildout_directory) == None)

    def test_pyramid_development_ini(self):
        """
        Test configuring the pyramid development.ini
        """
        buildout_directory = SANDBOX
        self.failUnless(pyramid_development_ini(buildout_directory) == None)
    
    def test_restish_development_ini(self):
        """
        Test configuring the restish development.ini
        """
        buildout_directory = SANDBOX
        self.failUnless(restish_development_ini(buildout_directory) == None)
    
    def test_restish_raisin_restish_ini(self):
        """
        Test configuring the restish raisin.restish.ini
        """
        buildout_directory = SANDBOX
        self.failUnless(restish_raisin_restish_ini(buildout_directory) == None)
    
    def test_pyramid_users_ini(self):
        """
        Test configuring the pyramid users.ini
        """
        buildout_directory = SANDBOX
        self.failUnless(pyramid_users_ini(buildout_directory) == None)
    
    def test_supervisord_conf_development(self):
        """
        Test configuring the supervisord.conf for development
        """
        buildout_directory = SANDBOX
        self.failUnless(supervisord_conf(buildout_directory, "development") == None)

    def test_supervisord_conf_production(self):
        """
        Test configuring the supervisord.conf for production
        """
        buildout_directory = SANDBOX
        self.failUnless(supervisord_conf(buildout_directory, "production") == None)
    
def test_suite():
    """
    Run the test suite
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
