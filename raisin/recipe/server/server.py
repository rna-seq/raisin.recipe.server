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
