import requests
import time
import webbrowser
from getpass import getpass
import os
from time import sleep
import re

def clear_screen():
    os.system('clear')

def animate_text(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()

def show_banner():
    banner = """
╔══════════════════════════════════════╗
║          IMEI TRACKER v2.0           ║
║      Created for Termux Users        ║
╚══════════════════════════════════════╝
    """
    print("\033[94m" + banner + "\033[0m")

def loading_animation(text, duration=2):
    symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start_time = time.time()
    i = 0
    while time.time() - start_time < duration:
        print(f'\r{text} {symbols[i%len(symbols)]}', end='', flush=True)
        time.sleep(0.1)
        i += 1
    print()

def validate_imei(imei):
    """Validate IMEI number format."""
    if not re.match(r'^\d{15}$', imei):
        return False
    return True

def validate_email(email):
    """Validate email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def authenticate(gmail, password):
    loading_animation("Authenticating with Google Find My Device")
    # This is a simulation - in a real implementation, you would use Google's API
    return True

def authenticate_apple(apple_id, password):
    loading_animation("Authenticating with Apple Find My iPhone")
    # This is a simulation - in a real implementation, you would use Apple's API
    return True

def request_location(imei):
    loading_animation("Requesting device location")
    # Simulated location request
    return "37.7749,-122.4194"

def parse_location(response_text):
    try:
        latitude, longitude = map(float, response_text.strip().split(','))
        return f"{latitude},{longitude}"
    except (ValueError, AttributeError):
        animate_text("Error: Could not parse location information.", 0.03)
        return None

def track_android(imei, gmail, password):
    if not validate_imei(imei):
        animate_text("Error: Invalid IMEI format. Please enter a 15-digit IMEI number.", 0.03)
        return

    if not validate_email(gmail):
        animate_text("Error: Invalid email format.", 0.03)
        return

    animate_text(f"Tracking Android device with IMEI: {imei}", 0.03)
    
    if authenticate(gmail, password):
        response_text = request_location(imei)
        if response_text:
            location = parse_location(response_text)
            if location:
                find_my_device_url = f"https://www.google.com/android/find?u=0&hl=en&source=android-browser&q={location}"
                animate_text("\nLocation found! Opening map...", 0.03)
                print(f"\n\033[92mDevice Location URL:\033[0m {find_my_device_url}")
                try:
                    webbrowser.open(find_my_device_url)
                except Exception as e:
                    print(f"\n\033[91mError opening browser: {e}\033[0m")

def track_iphone(apple_id, password):
    if not validate_email(apple_id):
        animate_text("Error: Invalid Apple ID format.", 0.03)
        return

    animate_text(f"Tracking iPhone device with Apple ID: {apple_id}", 0.03)
    
    if authenticate_apple(apple_id, password):
        # Simulated tracking process
        loading_animation("Accessing Find My iPhone service")
        animate_text("\nTracking completed. This is a simulation.", 0.03)

def main():
    try:
        while True:
            clear_screen()
            show_banner()
            
            animate_text("\nSelect device type:", 0.03)
            print("\033[96m1.\033[0m Android")
            print("\033[96m2.\033[0m iPhone")
            print("\033[96m3.\033[0m Exit")
            
            choice = input("\n\033[93mEnter your choice (1-3):\033[0m ")
            
            if choice == "1":
                clear_screen()
                show_banner()
                imei = input("\n\033[93mEnter IMEI:\033[0m ")
                gmail = input("\033[93mEnter Gmail:\033[0m ")
                password = getpass("\033[93mEnter Password:\033[0m ")
                track_android(imei, gmail, password)
            
            elif choice == "2":
                clear_screen()
                show_banner()
                apple_id = input("\n\033[93mEnter Apple ID:\033[0m ")
                password = getpass("\033[93mEnter Password:\033[0m ")
                track_iphone(apple_id, password)
            
            elif choice == "3":
                animate_text("\nThank you for using IMEI Tracker!", 0.03)
                break
            
            else:
                print("\n\033[91mInvalid choice. Please try again.\033[0m")
            
            input("\n\033[93mPress Enter to continue...\033[0m")

    except KeyboardInterrupt:
        print("\n\n\033[91mProgram terminated by user.\033[0m")
    except Exception as e:
        print(f"\n\033[91mAn error occurred: {e}\033[0m")

if __name__ == "__main__":
    main()