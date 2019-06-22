import yalebuildings
import os

# "api" name can be whatever is most convenient for your program
api = yalebuildings.YaleBuildings(os.environ['YALE_API_KEY'])

for building in api.buildings():
    print(f"{building.id}: {building.name}")
