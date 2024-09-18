import requests

IPGEOLOCATION_API_KEY = 'b03d06ec5b3e447bb3642627a027c32a' 

def get_public_ip():
    try:
        response = requests.get(f'https://api.ipgeolocation.io/getip')
        response.raise_for_status()
        return response.json().get('ip')
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

def get_location_from_ip(ip):
    if ip is None:
        return None

    geo_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={IPGEOLOCATION_API_KEY}&ip={ip}"
    try:
        response = requests.get(geo_url)
        response.raise_for_status() 
        data = response.json()
        if data:
            return data.get('city', 'Unknown City') + ", " + data.get('country_name', 'Unknown Country')
        else:
            print("No location information found.")
            return None
    except requests.RequestException as e:
        print(f"Error fetching location information: {e}")
        return None

def ip():
    ip_address = get_public_ip()
    if ip_address:
        print(f"Public IP Address: {ip_address}")
        location = get_location_from_ip(ip_address)
        if location:
            return location
        else:
            return False
