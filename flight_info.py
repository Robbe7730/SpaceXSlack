import datetime
import requests

def get_reused_info(n):
    reused_data = ""

    fsReused = 0
    for idx, core in enumerate(n["rocket"]["first_stage"]["cores"]):
        if(core["reused"]):
            fsReused += 1

    if fsReused == 1:
        reused_data += "a reused first stage"
    elif fsReused > 1:
        reused_data += f"{fsReused} reused first stage-parts"
    return "no reused parts" if reused_data == "" else reused_data

part_name = {
    "core": "core",
    "side_core1": "first side core",
    "side_core2": "second side core",
    "fairings": "fairings ",
    "capsule": "capsule"
}

def get_reuse_attempts(n):
    ret = []
    reuse = n["reuse"]
    for key, value in reuse.items():
        if value:
            key = part_name[key]
            ret.append(f"the {key}")
    return list_to_string(ret, "nothing")

def get_launch_date(n):
    ret = f"{datetime.datetime.fromtimestamp(n['launch_date_unix']):%A %d %b %Y}"
    return ret

def get_launch_time(n):
    ret = f"{datetime.datetime.fromtimestamp(n['launch_date_unix']):%H:%M:%S}"
    return ret

orbits = {
    "LEO": "low earth orbit",
    "HEO": "high earth orbit",
    "PO": "polar orbit",
    "ISS": "the ISS",
    "polar": "polar orbit",
    "GTO": "geostationary transfer orbit"
}

def get_orbit(key):
    if(key in orbits):
        return orbits[key]
    return key

def get_payload_info(n):
    for payload in n["rocket"]["second_stage"]["payloads"]:
        weight = payload['payload_mass_kg']
        weightstr = f"{weight} kg " if weight else ""
        yield f"{payload['payload_id']}: a {weightstr}{payload['payload_type']} from {list_to_string(payload['customers'], 'unkown cusomer')} to {get_orbit(payload['orbit'])}"

def list_to_string(lis, default):
    if len(lis) == 1:
        return lis[0]
    elif len(lis) > 0:
        return " and ".join([", ".join(lis[:-1]), lis[-1]])
    return default

def get_launch(offset=0):
    try:
        r = requests.get(url='https://api.spacexdata.com/v2/launches/upcoming').json()
    except Exception as e:
        yield "An error occured when trying to connect to the api, check the log for details."
        print(e)
        return
    if offset < len(r):
        if offset < 0:
            try:
                r = requests.get(url='https://api.spacexdata.com/v2/launches').json()
            except:
                yield "An error occured when trying to connect to the api, check the log for details."
                print(e)
                return
        n = r[offset]
        yield (f"This flight is a {n['rocket']['rocket_name']} flight with {get_reused_info(n)}.")
        yield (f"This flight, {get_reuse_attempts(n)} will be recovered.")
        yield (f"Launch scheduled on: {get_launch_date(n)} at {get_launch_time(n)}")
        yield (f"Payload:")
        for payloadtxt in get_payload_info(n):
            yield (f" - {payloadtxt}")
        if(n["links"]["video_link"]):
            yield (f"Watch the video here: {n['links']['video_link']}")
    else:
        yield f"Rocket at offset {offset} not found..."

######### TEMP #########
def testflight():
    return ([{"flight_number":58,"launch_year":"2018","launch_date_unix":1522333189,"launch_date_utc":"2018-03-29T14:19:49Z","launch_date_local":"2018-03-29T07:19:49-08:00","rocket":{"rocket_id":"falcon9","rocket_name":"Falcon 9","rocket_type":"FT","first_stage":{"cores":[{"core_serial":"B1041","flight":2,"block":4,"reused":True,"land_success":None,"landing_type":None,"landing_vehicle":None}]},"second_stage":{"payloads":[{"payload_id":"Iridium NEXT 5","reused":False,"customers":["Iridium Communications"],"payload_type":"Satellite","payload_mass_kg":9600,"payload_mass_lbs":21164.38,"orbit":"PO"}]}},"telemetry":{"flight_club":None},"reuse":{"core":True,"side_core1":False,"side_core2":False,"fairings":False,"capsule":False},"launch_site":{"site_id":"vafb_slc_4e","site_name":"VAFB SLC 4E","site_name_long":"Vandenberg Air Force Base Space Launch Complex 4E"},"launch_success":None,"links":{"mission_patch":None,"reddit_campaign":"https://www.reddit.com/r/spacex/comments/82njj5/iridium_next_constellation_mission_5_launch/","reddit_launch":None,"reddit_recovery":None,"reddit_media":None,"presskit":None,"article_link":None,"video_link":None},"details":None}])
