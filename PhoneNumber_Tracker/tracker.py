import webbrowser
import requests

def get_location(lat, lng, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat},{lng}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        return data['results'][0]['formatted']
    else:
        return None

def main():
    api_key = 'YOUR_API_KEY'  # Replace with your OpenCage API key
    current_lat = input("Enter your current latitude: ")
    current_lng = input("Enter your current longitude: ")
    dest_lat = input("Enter destination latitude: ")
    dest_lng = input("Enter destination longitude: ")

    current_location = get_location(current_lat, current_lng, api_key)
    dest_location = get_location(dest_lat, dest_lng, api_key)

    print(f"Your current location: {current_location}")
    print(f"Destination location: {dest_location}")

    maps_url = f"https://www.google.com/maps/dir/{current_lat},{current_lng}/{dest_lat},{dest_lng}"
    webbrowser.open(maps_url)

if __name__ == "__main__":
    main()
