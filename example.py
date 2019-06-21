import yalebuildings
import os

# "api" name can be whatever is most convenient for your program
api = yalebuildings.YaleBuildings(os.environ['YALE_API_TOKEN'])

for building in api.buildings():
    print(building['BUILDING'], end=' ')
