import pyodata
import requests
from pyodata.v2.service import GetEntitySetFilter
from requests.models import Response


class ServiceBase:
    def __init__(self, sServce_url, sClent):
        if not sClent:
            sClent = "510"

        params = {"sap-client": sClent}
        self._service_url = sServce_url
        self._session = requests.session()
        self._session.params = params
        self._service_instance = pyodata.Client(sServce_url, self._session)

    def getEntitySet(self, sEntityName):
        return self._service_instance.entity_sets._entity_sets[sEntityName]

    def readEntitySet(self, oRequest={}):
        sEntityName = oRequest.get("entityName", "")
        if not sEntityName:
            return
        entity_set_request = self.getEntitySet(sEntityName).get_entities()

        sSelect = oRequest.get("select", "")
        sFilter = oRequest.get("filter", "")

        if sSelect:
            entity_set_request.select(sSelect)

        if sFilter:
            entity_set_request.filter(sFilter)

        entity_set_request.skip(oRequest.get("skip", 0))
        entity_set_request.top(oRequest.get("top", None))
        sCount = oRequest.get("count", None)
        if sCount == "inline":
            entity_set_request.count(inline=True)
        elif sCount:
            entity_set_request.count()

        result = entity_set_request.execute()

        final_result = dict(count=len(result),
                            totalCount=result.total_count, data=[])
        for r in result:
            record = dict(r._cache.items())
            final_result["data"].append(record)

        return final_result

    def readEntity(self, oRequest={}):
        if not oRequest["entityName"]:
            return
        if not oRequest["entityKey"]:
            return

        read_request = self.getEntitySet(
            oRequest["entityName"]).get_entity(oRequest["entityKey"])

        sSelect = oRequest.get("select", "")
        sExpand = oRequest.get("expand", "")
        if sSelect:
            read_request.select(sSelect)
        if sExpand:
            read_request.expand(sExpand)
        oResponse = read_request.execute()
        print(oRequest)

    def createEntity(self, oRequest={}):
        if not oRequest["entityName"]:
            return
        if not oRequest["data"]:
            return

        create_request = self.getEntitySet(
            oRequest["entityName"]).create_entity()
        create_request.set(**oRequest["data"])
        oResponse = create_request.execute()
        print(oResponse)

    def updateEntity(self, oRequest={}):
        pass

    def deleteEntity(self, oRequest={}):
        pass

    def fetchCSRFToken(self):
        sToken = self._session.headers.get("x-csrf-token", "")
        if not sToken:
            oResponse = self._session.head(self._service_url, headers={
                                           'x-csrf-token': 'fetch'})
            sToken = oResponse.headers.get('x-csrf-token', '')
            self._session.headers.update({'x-csrf-token', sToken})
            self._service_instance.http_get()
