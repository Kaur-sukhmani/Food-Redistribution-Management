import datetime


class Food_Contributor:
    def __init__(self):
        self.cid = 0
        self.name = ""
        self.phone_no = ""
        self.email = ""
        self.address = ""
        self.type = ""
        self.createdOn = ""

    def read_food_contributor(self):
        self.name = input("Enter name of establishment ")
        self.phone_no = input("Enter phone number")
        self.email = input("Enter Email")
        self.address = input("enter address")
        contribute_types = ["restaurant", "cafe", "supermarket"]
        while True:
            self.type = input("Enter type of establishment (restaurant/cafe/supermarket): ").lower()
            if self.type in contribute_types:
                break
            else:
                print("Invalid Contribute type. Please choose from restaurant, cafe, or supermarket.")

        self.createdOn = str(datetime.datetime.today())