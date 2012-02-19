import csv
import os


def read_csv(file_name):
    return [line for line in csv.DictReader(open(file_name, 'r'),
                                            delimiter='\t',
                                            skipinitialspace=True)]


def projects_ini(buildout_directory, projects):
    """
    Produce a projects.ini file:
    
    etc/projects/projects.ini
    
    Like this:
    
    [Test]
    projects = Test,
        [[dbs]]
        RNAseqPipeline = db
        RNAseqPipelineCommon = dbcommon
    """
    path = os.path.join(buildout_directory, 'etc/projects/projects.ini')
    ini = open(path, 'w')
    for project in projects:
        ini.write('[%s]\n' % project)
        ini.write('projects = %s,\n' % project)
        ini.write('    [[dbs]]\n')
        ini.write('    RNAseqPipeline = %s\n' % project)
        ini.write('    RNAseqPipelineCommon = %sCommon\n' % project)
        ini.write('\n')
    ini.close()

def databases_ini(buildout_directory, dbs):
    """
    Produce a databases.ini file:

    etc/databases/databases.ini

    Like this:
    
    [Test]
    connection = raisin
    db = Test_RNAseqPipeline
    description = Contains the meta data
    
    [TestCommon]
    connection = raisin
    db = Test_RNAseqPipelineCommon
    description = Contains all the statistics results
    """
    path = os.path.join(buildout_directory, 'etc/databases/databases.ini')
    ini = open(path, 'w')
    projects = []
    for project_id, db, commondb in dbs:
        if project_id in projects:
            print "Ingnoring project", project_id, db, commondb
            continue
        else:
            projects.append(project_id)
        ini.write('[%s]\n' % project_id)
        ini.write('connection = raisin\n')
        ini.write('db = %s\n' % db)
        ini.write('description = Contains the meta data\n')
        ini.write('\n')
        ini.write('[%sCommon]\n' % project_id)
        ini.write('connection = raisin\n')
        ini.write('db = %s\n' % commondb)
        ini.write('description = Contains all the statistics results\n')
        ini.write('\n')
    ini.close()

def get_profiles(staging):
    profiles = read_csv(os.path.join(staging, 'profiles.csv'))
    return [profile for profile in profiles]


def get_projects(profiles):
    projects = set()
    for profile in profiles:
        projects.add(profile['project_id'])
    return projects


def get_dbs(profiles):
    dbs = set()
    for profile in profiles:
        dbs.add((profile['project_id'], profile['DB'], profile['COMMONDB'],))
    return dbs

def pyramid_projects_ini(buildout_directory, projects, project_users):
    """
    Produce a projects.ini file for pyramid:
    
    etc/pyramid/projects.ini
    
    Like this:
    
    [Test]
    users = "raisin",
    """
    path = os.path.join(buildout_directory, 'etc/pyramid/projects.ini')
    ini = open(path, 'w')
    for project in projects:
        ini.write('[%s]\n' % project)
        user_list = project_users[project]
        ini.write('users = %s\n' % ','.join(user_list))
        ini.write('\n')
    ini.close()

def get_parameters(buildout):
    vocabulary = buildout['parameter_vocabulary']
    categories = buildout['parameter_categories']
    types = buildout['parameter_types']
    columns = buildout['parameter_columns']
    parameters = {}
    for key, value in vocabulary.items():
        parameters[key] = {'title':value,
                           'category':categories[key],
                           'type':types[key],
                           'column':columns[key]
                           }
    return parameters
    
def misc_parameters_ini(buildout_directory, parameters):
    """
    Produce a parameters.ini file:
    
    etc/misc/parameters.ini
    
    Like this:
    
    [partition]
    title = Partition
    type = string
    """
    path = os.path.join(buildout_directory, 'etc/misc/parameters.ini')
    ini = open(path, 'w')
    keys = parameters.keys()
    keys.sort()
    for key in keys:
        parameter = parameters[key]
        ini.write('[%s]\n' % key)
        ini.write('title = %s\n' % parameter['title'])
        ini.write('category = %s\n' % parameter['category'])
        ini.write('type = %s\n' % parameter['type'])
        ini.write('column = %s\n' % parameter['column'])
        ini.write('\n')
    ini.close()

def get_project_users(buildout):
    project_users = {}
    for key, value in buildout['project_users'].items():
        project_users[key] = value.split('\n')
    return project_users

def get_project_parameters(buildout):
    project_parameters = buildout['project_parameters']
    results = {}
    for key, value in project_parameters.items():
        results[key] = value.split("\n")
    return results

