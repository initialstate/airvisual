import urllib2
import json
import os
import glob
import time
from ISStreamer.Streamer import Streamer

# --------- User Settings ---------
LATITUDE = "LAT"
LONGITUDE = "LONG"
AIRVISUAL_API_KEY = "AIR VISUAL API KEY"
BUCKET_NAME = "Local Air Quality"
BUCKET_KEY = "aq1"
ACCESS_KEY = "INITIAL STATE ACCES KEY"
MINUTES_BETWEEN_READS = 5
# ---------------------------------

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_current_conditions():
        api_conditions_url = "https://api.airvisual.com/v2/nearest_city?lat=" + LATITUDE + "&lon=" + LONGITUDE + "&key=" + AIRVISUAL_API_KEY
        try:
                f = urllib2.urlopen(api_conditions_url)
        except:
                return []
        json_currently = f.read()
        f.close()
        return json.loads(json_currently)


def main():
        curr_conditions = get_current_conditions()
        if ('data' not in curr_conditions):
                print "Error! AirQual API call failed, check your GPS coordinates and make sure your AirQual API key is valid!\n"
                print curr_conditions
                exit()
        else:
                streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
        while True:

                curr_conditions = get_current_conditions()
                if ('data' not in curr_conditions):
                        print "Error! AirQual API call failed. Skipping a reading then continuing ...\n"
                        print curr_conditions
                else:
                        streamer.log(":house: Location", LATITUDE + "," + LONGITUDE)

                        if 'aqius' in curr_conditions['data']['current']['pollution'] and isFloat(curr_conditions['data']['current']['pollution']['aqius']):
                                streamer.log("AQIUS",curr_conditions['data']['current']['pollution']['aqius'])

                        if 'mainus' in curr_conditions['data']['current']['pollution']:
                                streamer.log("MAINUS",curr_conditions['data']['current']['pollution']['mainus'])

                        streamer.flush()
                time.sleep(60*MINUTES_BETWEEN_READS)

if __name__ == "__main__":
    main()
