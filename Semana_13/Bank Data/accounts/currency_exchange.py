exchange_rate = 540 

def validate_numeric_params(func): #Exercise 2
    def wrapper(*args, ** kwargs ):
        for arg in args:
            if not isinstance(arg,(int,float)):
                raise TypeError(f"Invalid Input: {arg} is not a number.")
            return func(*args, **kwargs)
        return wrapper 
    

def dollars_to_colones(amount):
    return amount * exchange_rate 


def colones_to_dollars(amount):
    return amount / exchange_rate


def currency_exchange(): 
    while True: 
        print("\nCurrency Conversion:")
        print("1. Dollars to Colones")
        print("2. Colones to Dollars")
        print("3. Back")

        sub_option = input("Choose conversion option: ")

        if sub_option == "1":
            try:
                amount = float(input("Enter the amount in dollars: "))     
                result = dollars_to_colones(amount)
                print(f"{amount:.2f} USD = {result:.2f} CRC")
            except ValueError: 
                print("Please enter a valid number.")
            except TypeError as e:
                print(e)    

        elif sub_option == "2":
            try:
                amount = float(input("Enter the amount in colones: "))     
                result = colones_to_dollars(amount)
                print(f"{amount:.2f} CRC = {result:.2f} USD")
            except ValueError: 
                print("Please enter a valid number.")
            except TypeError as e:
                print(e)

        elif sub_option == "3":
            break

        else: 
            print("Please try a valid option.") 