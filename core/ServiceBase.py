import pyodata
import requests
from pyodata.v2.service import GetEntitySetFilter

class ServiceBase:
    def __init__(self, sServce_url, sClent):
        if not sClent:
            sClent = "510"

        params = {"sap-client": sClent}
        session = requests.session()
        session.params = params
        self.service_instance = pyodata.Client(sServce_url, session)

    def readEntitySet(self, oRequest={}):
        sEntityName = oRequest.get("EntityName", "")
        if not sEntityName:
            return
        entity_set_request = self.service_instance.entity_sets._entity_sets[sEntityName].get_entities()
        
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

        final_result = dict(count=len(result), totalCount=result.total_count, data=[])
        for r in result:
            record = dict(r._cache.items())
            final_result["data"].append(record)

        return final_result

    def readEntity(self, oRequest={}):
        pass
