'''
Structure of Lego Spike Prime project file

Word block project (scratch-like)

The project file is a zip and it contains (at least) three files:
    icon.svg - the scratch blocks image
    manifest.json - some high level information
    scratch.sb3 - a scratch project

    scratch.sb3 contains a few files itself as zip:
        project.json - the real program
        long_name_blalala.svg
        long_name_balal.wav

I am looking into expand them into one text for git

'''


from zipfile import ZipFile
import pprint

pp = pprint.PrettyPrinter(indent=4)

import json, os
from datetime import datetime

def wordBlock2json(project_file, outfile=None):
    with ZipFile(project_file, 'r') as project:
        with project.open('manifest.json') as f:
            manifest = json.load(f)
            #pp.pprint(manifest)

        with project.open('scratch.sb3') as scratchStream:
            with ZipFile(scratchStream)  as scratchZip:
                with scratchZip.open('project.json') as f:
                    scratch = json.load(f)
                    #pp.pprint(scratch)
    
    combined = {'manifiest': manifest, 'scratch': scratch}
    #pp.pprint(combined)
    if outfile is None:
        outfile = project_file + '.json'
    with open(outfile, 'w') as f:
        json.dump(combined, f, indent=4, sort_keys=True)

def json2wordBlock(json_file, outfile=None):
    '''
    This is reverse engineering and has not fully tested yet
    '''
    with open(json_file, 'r') as f:
        combined = json.load(f)
    
    if outfile is None:
        outfile = json_file + '.llsp'

    with ZipFile(outfile, 'w') as project:        
        manifiest = json.dumps(combined['manifiest'])
        project.writestr('manifest.json', manifiest)
        project.writestr('icon.svg', '')

        with project.open('scratch.sb3', 'w') as scratchStream:
            with ZipFile(scratchStream, 'w')  as scratchZip:
                scratch = json.dumps(combined['scratch'])
                scratchZip.writestr('project.json', scratch)


'''
Structure of Lego Spike Prime project file

Python project

The project file is a zip and it contains (at least) three files:
    icon.svg - just a icon
    manifest.json - some high level information
    projectbody.json - json of python codes

I am looking into expand them into one text for git

'''

def project2python(project_file, outfile=None):
    '''
    parse an Spike Python Project file (.llsp) and extract the python script into a file
    the python file can be edited using any editor
    '''
    with ZipFile(project_file, 'r') as project:
        with project.open('manifest.json') as f:
            manifest = json.load(f)
            if manifest['type'] != 'python':
                raise Exception('unexpect project type: {}'.format(manifest['type']))

        with project.open('projectbody.json') as f:
            python = json.load(f)
    
    if outfile is None:
        outfile = project_file + '.py'
    with open(outfile, 'w') as f:
        f.write(python['main'])


def python2project(pythonFile, project_file):
    '''
    take a python source file (.py), convert it into an Spike Prime python project
    '''
    with open(pythonFile, 'r') as f:
        python = f.read()

    projectbody = json.dumps({'main': python})
    name = os.path.basename(project_file).split('.')[0]
    manifest = create_python_manifest(name)
    with ZipFile(project_file, 'w') as project:
        project.writestr('manifest.json', manifest)
        project.writestr('icon.svg', get_svg())
        project.writestr('projectbody.json', projectbody)


def create_python_manifest(name):
    ''' create an generate manifest file for Spike Prime python project '''
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    manifest = {'autoDelete': False,
    'created': now_str,
    'lastsaved': now_str,
    'name': name,
    'size': 1142, # how to calculate this?
    'id': '8-TolOujzJr0', # 12 length string

    'extraFiles': [],
    'hardware': {'python': {'type': 'flipper'}},
    'slotIndex': 0,
    'state': {'canvasDrawerTab': 'knowledgeBaseTab'},
    'type': 'python',
    'workspaceX': 120,
    'workspaceY': 120,
    'zoomLevel': 0.5}

    return json.dumps(manifest)


def get_svg():
    ''' return svg string to be used in Spike Prime Python project'''
    icon_svg='''<svg width="60" height="60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd">\
<g fill="#D8D8D8" fill-rule="nonzero">\
<path d="M34.613 7.325H15.79a3.775 3.775 0 00-3.776 3.776v37.575a3.775 3.775 0 003.776 3.776h28.274a3.775 3.775 0 003.776-3.776V20.714a.8.8 0 00-.231-.561L35.183 7.563a.8.8 0 00-.57-.238zm-.334 1.6l11.96 12.118v27.633a2.175 2.175 0 01-2.176 2.176H15.789a2.175 2.175 0 01-2.176-2.176V11.1c0-1.202.973-2.176 2.176-2.176h18.49z"/>\
<path d="M35.413 8.214v11.7h11.7v1.6h-13.3v-13.3z"/></g>\
<path fill="#0290F5" d="M23.291 27h13.5v2.744h-13.5z"/>\
<path fill="#D8D8D8" d="M38.428 27h4.32v2.744h-4.32zM17 27h2.7v2.7H17zM17 31.86h2.7v2.744H17zM28.151 31.861h11.34v2.7h-11.34zM17 36.72h2.7v2.7H17zM34.665 36.723h8.1v2.7h-8.1z"/>\
<path fill="#0290F5" d="M28.168 36.723h4.86v2.7h-4.86z"/></g></svg>'''
    return icon_svg



if __name__ == '__main__':
    project2python('C:/Users/shufe/OneDrive/Lego/codes/new_python_code.llsp')
    python2project('C:/Users/shufe/OneDrive/Lego/codes/new_python_code.llsp.py', 'C:/Users/shufe/OneDrive/Lego/codes/test.llsp')


