from CodebaseParser import CodebaseParser
from GitAssistant import GitAssistant

ADDINGFILES = 'googleCalendarAssignments'
RECURSION = 'sitev2'

def main():
    parser = CodebaseParser('jhthirteen', RECURSION)
    # calling on an empty string gives us the root of the project
    print('----- Recurisvely Tracking Repository Contents -----')
    parser.buildRepoFiles('')
    print('----- Fetching Content of each File -----')
    parser.getFileContents()
    codePrompt = parser.formatRepoContents()
    assistant = GitAssistant()
    print('----- Analyzing Repository -----')
    assistant.query(codePrompt)

main()