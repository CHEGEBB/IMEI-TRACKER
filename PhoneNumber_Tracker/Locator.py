import phonenumbers
from phonenumbers import geocoder as phonenumbers_geocoder
from phonenumbers import carrier
from opencage.geocoder import OpenCageGeocode
import folium
import math

# Replace with your OpenCage API key
key = "8c3d04ff9f4a410b8ba3d6e8aa9408f7"

def get_location(lat, lng, api_key):
    geocoder = OpenCageGeocode(api_key)
    query = f"{lat},{lng}"
    result = geocoder.reverse_geocode(lat, lng)
    if result and len(result):
        return result[0]['formatted']
    else:
        return None

def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371.0  # radius of the Earth in km

    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)

    dlng = lng2_rad - lng1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # distance in km
    return distance

def main():
    number = input("Please enter your phone number: ")
    new_number = phonenumbers.parse(number)
    location = phonenumbers_geocoder.description_for_number(new_number, "en")
    print(f"Location based on phone number: {location}")

    service_name = carrier.name_for_number(new_number, "en")
    print(f"Service provider: {service_name}")

    # Use OpenCage to geocode the location from the phone number
    geocoder_client = OpenCageGeocode(key)
    query = str(location)
    result = geocoder_client.geocode(query)

    if result and len(result):
        target_lat = result[0]['geometry']['lat']
        target_lng = result[0]['geometry']['lng']
        print(f"Target coordinates: {target_lat}, {target_lng}")

        # Get user's current location (latitude and longitude)
        user_lat = float(input("Enter your current latitude: "))
        user_lng = float(input("Enter your current longitude: "))

        # Calculate distance between user and target location
        distance = calculate_distance(user_lat, user_lng, target_lat, target_lng)
        print(f"Distance to target location: {distance:.2f} km")

        # Get the address of the user's location
        user_location = get_location(user_lat, user_lng, key)
        print(f"Your current location: {user_location}")

        # Display on map
        my_map = folium.Map(location=[user_lat, user_lng], zoom_start=9)
        folium.Marker([user_lat, user_lng], popup=user_location, icon=folium.Icon(color='blue')).add_to(my_map)
        folium.Marker([target_lat, target_lng], popup=location, icon=folium.Icon(color='red')).add_to(my_map)

        # Draw a line between user's location and target location
        folium.PolyLine(locations=([user_lat, user_lng], [target_lat, target_lng]), color='green').add_to(my_map)

        my_map.save("directions_map.html")
        print("Map saved as 'directions_map.html'")
    else:
        print("Failed to geocode the target location.")

if __name__ == "__main__":
    main()
