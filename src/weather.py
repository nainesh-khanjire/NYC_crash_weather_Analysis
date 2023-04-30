import datetime as dt
import requests
import csv

# Define the start date and today's date
# given this date to match with the NYC vehicle crash dataset

given_date = '2022-03-01'
start_date = dt.datetime.strptime(given_date, '%Y-%m-%d').date()
today = dt.date.today()

# Define the API endpoint URL and query parameters
#url  = 'https://api.weather.com/v1/location/KJFK:9:US/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=e&startDate=20230228&endDate=20230228'
url = 'https://api.weather.com/v1/location/KJFK:9:US/observations/historical.json'
params = {
    'apiKey': 'e1f10a1e78da46f5b10a1e78da96f525',
    'units': 'e'
}


fieldnames = ['date','timestamp','time_of_day','temperature','condition','pressure','dew_point','humidity','visibility_in_miles',
          'wind_chill_temp','wdir_cardinal','wind_gust','wind_speed','maximum_temp','minimum_temp','precipitation_rate','snow_rate']

# Open the CSV file and write the fieldnames to the first row

with open('data/weather_scraping.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Loop over every day from the start date till today
    for date in (start_date + dt.timedelta(n) for n in range((today - start_date).days + 1)):
        
        # Add the current date to the query parameters
        params['startDate'] = date.strftime('%Y%m%d')
        params['endDate'] = date.strftime('%Y%m%d')

        # Send a GET request to the API endpoint
        response = requests.get(url, params=params)

        # If the response is successful, extract the weather data and write it to the CSV file
        if response.status_code == 200:
            data = response.json()
            print(data)
            for obs in data['observations']:
                timestamp = dt.datetime.fromtimestamp(obs['valid_time_gmt'])  #.strftime('%Y-%m-%d %H:%M:%S')
                #timestamp = obs['valid_time_gmt'] # by default it is in unix timestamp format
                # we have rto convert it to human readablle format
                time_of_day = obs['day_ind'] # important feature
                temperature = obs['temp']
                condition = obs['wx_phrase']
                pressure = obs['pressure_desc']
                dew_point = obs['dewPt'] # important feature
                humidity = obs['rh']
                visibility_in_miles = obs['vis'] # important feature
                wind_chill_temp = obs['wc']
                wdir_cardinal = obs['wdir_cardinal']
                wind_gust = obs['gust']
                wind_speed = obs['wspd']
                maximum_temp = obs['max_temp']
                minimum_temp = obs['min_temp']
                precipitation_rate = obs['precip_hrly']
                snow_rate = obs['snow_hrly'] # important feature

                # Write the weather data to the CSV file
                writer.writerow({
                    'date': date.strftime('%Y-%m-%d'), #this will set the date format
                    'timestamp': timestamp.strftime('%H:%M:%S'), # add if you want date with time('%Y-%m-%d )
                    #'timestamp': timestamp, # add the timestamp to the CSV
                    'time_of_day' : time_of_day,
                    'temperature' : temperature,
                    'condition' : condition,
                    'pressure' : pressure,
                    'dew_point' : dew_point, 
                    'humidity' : humidity,
                    'visibility_in_miles' : visibility_in_miles,
                    'wind_chill_temp' : wind_chill_temp,
                    'wdir_cardinal' : wdir_cardinal,
                    'wind_gust' : wind_gust,
                    'wind_speed' : wind_speed,
                    'maximum_temp' : maximum_temp,
                    'minimum_temp' : minimum_temp,
                    'precipitation_rate' : precipitation_rate,
                    'snow_rate' : snow_rate})
                    

    else:
        print(f"Error {response.status_code}: {response.text}")
        print(response.headers)
            # this prints the error message of responsse code is NOT equal to 200
