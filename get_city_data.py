
""" 
Get monitor type data from openaq API for cities.
Output a csv file that can be used in google sheets.
"""

import csv, math
import requests


# get list of cities from file
with open('cities.txt') as f:
    cities = f.read().splitlines()

# create file to write results to
with open("city_airquality_monitor_types.csv",mode="w") as f: 
    
    fieldnames = ['country', 'city', 'monitor_type'] 
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()

    for city in cities:
        print(city)
        city.replace(" ", "%20") # format city names use in url

        # Determine how many monitor records there are for a given city 
        r = requests.get(f'https://api.openaq.org/v1/locations?city={city}')
        data = r.json()
        matching_records = data['meta']['found']
        total_pages = math.ceil(matching_records / 100) # API is paginated with 100 records per request/page
        print(total_pages)

        if total_pages == 0: # no records, move on
            continue 
        
        # Get all pages
        for page in range(1,total_pages + 1):
            r = requests.get(f'https://api.openaq.org/v1/locations?city={city}&page={page}')
            data = r.json()
            records = data['results']

            # Write results to file
            for record in records:
                writer.writerow({'country':record['country'],
                                 'city':record['city'],
                                 'monitor_type':", ".join(record['parameters'])})