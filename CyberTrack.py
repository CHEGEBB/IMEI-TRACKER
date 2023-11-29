import requests
import time
import webbrowser
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

# Function to authenticate with Google Find My Device service
def authenticate(gmail, password):
    # Simulate authentication for testing purposes
    print("Authenticating with Google Find My Device...")

# Function to authenticate with Apple Find My iPhone service
def authenticate_apple(apple_id, password):
    # Simulate authentication for testing purposes
    print("Authenticating with Apple Find My iPhone...")

# Function to request location information from Google Find My Device
def request_location(imei):
    print("Requesting location from Google Find My Device...")

    # Simulate a successful request for testing purposes
    return "37.7749,-122.4194"

# Function to parse the location information from the response
def parse_location(response_text):
    try:
        # Implement the logic to parse the location information from the response
        # and return the coordinates (latitude, longitude) as a string
        latitude, longitude = map(float, response_text.strip().split(','))
        location = f"{latitude},{longitude}"
        return location
    except (ValueError, AttributeError):
        print("Error parsing location information.")
        return None

# Function to track the device and find the location
def track(imei, gmail, password, status_display):
    status_display.config(state=NORMAL)
    status_display.delete(1.0, END)  # Clear previous status messages

    status_display.insert(END, f"Tracking Android device with IMEI: {imei}\n")

    # Prompt for Gmail and Password on the same window
    credentials = get_credentials()
    if credentials:
        gmail, password = credentials.split()

    authenticate(gmail, password)

    response_text = request_location(imei)

    if response_text is not None:
        location = parse_location(response_text)

        if location:
            find_my_device_url = f"https://www.google.com/android/find?u=0&hl=en&source=android-browser&q={location}"
            webbrowser.open(find_my_device_url)
            time.sleep(5)  # Add a delay to allow the browser to open
            status_display.insert(END, "Location found. Opening in browser.\n")
        else:
            status_display.insert(END, "Location not found.\n")
    else:
        status_display.insert(END, "Error getting location information.\n")

    status_display.insert(END, "Tracking completed.\n")
    status_display.insert(END, "Showing results...\n")
    time.sleep(2)
    status_display.insert(END, "Opening browser...\n")
    time.sleep(2)
    status_display.insert(END, "Done.\n")
    status_display.config(state=DISABLED)

# Function to get Gmail and Password from a separate window
def get_credentials():
    credentials_window = Tk()
    credentials_window.title("Enter Credentials")

    gmail_label = Label(credentials_window, text="Enter Gmail:")
    gmail_entry = Entry(credentials_window)
    gmail_label.pack()
    gmail_entry.pack()

    password_label = Label(credentials_window, text="Enter Password:")
    password_entry = Entry(credentials_window, show="*")  # Show '*' for password
    password_label.pack()
    password_entry.pack()

    # Function to store the entered credentials as instance variables
    def ok_button_click():
        credentials_window.gmail = gmail_entry.get()
        credentials_window.password = password_entry.get()
        credentials_window.destroy()

    ok_button = Button(credentials_window, text="OK", command=ok_button_click)
    ok_button.pack()

    credentials_window.wait_window()

    # Access entered values from instance variables
    gmail = credentials_window.gmail
    password = credentials_window.password

    return f"{gmail} {password}"  # Return credentials as a space-separated string

# Function to handle the track button click
def track_device():
    imei = imei_entry.get()
    track(imei, "", "", status_display)  # Pass empty strings for Gmail and Password initially

# Function to handle the track iPhone button click
def track_iphone_device():
    apple_id = apple_id_entry.get()
    password = simpledialog.askstring("Password", "Enter your password:")
    status_display.config(state=NORMAL)
    status_display.delete(1.0, END)  # Clear previous status messages
    status_display.insert(END, f"Tracking iPhone device with Apple ID: {apple_id}\n")
    authenticate_apple(apple_id, password)
    status_display.insert(END, "Tracking completed.\n")
    status_display.insert(END, "Done.\n")
    status_display.config(state=DISABLED)

# Function to clear the status display
def clear_status():
    status_display.config(state=NORMAL)
    status_display.delete(1.0, END)
    status_display.config(state=DISABLED)

# GUI setup
root = Tk()
root.title("IMEI Tracker")

# Device selection dropdown
device_var = StringVar(root)
device_var.set("Android")  # default value
device_options = ["Android", "iPhone"]
device_menu = OptionMenu(root, device_var, *device_options)
device_menu.pack()

# Android tracking UI
imei_label = Label(root, text="Enter IMEI:")
imei_entry = Entry(root)
imei_label.pack()
imei_entry.pack()

# iPhone tracking UI
apple_id_label = Label(root, text="Enter Apple ID:")
apple_id_entry = Entry(root)
apple_id_label.pack()

# Function to update UI based on selected device
def update_ui(*args):
    selected_device = device_var.get()
    if selected_device == "Android":
        imei_label.pack()
        imei_entry.pack()
        apple_id_label.pack_forget()
        apple_id_entry.pack_forget()
    elif selected_device == "iPhone":
        imei_label.pack_forget()
        imei_entry.pack_forget()
        apple_id_label.pack()
        apple_id_entry.pack()

# Call the update_ui function when device selection changes
device_var.trace_add("write", update_ui)

# Track buttons
track_button = Button(root, text="Track Device", command=track_device)
track_button.pack()

track_iphone_button = Button(root, text="Track iPhone", command=track_iphone_device)
track_iphone_button.pack()

# Clear button
clear_button = Button(root, text="Clear Status", command=clear_status)
clear_button.pack()

# Status display
status_display = Text(root, height=10, width=50, state=DISABLED)
status_display.pack()

root.mainloop()
