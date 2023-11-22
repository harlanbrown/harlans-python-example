from nuxeo.client import Nuxeo
nuxeo = Nuxeo(auth=('Administrator', 'Administrator'))

query = "SELECT * FROM Document WHERE ecm:primaryType = 'File' AND ecm:isTrashed = 0 AND ecm:isVersion = 0"
entries = []
index = 0

while True:
    query_result = nuxeo.documents.query({"query":query, "pageSize":500, "currentPageIndex":index});
    listOfEntries = query_result["entries"];

    for doc in listOfEntries:
        entries.append(doc.properties)

    if not query_result['isNextPageAvailable']:
        break

    index += 1
print(entries)

