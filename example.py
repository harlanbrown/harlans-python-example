from nuxeo.client import Nuxeo
nuxeo = Nuxeo(auth=('Administrator', 'Administrator'))

query = "SELECT * FROM Document WHERE ecm:primaryType = 'File' AND ecm:isTrashed = 0 AND ecm:isVersion = 0"
entries = []
index = 0

while True:
    query_result = nuxeo.documents.query({"query":query, "pageSize":500, "currentPageIndex":index})
    print("resultsCount: ",query_result["resultsCount"])
    listOfEntries = query_result["entries"]
    print("number of entries in this page: ", len(listOfEntries))

    for doc in listOfEntries:
        entries.append(doc.uid)
    print("number of uids appended to entries list: ", len(entries))
    print("number of unique uids in entries list:", len(set(entries)))
    if not query_result['isNextPageAvailable']:
        break

    index += 1

