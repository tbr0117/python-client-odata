from core.ServiceBase import ServiceBase

service_url = 'http://services.odata.org/V2/Northwind/Northwind.svc/'
service_base = ServiceBase(service_url, '510')
oRequest = {
    "EntityName": "Customers",
    "select": "CustomerID, CompanyName, ContactTitle, Country",
    "filter": "Country eq 'Germany'",
    "count": "inline",
    "top": 20
}
Customers_response = service_base.readEntitySet(oRequest)
# Customer = service_base.readEntity()

for employee in Customers_response.get("data", []):
    if employee:
        print(employee)