def misc_project_parameters_ini(buildout_directory, project_parameters):
    """
    Produce a project_parameters.ini file:
    
    etc/misc/project_parameters.ini
    
    Like this:
    
    [Test]
    parameters = 'read_length',
    """
    path = os.path.join(buildout_directory, 'etc/misc/project_parameters.ini')
    ini = open(path, 'w')
    keys = project_parameters.keys()
    keys.sort()
    for key in keys:
        parameters = project_parameters[key]
        ini.write('[%s]\n' % key)
        value = ['"%s"' % p for p in parameters]
        ini.write('parameters = %s\n' % ', '.join(value))
        ini.write('\n')
    ini.close()


def connections_mysql_ini(buildout_directory):
    """Create the mysql connection file"""
    path = os.path.join(buildout_directory, 'etc/connections')
    if not os.path.exists(path):
            os.makedirs(path)
    path = os.path.join(buildout_directory, 'etc/connections/mysql.ini')
    if not os.path.exists(path):
        ini = open(path, 'w')
        ini.write("[raisin]\n")
        ini.write("port = 3306\n")
        ini.write("server = 127.0.0.1\n")
        ini.write("user = raisin\n")
        ini.write("password = raisin\n")
        ini.close()

def pyramid_development_ini(buildout_directory):
    path = os.path.join(buildout_directory, 'etc/pyramid')
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(buildout_directory, 'etc/pyramid/development.ini')
    if not os.path.exists(path):
        ini = open(path, 'w')
        ini.write("""[app:main]
use = egg:raisin.pyramid

pyramid.reload_templates = true
pyramid.debug_authorization = false
pyramid.debug_notfound = false
pyramid.debug_routematch = false
pyramid.debug_templates = true
pyramid.default_locale_name = en
pyramid.includes = pyramid_debugtoolbar

[server:main]
use = egg:waitress#main
host = 0.0.0.0
port = 7777

# Begin logging configuration

[loggers]
keys = root, raisin

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = INFO
handlers = console

[logger_raisin]
level = DEBUG
handlers =
qualname = raisin

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s

# End logging configuration""")
        ini.close()

def restish_development_ini(buildout_directory):
    path = os.path.join(buildout_directory, 'etc/restish')
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(buildout_directory, 'etc/restish/development.ini')
    if not os.path.exists(path):
        ini = open(path, 'w')
        ini.write("""[DEFAULT]
; Application id used to prefix logs, errors, etc with something unique to this
; instance.
APP_ID = raisin.restish@localhost
; Email settings.
SMTP_SERVER = localhost
ERROR_EMAIL_FROM = %(APP_ID)s
ERROR_EMAIL_TO = %(APP_ID)s

CACHE_DIR = %(here)s/cache

use_pickles_cache = False
use_sql_database = True
pickles_cache_path = %(here)s/../../cache
mysql_connections = %(here)s/../connections/mysql.ini
mysql_databases = %(here)s/../databases/databases.ini
projects = %(here)s/../projects/projects.ini
parameters = %(here)s/../misc/parameters.ini
project_parameters = %(here)s/../misc/project_parameters.ini
sqlite3_database = %(here)s/../../etl/database/database.db

[composite:main]
use = egg:Paste#cascade
app1 = public
app2 = raisin.restish

[app:raisin.restish]
use = config:raisin.restish.ini#raisin.restish

[app:public]
use = egg:Paste#static
document_root = %(here)s/raisin.restish/public

[server:main]
use = egg:Paste#http
host = 127.0.0.1
port = 6464

# Logging configuration
[loggers]
keys = root, raisin.restish

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = DEBUG
handlers = console

[logger_raisin.restish]
level = DEBUG
handlers =
qualname = raisin.restish

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S""")
        ini.close()



def main(buildout, buildout_directory, staging):
    profiles = get_profiles(staging)
    projects = get_projects(profiles)
    projects_ini(buildout_directory, projects)
    dbs = get_dbs(profiles)
    databases_ini(buildout_directory, dbs)
    project_users = get_project_users(buildout)
    pyramid_projects_ini(buildout_directory, projects, project_users)
    parameters = get_parameters(buildout)
    misc_parameters_ini(buildout_directory, parameters)
    project_parameters = get_project_parameters(buildout)
    misc_project_parameters_ini(buildout_directory, project_parameters)
    connections_mysql_ini(buildout_directory)
    pyramid_development_ini(buildout_directory)
    restish_development_init(buildout_directory)
    