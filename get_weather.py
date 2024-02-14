import requests,bs4

def get_province(city_input):
    "gets the province of the city"
    city = city_input.capitalize()
    # city = input("fdf: ").capitalize()
    pk_city_webpage = requests.get("https://en.wikipedia.org/wiki/List_of_cities_in_Pakistan_by_population").text
    soup = bs4.BeautifulSoup(pk_city_webpage,"lxml")
    # print(pk_city_webpage)

    city_table = soup.find('table', class_ = "sortable wikitable")
    try:# chhecks for valid city and returns None if true
        city_row = (city_table.find(string=city).parent.parent.parent.parent)
    except AttributeError as e:
        return None
    
    city_links = [link.string for link in  city_row.find_all("a")] # city_links is (city, province) pair
    print(type(city_row))
    if len(city_links) != 2: # checks for inconsistency in html syntax
        city_row = (city_table.find(string=city).parent.parent.parent)# one less parent
        city_links = [link.string for link in  city_row.find_all("a")]
    
    province = city_links[1]
    return province

def get_weather():
    provinces_url_mapping ={ # converts province name into url friendly string
        "Sindh": "sindh",
        "Punjab":"punjab",
        "Balochistan":"balochistan",
        "Khyber Pakhtunkhwa":"north-west-frontier",
        "Azad Kashmir": "azad-kashmir"
    }
    city_input = input("city: ").lower()
    if not get_province(city_input): return None
    province = provinces_url_mapping[get_province(city_input)]
    # get and parse webpage
    url = f'https://www.worldweatheronline.com/{city_input}-weather/{province}/pk.aspx'
    weather_webpage = requests.get(url).text
    soup = bs4.BeautifulSoup(weather_webpage,"lxml")
    #get the statistcs
    weather_summary= soup.find("div", class_ = "weather-summary") # get the weather info container
    # print(weather_summary)
    info_list =[" ".join(info.text.strip().split()) for info in weather_summary.find_all("p")]
    next_10_days = soup.find("p",class_="weather-text").text
    info_list.remove("Phase:")
    return info_list 
    # ['Sunny', '8', 'Feels 6 °c', 'Sunrise: 07:12 AM', 'Moonrise: 10:33 AM', 'Phase:', 'Sunset: 05:19 PM', 'Moonset: 10:59 PM', 'Illum: 26.4']
    #  print(next_10_days)


if __name__ == "__main__":
    print(get_weather())