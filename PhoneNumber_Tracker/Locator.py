import phonenumbers
from phonenumbers import geocoder as phonenumbers_geocoder
from phonenumbers import carrier
from opencage.geocoder import OpenCageGeocode
import webbrowser
import math
import time
import sys  # Added sys for stdout
from colorama import Fore, Style

# Replace with your OpenCage API key
key = "8c3d04ff9f4a410b8ba3d6e8aa9408f7"

def get_coordinates(location, api_key):
    geocoder = OpenCageGeocode(api_key)
    result = geocoder.geocode(location)
    if result and len(result):
        return result[0]['geometry']['lat'], result[0]['geometry']['lng']
    else:
        return None, None

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

def print_animated_message(message):
    animation = "|/-\\"
    for i in range(20):
        time.sleep(0.1)
        sys.stdout.write(f"\r{Fore.GREEN}{animation[i % len(animation)]} {message}{Style.RESET_ALL}")
        sys.stdout.flush()

def main():
    print(Fore.YELLOW + r"""
  ___           _   _     _               ____            _             
 |_ _|  _ __   | | (_) __| |  ___  _ __  / ___|   ___  __| |  ___  _ __ 
  | |  | '_ \  | | | |/ _` | / _ \| '__| \___ \  / _ \/ _` | / _ \| '__|
  | |  | | | | | | | | (_| ||  __/| |     ___) ||  __/ (_| ||  __/| |   
 |___| |_| |_| |_| |_|\__,_| \___||_|    |____/  \___|\__,_| \___||_|   
                                                                        
    """ + Style.RESET_ALL)
    
    print(Fore.YELLOW + "Created by CHEGEBB" + Style.RESET_ALL)
    print(Fore.YELLOW + "Computer Science Student and Cybersecurity Enthusiast" + Style.RESET_ALL)
    print(Fore.YELLOW + "GitHub: https://github.com/CHEGEBB" + Style.RESET_ALL)
    print_animated_message("Welcome to Phone Number Locator!")

    print(Fore.BLUE + "\nPlease provide the phone number to locate:" + Style.RESET_ALL)
    number = input("Enter phone number in international format (e.g., +123456789): ")

    new_number = phonenumbers.parse(number)
    location = phonenumbers_geocoder.description_for_number(new_number, "en")
    print(f"\nLocation based on phone number: {Fore.GREEN}{location}{Style.RESET_ALL}")

    service_name = carrier.name_for_number(new_number, "en")
    print(f"Service provider: {Fore.BLUE}{service_name}{Style.RESET_ALL}")

    # Use OpenCage to geocode the location from the phone number
    geocoder_client = OpenCageGeocode(key)
    query = str(location)
    print("\nLocating the target coordinates...")
    result = geocoder_client.geocode(query)

    if result and len(result):
        target_lat = result[0]['geometry']['lat']
        target_lng = result[0]['geometry']['lng']
        print(f"Target coordinates: {Fore.GREEN}{target_lat}, {target_lng}{Style.RESET_ALL}")

        # Ask user for their current location (in a more user-friendly format)
        print(Fore.BLUE + "\nEnter your current location (city or address):" + Style.RESET_ALL)
        user_location_input = input("Location: ")
        print("\nLocating your current coordinates...")
        user_lat, user_lng = get_coordinates(user_location_input, key)

        if user_lat is not None and user_lng is not None:
            print(f"Your current location: {Fore.GREEN}{user_location_input}{Style.RESET_ALL}")

            # Calculate distance between user's location and target location
            distance = calculate_distance(user_lat, user_lng, target_lat, target_lng)
            print(f"Distance to target location: {Fore.BLUE}{distance:.2f} km{Style.RESET_ALL}")

            # Open Google Maps with directions
            maps_url = f"https://www.google.com/maps/dir/{user_lat},{user_lng}/{target_lat},{target_lng}"
            webbrowser.open(maps_url)

        else:
            print(f"\nFailed to geocode the location: {Fore.RED}{user_location_input}{Style.RESET_ALL}")

    else:
        print("\nFailed to geocode the target location.")

if __name__ == "__main__":
    main()
