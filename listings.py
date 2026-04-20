import json
import uuid
import os

# ===================
# READ AND LOAD CONTENT
# ===================
def load_listings():
    # If file doesn't exist or is empty, return an empty list
    if not os.path.exists("listings.json") or os.stat("listings.json").st_size == 0:
        with open("listings.json", "w") as file:
            json.dump([], file)
        return []
    
    with open("listings.json", "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

# ===================
# SAVE LISTINGS
# ===================       
def save_listings(listings):
    with open("listings.json", "w") as file:
        json.dump(listings, file, indent=4)

# ===================
# CREATE LISTING
# ===================      
def create_listing(current_user):
    listings = load_listings() # Get fresh data
    while True:
        print("\nPOST A LOST OR FOUND ITEM")
        item_status = input("Is Your Item Lost or Found?: ").capitalize()
        
        if item_status not in ["Lost", "Found"]:
            print("Invalid Input. Please Enter 'Lost' or 'Found'")
            continue
        
        item_id = f"ITEM-{uuid.uuid4().hex[:8].upper()}"
        item_name = input("Enter Item Name: ")
        item_desc = input("Enter Item Description: ")
        item_loc  = input(f"Enter Location {item_status} at: ") 
        item_date = input(f"Enter Date {item_status}: ")
        contact_details = input("Enter Your Contact Details: ")
        
        listing = {
            "user": current_user,
            "status": item_status, 
            "id": item_id,
            "name": item_name,
            "description": item_desc,
            "location": item_loc,
            "date": item_date,
            "contact": contact_details
        }

        listings.append(listing)
        save_listings(listings)
        print(f"\nListing successfully added! ID: {item_id}")

        again = input("Add another? (y/n): ")
        if again.lower() != "y":
            break
        
# ===================
# VIEW LISTINGS
# ===================        
def view_all_listings():
    listings = load_listings()
    if not listings:
        print("\nNo listings available.")
        return

    print("\nALL LISTINGS:")
    for item in listings:
        print_item(item)

def lost_item_listings():
    print("\nLost Item Listings")
    listings = load_listings()
    found_any = False 
    for item in listings:
        if item['status'] == "Lost":
            print_item(item)
            found_any = True
    if not found_any: print("No lost items reported yet.")

def found_item_listings():
    print("\nFound Item Listings")
    listings = load_listings()
    found_any = False 
    for item in listings:
        if item['status'] == "Found":
            print_item(item)
            found_any = True
    if not found_any: print("No found items reported yet.")

def my_listings(current_user):
    print("\nMY LISTINGS")
    listings = load_listings()
    found_any = False
    for item in listings:
        if item.get("user") == current_user:
            print_item(item)
            found_any = True
    if not found_any: print("You have no listings yet.")

# Helper to avoid repeating print statements
def print_item(item):
    print("\n----------------------")
    print(f"STATUS: {item['status']} | ID: {item['id']}")
    print(f"Name: {item['name']}")
    print(f"Description: {item['description']}")
    print(f"Location: {item['location']}")
    print(f"Date: {item['date']}")
    print(f"Contact: {item['contact']}")

# ===================
# SEARCH LISTINGS
# ===================
def search_listings():
    keyword = input("\nEnter keyword to search: ").lower()
    listings = load_listings()
    found = False
    for item in listings:
        if any(keyword in str(item[k]).lower() for k in ['name', 'description', 'location']):
            print_item(item)
            found = True
    if not found: print("No matching items found.")

# ===================
# EDIT / DELETE
# ===================
def edit_listing(current_user):
    listings = load_listings()
    edit_id = input("\nEnter Item ID to edit: ").strip().upper()

    for item in listings:
        if item["id"] == edit_id and item["user"].lower() == current_user.lower():
            print("\nLeave blank to keep current value.\n")
            
            new_status = input(f"New Status ({item['status']}): ").capitalize()
            new_name = input(f"New Name ({item['name']}): ")
            new_desc = input(f"New Description ({item['description']}): ")
            
            if new_status in ["Lost", "Found"]: item['status'] = new_status
            if new_name: item['name'] = new_name
            if new_desc: item['description'] = new_desc
            # (Add other fields as needed following this pattern)

            save_listings(listings)
            print("Listing updated successfully!")
            return
    print("Item not found or not yours.")

def delete_listing(current_user):
    listings = load_listings()
    delete_id = input("\nEnter Item ID to delete: ").strip().upper()

    for item in listings:
        if item["id"] == delete_id and item["user"].lower() == current_user.lower():
            if input("Confirm deletion? (y/n): ").lower() == "y":
                listings.remove(item)
                save_listings(listings)
                print("Deleted successfully.")
            return
    print("Item not found or not yours.")

# ===================
# MENU
# ===================
def listing_menu(current_user):
    while True:
        print("\n--- LISTING OPTIONS ---")
        print("1. Create Post | 2. View All | 3. Lost | 4. Found")
        print("5. My Posts   | 6. Search   | 7. Edit | 8. Delete")
        print("9. Back to Main Menu")
        choice = input("Select: ").strip()
        
        if choice == '1': create_listing(current_user)
        elif choice == '2': view_all_listings()
        elif choice == '3': lost_item_listings()
        elif choice == '4': found_item_listings()
        elif choice == '5': my_listings(current_user)
        elif choice == '6': search_listings()
        elif choice == '7': edit_listing(current_user)
        elif choice == '8': delete_listing(current_user)
        elif choice == '9': break
        else: print("Invalid Input.")