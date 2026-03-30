'''
for managing lost and found item posts
''' 
import json
import uuid

def load_listings():
    global listings
    try:
        with open("listings.json", "r") as file:
            # check if the file is empty before loading
            content = file.read().strip()
            if not content:
                listings = []
            else:
                listings = json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        # if the file doesn't exist OR it's formatted badly, start fresh
        listings = []
        
def save_listings():
    with open("listings.json", "w") as file:
        json.dump(listings, file, indent=4)
        
load_listings()
       
def create_listing():
    while True:
        print("\nPOST A LOST OR FOUND ITEM")
        item_status = input("Is Your Item Lost or Found?: ").capitalize()
        
        if item_status not in ["Lost", "Found"]:
            print("Invalid Input. Please Enter 'Lost' or 'Found'")
            continue
        
        # item details 
        item_id = f"ITEM-{uuid.uuid4().hex[:8].upper()}"
        item_name = input("Enter Item Name: ")
        item_desc = input("Enter Item Description: ")
        item_loc  = input(f"Enter Location {item_status} at: ") 
        item_date = input(f"Enter Date {item_status}: ")
        item_time = input(f"Enter Time {item_status}: ")
        contact_details = input("Enter Your Contact Details: ")
        
        listing = {
            "status": item_status, 
            "id": item_id,
            "name": item_name,
            "description": item_desc,
            "location": item_loc,
            "date": item_date,
            "time": item_time,
            "contact": contact_details
        }

        listings.append(listing)
        save_listings()
        print(f"\nListing successfully added! ID: {item_id}")

        again = input("Add another? (y/n): ")
        if again.lower() != "y":
            break
        
def view_all_listings():
    if not listings:
        print("\nNo listings available.")
        return

    print("\nALL LISTINGS:")
    for item in listings:
        print("\n----------------------")
        print(f"STATUS: {item['status']}")
        print(f"Item ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Description: {item['description']}")
        print(f"Location: {item['location']}")
        print(f"Date: {item['date']}")
        print(f"Time: {item['time']}")
        print(f"Contact: {item['contact']}")
        
def lost_item_listings():
    print("\nLost Item Listings")
    found_any = False 
    
    for item in listings:
        if item['status'].capitalize() == "Lost":
            found_any = True

            print("\n----------------------")
            print(f"STATUS: {item['status']}")
            print(f"Item ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Description: {item['description']}")
            print(f"Location: {item['location']}")
            print(f"Date: {item['date']}")
            print(f"Time: {item['time']}")
            print(f"Contact: {item['contact']}")
            
        if not found_any:
            print("No lost items have been reported yet.")
            
def found_item_listings():
    print ("\nFound Item Listings")
    found_any = False 
    
    for item in listings:
        if item['status'].capitalize() == "Found":
            found_any = True

            print("\n----------------------")
            print(f"STATUS: {item['status']}")
            print(f"Item ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Description: {item['description']}")
            print(f"Location: {item['location']}")
            print(f"Date: {item['date']}")
            print(f"Time: {item['time']}")
            print(f"Contact: {item['contact']}")
            
        if not found_any:
            print("No found items have been reported yet.")
            
def my_listings():
    print("My Listings")
    
def listing_menu():
    while True:
        print("\nLISTING OPTIONS")
        print("1. Create a Post")
        print("2. View all Listings")
        print("3. Lost Item Listings")
        print("4. Found Item Listings")
        print("5. My Listings")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            create_listing()
        elif choice == '2':
            view_all_listings()
        elif choice == '3':
            lost_item_listings()
        elif choice == '4':
            found_item_listings()
        elif choice == '5':
            my_listings()
        else:
            print("Invalid Input. Try again")
            continue
            
if __name__ == "__main__":
    listing_menu()
