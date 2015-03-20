import arcpy, arcrest
from arcrest.ags import MapService

if __name__ == "__main__":
    try:
        url = "{your server URL}"
        #url = "http://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer"

        username = "{Your ArcGIS Online Username}"
        password = "{Your ArcGIS Online Password}"
        sh = None
        agol = None
        usercontent = None
        folderId = None
        proxy_port = None
        proxy_url = None
        baseURL = None
        
        fs = MapService(url=url)
        for serviceLayer in fs.layers:
            if serviceLayer.type == "Feature Layer":
                if baseURL is None or baseURL == "":
                    baseURL = "https://www.arcgis.com/sharing/rest"
                sh = arcrest.AGOLTokenSecurityHandler(username='ScottMoorePNW', password='ChangeMeBack')
                agol = arcrest.manageorg.Administration(url=baseURL, securityHandler=sh)
                usercontent = agol.content.usercontent('ScottMoorePNW')
                if isinstance(usercontent, arcrest.manageorg.administration._content.UserContent):
                    pass

                #create an ArcPy Extent Object so we can reproject it to 4326 (lat/long)
                layerExtent = arcpy.Extent(serviceLayer.extent.get('xmin'),serviceLayer.extent.get('ymin'),serviceLayer.extent.get('xmax'),serviceLayer.extent.get('ymax'))
                layerExtent.spatialReference = arcpy.SpatialReference(serviceLayer.extent["spatialReference"]["wkid"])

                #project the extent of the layer to 4326
                layerExtentPrj = layerExtent.projectAs(arcpy.SpatialReference(4326))
                
                itemURL = url + "/" + str(serviceLayer.id)
                itemParams = arcrest.manageorg.ItemParameter()
                itemParams.title = serviceLayer.name
                itemParams.description = serviceLayer.description
                itemParams.snippet = serviceLayer.name
                itemParams.accessInformation = "Creative Commons Attribution License"
                itemParams.type = "Feature Service"
                itemParams.tags = "Open Data, MyAgency"
                itemParams.url = itemURL
                itemParams.typeKeywords = ["Data", "Service", "Feature Service", "ArcGIS Server", "Feature Access"]
                itemParams.extent = str(layerExtentPrj.XMin) + "," + str(layerExtentPrj.YMin) + "," + str(layerExtentPrj.XMax) + "," + str(layerExtentPrj.YMax)
                res = usercontent.addItem(itemParameters=itemParams, overwrite=True, folder=folderId)
            else:
                print serviceLayer.name + " is not a valid type"

        print res
    except ValueError, e:
        print e
