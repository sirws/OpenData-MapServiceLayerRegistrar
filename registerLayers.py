import json
from arcrest.ags import mapservice
from arcrest.agol import admin

if __name__ == "__main__":
    try:
        #url = "http://sampleserver6.arcgisonline.com/arcgis/rest/services/Water_Network/MapServer"
        url = "{url to map service}"
        fs = mapservice.MapService(url=url)
        for serviceLayer in fs.layers:
            if serviceLayer.type == "Feature Layer":
                print serviceLayer.name
                print serviceLayer.description
                agol = admin.AGOL(username='{AGOL Username}',password='{AGOL Password}')
                itemURL = url + "/" + str(serviceLayer.id)
                inparams = {"url":itemURL}
                
                res = agol.addItem(name=serviceLayer.name,
                             tags="Bellingham, Open Data, Washington",
                             description=serviceLayer.description,
                             snippet=serviceLayer.name,
                             data=None,
                             extent=str(serviceLayer.extent.get('xmin')) + "," + str(serviceLayer.extent.get('ymin')) + "," + str(serviceLayer.extent.get('xmax')) + "," + str(serviceLayer.extent.get('ymax')),
                             item_type="Feature Service",
                             folder="765cc150b552475eb4f2b87808824493",
                             inparams=inparams,
                             typeKeywords=["Data", "Service", "Feature Service", "ArcGIS Server", "Feature Access"]
                            )
            else:
                print serviceLayer.name + " is not a valid type"

        print res
    except ValueError, e:
        print e
