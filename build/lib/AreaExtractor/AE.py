import osmnx as ox
import networkx as nx

def TestPackage():
    print("AreaExtractor v-1.0.0")



def MainAlg(osm_type, osm_id):
    
    # 1) load geometry of master
    if(osm_type=="relation" or "Relation" or "r" or "R"): 
        osm_type='relation'
        osmid='R'
    elif(osm_type=="way" or "Way" or "w" or "W"): 
        osm_type='way'
        osmid="W"
    else: 
        osm_type=""
        osmid=""
    osmid = osmid + osm_id
    master_obj, master_geo = LoadData(osmid)
    
    # 2) search areas in master
    list = LoadAreas(master_geo)
    
    # 3) clean list of Arease
    area_list = CleanAreaList(list, osm_type, osm_id, master_geo)

    return master_obj, area_list



# load data of an OSM object and it's geometry
def LoadData(osmid):
    obj = ox.geocoder.geocode_to_gdf([osmid], by_osmid=True)
    geo = obj['geometry'][0]
    return obj, geo
    

# search and load data of areas in given geometry
def LoadAreas(geo):
    tags = {"type": "boundary"} 
    list = ox.features.features_from_polygon(geo, tags)
    list.reset_index(inplace=True)
    return list

# remove incorrect objects from the list
def CleanAreaList(list, master_type, master_id, master_geo):
    n=len(list['id'])
    for i in range(n):
        # remove master object 
        if list['element'][i] == master_type and str(list['id'][i]) == master_id: 
            list = list.drop([i])
        else:  
        # remove incorrect objects (not in master area or master don't contain them)
            g = list['geometry'][i]
            if(not (master_geo.contains(g))):
                list = list.drop([i])
    list.reset_index(inplace=True)
    return list
