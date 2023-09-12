from nuxeo.client import Nuxeo
nuxeo = Nuxeo(auth=('Administrator', 'Administrator'))

events = nuxeo.operations.new('Audit.QueryWithPageProvider')
events.params = {
        'providerName': 'EVENTS_VIEW',
        'namedQueryParams':{
                'principalName':'',
                'startDate':'2023-09-10T05:00:00.000Z',
                'endDate':'2023-09-14T05:00:00.000Z'}
}
results = events.execute()
print(results)

