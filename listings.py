
"""
============================================
listings.py - Lost & Found Listings Module
============================================
This file contains the core logic for managing lost and found item listings. 
It handles the creation, storage, retrieval, searching, editing, and deletion 
of listings using a local JSON file as persistent storage.

Functions:
    load_listings()            -- Loads all listings from listings.json.
    save_listings(listings)    -- Saves the updated listings list to file.
    create_listing(user)       -- Posts a new lost or found item listing.
    view_all_listings()        -- Displays all listings regardless of status.
    lost_item_listings()       -- Filters and displays lost items only.
    found_item_listings()      -- Filters and displays found items only.
    my_listings(user)          -- Displays listings belonging to the current user.
    search_listings()          -- Searches listings by name, description, or location.
    edit_listing(user)         -- Edits an existing listing owned by the current user.
    delete_listing(user)       -- Deletes a listing owned by the current user.
    listing_menu(user)         -- Main menu loop for all listing operations.

Purpose of the File:
This module serves as the backend logic for listing management in the
Lost and Found system. It is intended to be integrated with an
authentication system and acts as the main handler for all listing-related
operations in a console-based application.

Author:  Onikka Mae Buela
Date:    April 20, 2026
"""

import json
import uuid

# ============================================
# READ AND LOAD CONTENT INSIDE 'listings.json'
# ============================================

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

# ====================================
# SAVE NEW LISTING TO 'listings.json'
# ====================================      

def save_listings():
    with open("listings.json", "w") as file:
        json.dump(listings, file, indent=4)

load_listings()

# ===================
# CREATE LISTING
# ===================      

def create_listing(current_user):
    while True:
        print("\nPOST A LOST OR FOUND ITEM")
        item_status = input("Is Your Item Lost or Found?: ").capitalize()    

        if item_status not in ["Lost", "Found"]:
            print("Invalid Input. Please Enter 'Lost' or 'Found'")
            continue
        
# asks [user] for listing item details
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
        save_listings()

        print(f"\nListing successfully added! ID: {item_id}")
        
        again = input("Add another? (y/n): ")
        if again.lower() != "y":
            break

# ==========================
# VIEW ALL ACTIVE LISTINGS
# =========================        

def view_all_listings():
    if not listings:
        print("\nNo listings available.")
        return

# check listings.json if there are active listings
    print("\nALL LISTINGS:")
    for item in listings:
        print("\n----------------------")
        print(f"STATUS: {item['status']}")
        print(f"Item ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Description: {item['description']}")
        print(f"Location: {item['location']}")
        print(f"Date: {item['date']}")
        print(f"Contact: {item['contact']}")

# =============================
# VIEW ONLY LOST ITEM LISTINGS
# =============================

def lost_item_listings():
    print("\nLost Item Listings")
    found_any = False

# check listings.json if there are active listings under 'Lost'
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
            print(f"Contact: {item['contact']}")

    if not found_any:
        print("No lost items have been reported yet.")

# ==============================
# VIEW ONLY FOUND ITEM LISTINGS
# ==============================          

def found_item_listings():
    print ("\nFound Item Listings")
    found_any = False

# check listings.json if there are active listings under 'Found'
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
            print(f"Contact: {item['contact']}")

    if not found_any:
        print("No found items have been reported yet.")

# ===================
# VIEW MY LISTINGS
# ===================            

def my_listings(current_user):
    print("\nMY LISTINGS")
    found_any = False

# check listings.json if there are active listings under [user]
    for item in listings:
        if item.get("user") == current_user:
            found_any = True

            print("\n----------------------")
            print(f"STATUS: {item['status']}")
            print(f"Item ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Description: {item['description']}")
            print(f"Location: {item['location']}")
            print(f"Date: {item['date']}")
            print(f"Contact: {item['contact']}")

    if not found_any:
        print("You have no listings yet.")

# ==========================
# SEARCH LISTINGS BY KEYWORD
# ==========================

def search_listings():
    global listings
    keyword = input("\nEnter keyword to search: ").lower()
    found = False

# search keyword inside listings.json
    for item in listings:
        if (keyword in item['name'].lower() or
            keyword in item['description'].lower() or
            keyword in item['location'].lower()):

            found = True
            print("\n----------------------")
            print(f"STATUS: {item['status']}")
            print(f"Item ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Description: {item['description']}")
            print(f"Location: {item['location']}")
            print(f"Date: {item['date']}")
            print(f"Contact: {item['contact']}")

    if not found:
        print("No matching items found.")  

# ===================
# EDIT USER LISTING
# ===================

def edit_listing(current_user):
    print("\nEDIT YOUR LISTING")
    
# check listings only owned by the [user]
    user_items = [
        item for item in listings
        if item.get("user", "").lower() == current_user.lower()
    ]

    if not user_items:
        print("You have no listings to edit.")
        return

    for item in user_items:
        print("\n----------------------")
        print(f"Item ID: {item['id']}")
        print(f"Name: {item['name']}")

    edit_id = input("\nEnter Item ID to edit: ").strip()

# enables [user] to enter new values in chosen listing
    for item in listings:
        if item["id"] == edit_id and item["user"].lower() == current_user.lower():
            print("\nLeave blank to keep current value.\n")

            new_status = input(f"New Status ({item['status']} - Lost/Found): ")
            new_name = input(f"New Name ({item['name']}): ")
            new_desc = input(f"New Description ({item['description']}): ")
            new_loc = input(f"New Location ({item['location']}): ")
            new_date = input(f"New Date ({item['date']}): ")
            new_contact = input(f"New Contact ({item['contact']}): ")

            if new_status.capitalize() in ["Lost", "Found"]:
                item['status'] = new_status.capitalize()
            if new_name:
                item['name'] = new_name
            if new_desc:
                item['description'] = new_desc
            if new_loc:
                item['location'] = new_loc
            if new_date:
                item['date'] = new_date
            if new_contact:
                item['contact'] = new_contact
           
            save_listings()
            print("Listing updated successfully!")
            return

    print("Item not found or not yours.")

# ====================
# DELETE USER LISTING
# ====================

def delete_listing(current_user):
    print("\nDELETE YOUR LISTING")

    user_items = [
        item for item in listings
        if item.get("user", "").lower() == current_user.lower()
    ]

    if not user_items:
        print("You have no listings to delete.")
        return

    for item in user_items:
        print("\n----------------------")
        print(f"Item ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Status: {item['status']}")

# asks the [user] for the item ID to delete
    delete_id = input("\nEnter Item ID to delete: ").strip()
    for item in listings:
        if item["id"] == delete_id and item["user"].lower() == current_user.lower():
            
            confirm = input("Are you sure you want to delete this? (y/n): ").lower()
            if confirm == "y":
                listings.remove(item)
                save_listings()
                print("Listing deleted successfully.")
            else:
                print("Deletion cancelled.")
            return
        
    print("Item not found or you do not own this listing.")

# ===================
# LISTING MENU
# ===================

def listing_menu(current_user):
    while True:

        print("\nLISTING OPTIONS")
        print("1. Create a Post")
        print("2. View all Listings")
        print("3. Lost Item Listings")
        print("4. Found Item Listings")
        print("5. My Listings")
        print("6. Search By Keyword")
        print("7. Edit My Listing")
        print("8. Delete My Listing")
        choice = input("Select an option: ").strip()