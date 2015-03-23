### ArcGIS Online Open Data Map Service Layer registration script
Open data people! I wanted to share a script I have used to register all layers in a map services individually to ArcGIS Online for Open Data purposes. The idea being that users may want to create a single ArcGIS Server based open data service with some number of layers in it. For best results, we need to register each layer (i.e. MapServer/1) individually. This could be time consuming. Using this script will save a lot of time. Make sure you fill out your layer description and credits properties. This is a work in progress, but I figured I would share as I have found it useful.

Keep in mind, you will also need to download ArcREST to use this which can be found here: https://github.com/Esri/ArcREST/

registerLayers.py uses ArcREST v1 and registerLayers2.py uses ArcREST v2
