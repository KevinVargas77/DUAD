#first idea of the dictionary

hotel = {
    "name": "",
    "star_rating": 0,
    "rooms": [
        {
            "room_number": 0,
            "floor": 0,
            "price_per_night": 0
        }
    ]
}

#testing how to input data in a dictionary

hotel_input = {
    "name": "",
    "star_rating": 0,
    "rooms": []
}

hotel_input["name"] = input("Hotel name: ")
hotel_input["star_rating"] = int(input("Star rating: "))
total_rooms = int(input("How many rooms do you want to add? "))

for i in range(total_rooms):
    print(f'\nRoom #{i+1}:')
    number = int(input("Room number: "))
    floor = int(input("Floor number: "))
    price = float(input("Price per night: "))

    room = {
        "room_number": number,
        "floor": floor,
        "price_per_night": price
    }

    hotel_input["rooms"].append(room)
print(hotel_input)
print()
# add 2 lists data to a dictionary

first_list = ['first_name','last_name','role']
second_list = ['Kevin', 'Vargas', 'Full Stack Developer']
employees = {}

for i in range(len(first_list)):
    employees[first_list[i]] = second_list[i]

print(employees)
print()

#using a list to delete data from a dictionary 

list_of_keys = ['access_level', 'age']
employee = {'name': 'John', 'email': 'john@ecorp.com', 'access_level': 5, 'age': 28}

for key in list_of_keys:
    employee.pop(key)

print(employee)
print()

#sales list and dictionaries

sales = [ 
    { 
        "date": "00/00/0000",
        "customer_email": "customer@ex.com",
        "items": [
            {
                "name": "Ex_Product",
                "upc": "ITEM-001",
                "unit_price": 25.0
            }
        ]
    }
]

totals_upc = {}

for sale in sales:
    for item in sale["items"]:
        upc = item["upc"]
        price = item["unit_price"]

        if upc in totals_upc:
            totals_upc[upc] += price
        else:
            totals_upc[upc] = price

print(totals_upc)
