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

import json


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
	with open(json_file, 'r') as f:
		combined = json.load(f)
	#print(combined)
	
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

if __name__ == '__main__':
	wordBlock2json('C:/Users/shufe/OneDrive/Lego/2021_challenge/FLL_2021_Run3-Felix_v1-0-0.llsp')
	#json2wordBlock('C:/Users/shufe/OneDrive/Lego/Project_word_block.llsp.json')
