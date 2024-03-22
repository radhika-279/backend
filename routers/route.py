# # FastAPI backend
# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class RouteRequest(BaseModel):
#     start_address: str
#     end_address: str

# @app.post("/calculate_route")
# def calculate_route(route_request: RouteRequest):

# ##AIzaSyCrxA-NkFJX8CtxFBlu0ROuEK3aMCJs1Nc##map api

# # Frontend HTML file
# # <!DOCTYPE html>
# # <html>
# # <head>
# #     <title>Route Map</title>
# #     <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCrxA-NkFJX8CtxFBlu0ROuEK3aMCJs1Nc&libraries=places"></script>
# #     <script>
# #         function initMap() {
# #             // Initialize map
# #             var map = new google.maps.Map(document.getElementById('map'), {
# #                 center: {lat: -34.397, lng: 150.644},
# #                 zoom: 8
# #             });

# #             // Draw route on map
# #             // Use Google Maps DirectionsService to calculate route
# #             // Draw polyline on map to represent route
# #         }
# #     </script>
# # </head>
# # <body onload="initMap()">
# # <div id="map" style="height: 400px;"></div>
# # </body>
# # </html>
