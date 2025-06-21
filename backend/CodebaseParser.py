import requests
import os
import base64

#NOTE: it may be worth it in the future to refactor some code such that it is not necessarily to hash each file name to its description. Rather, we just store those in some kind of set and then create the prompt string as we acquire file details 

class CodebaseParser:
    def __init__(self, repositoryOwner, repositoryName):
        '''
        sets variables for this specific parser to make calls to GitHub's API
        '''
        self.token = os.getenv('GITHUB_TOKEN')
        self.owner = repositoryOwner
        self.repo = repositoryName
        self.fileNames = {}
        # this is an ever-evolving list of files we do not care to look at. Huge config type files that are known to blow up the context window. 
        self.doNotProcess = {'__pycache__', '.DS_Store', 'package-lock.json', 'package.json', '.png', '.jpeg', '.jpg', '.mp4', '.svg'}

    def buildRepoFiles(self, subDir):
        # build the base URL. The /contents endpoint lists everything in the project's root directory
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/{subDir}'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(url, headers=headers)

        # check to see if our request was processed
        if( response.status_code != 200 ):
            print(f'Error: Failed to fetch repository contents for /{subDir}, please try again.')
            exit()

        rootContents = response.json()
        for file in rootContents:
            fileName = file['name']
            # check if the file is on the do not process list / has a bad extension 
            if( fileName in self.doNotProcess or (len(fileName) > 3 and (fileName[len(fileName)-4:] in self.doNotProcess or fileName[len(fileName)-5:] in self.doNotProcess) ) ):
                continue
            # if we see a file add it to the global list --> map to empty string for now 
            if( file['type'] == 'file' ):
                self.fileNames[f'{subDir}/{fileName}'] = ''
            # if we see a directory recursively search its contents
            if( file['type'] == 'dir' ):
                self.buildRepoFiles(f'{subDir}/{fileName}')

    def getFileContents(self):
        for fileName in self.fileNames:
            # build the base URL. The /contents endpoint lists everything in the project's root directory
            url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/{fileName}'
            headers = {
                'Authorization': f'Bearer {self.token}'
            }
            response = requests.get(url, headers=headers)

            # check to see if our request was processed
            if( response.status_code != 200 ):
                print(f'Error: Failed to fetch file contents for {fileName}, please try again.')
                exit()

            # the file contents are base-64 encoded
            fileContents = base64.b64decode((response.json())['content'])
            # switch raw contents back to being properly formatted
            fileContents = fileContents.decode('utf-8')
            self.fileNames[fileName] = fileContents

    def formatRepoContents(self):
        codePrompt = ""
        for key in self.fileNames:
            codePrompt += f"file: {key} contains:\n{self.fileNames[key]}\n"
        return codePrompt