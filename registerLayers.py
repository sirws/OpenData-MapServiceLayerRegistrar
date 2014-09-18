import json, arcpy
from arcrest.ags import mapservice
from arcrest.ags import geometryservice
from arcrest.agol import admin

if __name__ == "__main__":
    try:
        #url = "http://sampleserver6.arcgisonline.com/arcgis/rest/services/Water_Network/MapServer"
        url = "{your server URL}"
        fs = mapservice.MapService(url=url)
        for serviceLayer in fs.layers:
            if serviceLayer.type == "Feature Layer":
                print serviceLayer.name
                print serviceLayer.description
                agol = admin.AGOL(username='{AGOL Username}',password='{AGOL Password}')
                itemURL = url + "/" + str(serviceLayer.id)
                inparams = {"url":itemURL}

                #in the future, I would like to support reprojecting the data using the geometry service instead of arcpy
                #gs = geometryservice.GeometryService(url="http://utility.arcgisonline.com/arcgis/rest/services/Geometry/GeometryServer")

                #create an ArcPy Extent Object so we can reproject it to 4326 (lat/long)
                layerExtent = arcpy.Extent(serviceLayer.extent.get('xmin'),serviceLayer.extent.get('ymin'),serviceLayer.extent.get('xmax'),serviceLayer.extent.get('ymax'))
                layerExtent.spatialReference = arcpy.SpatialReference(serviceLayer.extent["spatialReference"]["wkid"])

                #project the extent of the layer to 4326
                layerExtentPrj = layerExtent.projectAs(arcpy.SpatialReference(4326))

                res = agol.addItem(name=serviceLayer.name,
                             tags="Open Data, MyAgency",
                             description=serviceLayer.description,
                             snippet=serviceLayer.name,
                             data=None,
                             extent=str(layerExtentPrj.XMin) + "," + str(layerExtentPrj.YMin) + "," + str(layerExtentPrj.XMax) + "," + str(layerExtentPrj.YMax),
                             item_type="Feature Service",
                             #folder="765cc150b552475eb4f2b87808824493",
                             folder=None,
                             inparams=inparams,
                             typeKeywords=["Data", "Service", "Feature Service", "ArcGIS Server", "Feature Access"]
                            )
            else:
                print serviceLayer.name + " is not a valid type"

        print res
    except ValueError, e:
        print e
