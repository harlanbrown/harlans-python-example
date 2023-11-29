import random, string
from nuxeo.client import Nuxeo
from nuxeo.models import Document
nuxeo = Nuxeo(auth=('Administrator', 'Administrator'))


def randstr(k):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))

def createWorkspaceRoot():
    workspaceRootName = randstr(8)
    new_ws = Document(name=workspaceRootName, type='WorkspaceRoot', properties={'dc:title':workspaceRootName}) 
    ws = nuxeo.documents.create(new_ws, parent_path='/default-domain')
    return workspaceRootName

def createWorkspace(workspaceRootName):
    workspaceName = randstr(8)
    new_ws = Document(name=workspaceName, type='Workspace', properties={'dc:title':workspaceName}) 
    ws = nuxeo.documents.create(new_ws, parent_path='/default-domain/'+workspaceRootName)
    return workspaceName
    
def createDocument(workspaceRootName, workspaceName, docname, doctype):
    new_doc = Document(name=docname, type=doctype, properties={'dc:title':docname}) 
    doc = nuxeo.documents.create(new_doc, parent_path='/default-domain/'+workspaceRootName+'/'+workspaceName)
    return doc

lvl1 = 70
lvl2 = 100
wstype = 'Workspace'
doctype = 'File'
def main():
    wsr = 'workspaces'
    for i in range(lvl1):
        ws = createWorkspace(wsr)
        for j in range(lvl2):
            docname = randstr(12)
            doc = createDocument(wsr, ws, docname, doctype)
main()

