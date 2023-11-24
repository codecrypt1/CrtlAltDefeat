
import googlemaps

a='AIzaSyCOnOQkks'
b='_tDZEubzMLfkTr'
c='a9E1R5oC7-4'
gmaps = googlemaps.Client(key=a+b+c)

def get_popular_places(cords, place_type, place_name='', radius=1500, rankby='prominence'):
    """
    Function to get popular places with their details based on coordinates.

    Args:
        lat (float): Latitude of the location.
        lng (float): Longitude of the location.
        radius (int, optional): Search radius in meters. Defaults to 1500 meters.
        place_type (str, optional): Type of place to search for. Defaults to 'restaurant'.
        rankby (str, optional): Specifies the ranking method. Defaults to 'prominence'.

    Returns:
        list: List of dictionaries containing place details.
    """
    places = gmaps.places_nearby(location=cords, radius=radius, type=place_type, rank_by=rankby)

    places_details = []

    for place in places['results']:
        place_id = place['place_id']
        details = gmaps.place(place_id, fields=['name', 'rating', 'user_ratings_total', 'geometry'])
        distance = gmaps.distance_matrix(origins=cords, destinations=(details['result']['geometry']['location']['lat'], details['result']['geometry']['location']['lng']))['rows'][0]['elements'][0]['distance']['value']
        try:
          place_details = {
              'name': details['result']['name'],
              'rating': details['result']['rating'],
              'user_ratings_total': details['result']['user_ratings_total'],
              'coordinates': details['result']['geometry']['location'],
              'distance': 1 if distance==0 else distance
          }
        except:
          place_details = {
            'name': details['result']['name'],
            'rating': 0.1,
            'user_ratings_total': 0.1,
            'coordinates': details['result']['geometry']['location'],
            'distance': 1 if distance==0 else distance
        }
        places_details.append(place_details)

    # Rank places based on rating and number of reviews
    places_details.sort(key=lambda x: (x['rating'], x['user_ratings_total']), reverse=True)

    return places_details
