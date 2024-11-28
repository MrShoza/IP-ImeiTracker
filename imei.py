import requests
import webbrowser

# Ganti dengan API Key dari IMEI.info (mendaftar di imei.info untuk mendapatkan API Key)
api_key = 'YOUR_IMEI_API_KEY'
imei_number = input("Masukkan nomor IMEI untuk dilacak: ")

def check_imei_status(imei):
    url = f'https://api.imei.info/v1/imei/{imei}'
    
    # Mengirim permintaan GET dengan API Key untuk mendapatkan status IMEI
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'error' not in data:
            print("Informasi IMEI:")
            print(f"Model Perangkat: {data['model']}")
            print(f"Brand Perangkat: {data['brand']}")
            print(f"Status Blacklist: {data['blacklist_status']}")
            print(f"Tanggal Registrasi: {data['registration_date']}")
            print(f"Latitude dan Longitude: {data.get('location', 'Lokasi tidak ditemukan')}")
            
            # Jika ada informasi lokasi, menampilkan peta
            if 'location' in data:
                lat, lon = data['location'].split(',')
                lat = float(lat)
                lon = float(lon)
                show_map(lat, lon)
        else:
            print("Error: IMEI tidak valid atau tidak terdaftar.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def show_map(latitude, longitude):
    """
    Fungsi untuk menghasilkan peta berbasis Google Maps menggunakan latitude dan longitude
    """
    google_maps_url = f'https://www.google.com/maps?q={latitude},{longitude}'
    
    print(f"Lihat lokasi pada peta: {google_maps_url}")
    
    # Membuka peta di browser
    webbrowser.open(google_maps_url)

def get_ip_location():
    """
    Fungsi untuk mendapatkan lokasi perangkat berdasarkan IP address menggunakan API ipinfo.io
    """
    ip_address = requests.get('https://api.ipify.org').text  # Mendapatkan IP publik perangkat
    url = f'https://ipinfo.io/{ip_address}/json'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"IP Address: {ip_address}")
        print(f"Location: {data['city']}, {data['region']}, {data['country']}")
        print(f"Latitude and Longitude: {data['loc']}")
        
        # Pisahkan Latitude dan Longitude
        lat, lon = data['loc'].split(',')
        lat = float(lat)
        lon = float(lon)
        
        # Tampilkan lokasi di Google Maps
        show_map(lat, lon)
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Pilih metode pelacakan
choice = input("Pilih metode pelacakan:\n1. Pelacakan IMEI\n2. Pelacakan IP Address\nMasukkan pilihan (1/2): ")

if choice == '1':
    # Melakukan pelacakan IMEI
    check_imei_status(imei_number)
elif choice == '2':
    # Melakukan pelacakan IP Address
    get_ip_location()
else:
    print("Pilihan tidak valid!")
