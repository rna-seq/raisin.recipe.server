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
        ini.write('    RNASeqPipeline = %s\n' % project)
        ini.write('    RNASeqPipelineCommon = %sCommon\n' % project)
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
    for project_id, db, commondb in dbs:
        ini.write('[%s]\n' % project_id)
        ini.write('connection = raisin\n')
        ini.write('db = %s\n' % db)
        ini.write('description = Contains the meta data\n')
        ini.write('\n')
        ini.write('[%sCommon]\n' % project_id)
        ini.write('connection = raisin\n')
        ini.write('db = %s\n' % commondb)
        ini.write('description = Contains all the statistics results\n')
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


def main(buildout_directory, staging):
    profiles = get_profiles(staging)
    projects = get_projects(profiles)
    projects_ini(buildout_directory, projects)
    commondbs = get_dbs(profiles)
    dbs = get_dbs(profiles)
    databases_ini(buildout_directory, dbs)
