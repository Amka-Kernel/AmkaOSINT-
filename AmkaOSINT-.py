#!/usr/bin/env python3
import requests
import dns.resolver
import phonenumbers
from phonenumbers import geocoder, carrier

BANNER = """
==================================================
                AmkaOSINT- v1.0                  
         Public Intelligence Gathering           
==================================================
"""

def lookup_ip(ip_address):
    print(f"\n[*] Querying IP: {ip_address}")
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url, timeout=5).json()
        if response.get("status") == "success":
            print(f" [+] Country: {response.get('country')}")
            print(f" [+] Region: {response.get('regionName')}")
            print(f" [+] City: {response.get('city')}")
            print(f" [+] ISP: {response.get('isp')}")
            print(f" [+] Org: {response.get('org')}")
            print(f" [+] Coordinates: {response.get('lat')}, {response.get('lon')}")
        else:
            print(" [-] Unable to retrieve info for this IP.")
    except Exception as e:
        print(f" [-] Error fetching IP details: {e}")

def lookup_domain(domain):
    print(f"\n[*] Querying Domain: {domain}")
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            print(f" [+] {rtype} Records:")
            for rdata in answers:
                print(f"     - {rdata.to_text()}")
        except Exception:
            pass

def lookup_phone(phone_num):
    print(f"\n[*] Querying Phone Number: {phone_num}")
    try:
        parsed_num = phonenumbers.parse(phone_num, None)
        if phonenumbers.is_valid_number(parsed_num):
            country = geocoder.description_for_number(parsed_num, "en")
            service_provider = carrier.name_for_number(parsed_num, "en")
            print(f" [+] Valid: Yes")
            print(f" [+] Country/Location: {country or 'Unknown'}")
            print(f" [+] Carrier: {service_provider or 'Unknown'}")
        else:
            print(" [-] Invalid phone number format. Make sure to include the country code (e.g., +254...).")
    except Exception as e:
        print(f" [-] Error processing phone number: {e}")

def lookup_username(username):
    print(f"\n[*] Searching Public Profiles for Username: {username}")
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Twitter/X": f"https://x.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Telegram": f"https://t.me/{username}",
    }
    
    headers = {"User-Agent": "Mozilla/5.0"}
    for site, url in platforms.items():
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                print(f" [+] Found on {site}: {url}")
            else:
                print(f" [-] Not found on {site}")
        except Exception:
            print(f" [-] Could not reach {site}")

def lookup_email(email):
    print(f"\n[*] Basic Email Format & Domain Analysis: {email}")
    if "@" in email:
        domain = email.split("@")[1]
        print(f" [+] Extracted Domain: {domain}")
        lookup_domain(domain)
    else:
        print(" [-] Invalid email address format.")

def main():
    print(BANNER)
    while True:
        print("\nSelect Search Category:")
        print("1. IP Address Lookup")
        print("2. Domain Lookup")
        print("3. Phone Number Analysis")
        print("4. Username Search")
        print("5. Email Domain Analysis")
        print("6. Exit")
        
        choice = input("\nEnter choice [1-6]: ").strip()
        
        if choice == '1':
            target = input("Enter IP Address: ").strip()
            lookup_ip(target)
        elif choice == '2':
            target = input("Enter Domain (e.g. example.com): ").strip()
            lookup_domain(target)
        elif choice == '3':
            target = input("Enter Phone (with country code, e.g. +254...): ").strip()
            lookup_phone(target)
        elif choice == '4':
            target = input("Enter Username: ").strip()
            lookup_username(target)
        elif choice == '5':
            target = input("Enter Email Address: ").strip()
            lookup_email(target)
        elif choice == '6':
            print("Exiting AmkaOSINT-...")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()

