import os, random, string
from nuxeo.client import Nuxeo
from nuxeo.models import Document, FileBlob
from nuxeo.exceptions import UploadError
from robohash import Robohash

def randstr(k):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))

def randword(count):
# http://www.regexprn.com/2008/11/read-random-line-in-large-file-in.html
    filename = DICTFILE
    file = open(filename,'r')

#Get the total file size
    file_size = os.stat(filename)[6]

    words = []
    for x in range(count):
#Seek to a place in the file which is a random distance away
#Mod by file size so that it wraps around to the beginning
        file.seek((file.tell()+random.randint(0,file_size-1))%file_size)

#dont use the first readline since it may fall in the middle of a line
        file.readline()
#this will return the next (complete) line from the file
        line = file.readline()

#here is your random line in the file
        word = line.strip()
        words.append(word.replace('\'s',''))
    return ' '.join(words)

def randimg(filename):
    size = 300
    rh = Robohash(filename)
    rh.assemble(roboset='set1', sizex=size, sizey=size)
    with open('/tmp/' + filename, 'wb') as f:
        rh.img.save(f, format=FORMAT)
    return '/tmp/' + filename

def createImageBlob(pathtofile):
    try:
        batch = nuxeo.uploads.batch()
        batch.upload(FileBlob(pathtofile), chunked=True)
        return batch.get(0)
    except UploadError:
        return

def createWorkspaceRoot():
    root = nuxeo.documents.get(path='/default-domain')
    if USEDICT:
        workspaceRootName = randword(2).replace(' ','-')
    else:
        workspaceRootName = randstr(8)
    new_ws = Document(name=workspaceRootName, type='WorkspaceRoot', properties={'dc:title':workspaceRootName}) 
    ws = nuxeo.documents.create(new_ws, parent_path=root.path)
    return ws

def createWorkspace(parentDoc):
    if USEDICT:
        ok = False
        while not ok :
            workspaceName = randword(2).replace(' ','-')
            if len(workspaceName) < 25: # keep workspace names short
                ok = True
    else:
        workspaceName = randstr(8)
    new_ws = Document(name=workspaceName, type='Workspace', properties={'dc:title':workspaceName}) 
    ws = nuxeo.documents.create(new_ws, parent_path=parentDoc.path)
    return ws
    
def createDocument(parentDoc, docname, doctype):
    new_doc = Document(name=docname, type=doctype, properties={'dc:title':docname}) 
    if USEDICT:
        new_doc.properties['dc:description']=randword(3)
    doc = nuxeo.documents.create(new_doc, parent_path=parentDoc.path)
    return doc

nuxeo = Nuxeo(auth=('Administrator', 'Administrator'))
FORMAT = 'png'
USEBLOBS = False
USEDICT = False
DICTFILE = '/usr/share/dict/cracklib-small'

lvl1 = 4 
lvl2 = 4
wstype = 'Workspace'
doctype = 'File'
def main():
    wsr = nuxeo.documents.get(path='/default-domain/workspaces')
    for i in range(lvl1):
        ws = createWorkspace(wsr)
        print(ws.title)

        for j in range(lvl2):
            if USEDICT:
                docname = randword(2).replace(' ','-')
            else:
                docname = randstr(12)
            doc = createDocument(ws, docname, doctype)
            print('    ', j, doc.title)
            if USEBLOBS:
                filename = docname + '.' + FORMAT
                img = randimg(filename)
                uploaded = createImageBlob(img)
                if (uploaded):
                    operation = nuxeo.operations.new('Blob.AttachOnDocument')
                    operation.params = {'document': doc.path}
                    operation.input_obj = uploaded
                    operation.execute()

main()

