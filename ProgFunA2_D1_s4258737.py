# ==============================================================================
# STUDENT INFORMATION
# Name: PRANJAY GULERIA
# Student ID: s4258737
# File Name: ProgFunA2_D1_s4258737.py
# Course: Programming Fundamentals (COSC2531)
# ==============================================================================

"""
-- Design Justification & Documentation: --

1. OOP PRINCIPLE REFLECTION (Handling the Game / Food Divergence):

To handle the cafe's offerings, I utilized Inheritance and Polymorphism. I created a base
`Offering` parent class to hold shared attributes (name, price, service_time). I then created
two subclasses: `BoardGame` and `FoodDrink`.

Alternative Considered: I considered using Composition (e.g., creating a generic Item class
and injecting a 'Behavior' object into it), but I rejected this because a Board Game intrinsically
is an Offering. Inheritance maps more logically to the real world here.

By using Inheritance, I was able to implement Polymorphism by overriding the
`service_item()` method in both subclasses. When the system calls `service_item()`,
a BoardGame will print an animated sequence for fetching and checking pieces, while a
FoodDrink will print a sequence for sending the order to the kitchen and cooking it.
This perfectly encapsulates their divergent behaviors while allowing the main program
to treat them all identically as Offerings.

2. Bug REFLECTION:

- Symptom: When running the program and trying to rent a game, the program crashed with an
  `AttributeError: 'tuple' object has no attribute 'append'`.

- Diagnosis: I traced the error back to the `Customer` class's `__init__` method. I noticed
  I had accidentally placed a trailing comma at the end of the `self.rented_games = []`
  declaration (writing it as `self.rented_games = [],`). In Python, a trailing comma
  automatically converts the variable into a tuple, which is immutable and cannot be appended to.

- Fix: I removed the trailing comma so the variable correctly initialized as a standard list.

3. REFERENCES (IEEE FORMAT):

[1] RMIT University, "Programming Fundamentals (COSC2531) Course Notes & Lectorial Slides,"
    School of Computing Technologies, RMIT University, Melbourne, Australia, 2026.

[2] Python Software Foundation, "Python 3.12 Documentation: time — Time access and conversions,"
    Python.org, 2026. [Online]. Available: https://docs.python.org/3/library/time.html.
"""

import time


class Customer:
    """Represents a customer visiting the board game cafe."""

    def __init__(self, customer_id: str, name: str, membership_type: str, phone: str, budget: float, loyalty_points: int):
        self.customer_id = customer_id
        self.name = name
        self.membership_type = membership_type
        self.phone = phone
        self.budget = budget
        self.current_table = None
        self.rented_games = []
        self.tab_total = 0.0
        self.loyalty_points = loyalty_points

    def assign_table(self, table_number: int) -> None:
        """Assigns the customer to a specific cafe table."""
        self.current_table = table_number
        print(f"🪑 {self.name} is now seated at Table {table_number}.")

    def rent_game(self, game_name: str) -> None:
        """Adds a board game to the customer's active rentals from the cafe library."""
        self.rented_games.append(game_name)
        print(f"🎲 {self.name} checked out '{game_name}' from the library.")

    def return_game(self, game_name: str) -> None:
        """Removes a game from the customer's active rentals when returned."""
        if game_name in self.rented_games:
            self.rented_games.remove(game_name)
            print(f"📥 {self.name} returned '{game_name}' to the library.")
        else:
            print(f"⚠️ {self.name} does not have '{game_name}' checked out.")

    def add_to_tab(self, amount: float, description: str) -> None:
        """Adds food, drinks, or cover charges to the customer's running tab."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.tab_total += amount
        # Earn 1 loyalty point per dollar spent on the tab
        self.loyalty_points += int(amount)
        print(f"☕ Added {description} (${amount:.2f}) to {self.name}'s tab. New total: ${self.tab_total:.2f}")

    def settle_tab(self) -> float:
        """Closes out and pays the running tab, returning the total amount paid."""
        total_to_pay = self.tab_total
        if total_to_pay == 0:
            print(f"💳 {self.name} has no open tab items.")
            return 0.0
        print(f"✅ {self.name} settled their tab of ${total_to_pay:.2f}. Thank you!")
        self.tab_total = 0.0
        self.current_table = None
        return total_to_pay

    def __str__(self) -> str:
        status = f"Table {self.current_table}" if self.current_table else "Not seated"
        games = f", Games: {', '.join(self.rented_games)}" if self.rented_games else ""
        return f"🧑 [{status}] {self.name} (ID: {self.customer_id}) | Tab: ${self.tab_total:.2f} | Points: {self.loyalty_points}{games}"


class Offering:
    def __init__(self, name: str, price: float, service_time: int):
        self.name = name
        self.price = price
        self.service_time = service_time

    def service_item(self):
        pass


class BoardGame(Offering):
    def __init__(self, name: str, price: float, service_time: int, player_count_range: str, complexity: str):
        super().__init__(name, price, service_time)
        self.player_count_range = player_count_range
        self.complexity = complexity

    def service_item(self):
        # 1. Staff goes to the shelf
        print(f"Fetching '{self.name}' from the cafe library...")
        time.sleep(0.5)  # Pauses the console for half a second

        # 2. Staff checks the box
        print(f"Verifying pieces for a {self.player_count_range} player game...")
        time.sleep(0.5)  # Pauses again

        # 3. Staff delivers it
        print(f"'{self.name}' (Complexity: {self.complexity}) is checked out and delivered to the table!")


class FoodDrink(Offering):
    def __init__(self, name: str, price: float, service_time: int, prep_time: int, temperature: str):
        super().__init__(name, price, service_time)
        self.prep_time = prep_time
        self.temperature = temperature

    def service_item(self):
        # 1. Order goes in
        print(f"Sending '{self.name}' order to the kitchen...")
        time.sleep(0.5)

        # 2. Kitchen cooks it
        print(f"Preparing food (Estimated prep time: {self.prep_time} mins)...")
        time.sleep(0.5)

        # 3. Staff serves it
        print(f"Serving '{self.name}' {self.temperature} to the table!")


class Inventory:
    def __init__(self):
        self._items = {}  # Internal dictionary to store offerings

    def load_file(self):
        with open("Offerings.csv", "r") as file:
            next(file)
            for line in file:
                OfferingID, Name, Price, Category, Subcategory, MinPlayers, MaxPlayers, Complexity, IsAvailable, PrepTime = line.strip().split(",")

                if Category == "Board game":
                    game = BoardGame(
                        name=Name,
                        price=float(Price),
                        service_time=0,
                        player_count_range=f"{MinPlayers}-{MaxPlayers}",
                        complexity=Complexity
                    )
                    self._items[Name] = game

                elif Category == "Consumable":
                    food_drink = FoodDrink(
                        name=Name,
                        price=float(Price),
                        service_time=0,
                        prep_time=int(PrepTime),
                        temperature="hot"
                    )
                    self._items[Name] = food_drink

    def get_item(self, item_name: str):
        """Searches the inventory and returns the item if found."""
        if item_name in self._items:
            return self._items[item_name]
        else:
            print(f"{item_name} is not in the catalogue.")
            return None


class Table:
    def __init__(self, table_number: int, capacity: int):
        self.table_number = table_number
        self.capacity = capacity


class TableManager:
    def __init__(self):
        self._tables = {}

    def load_file(self):
        with open("Tables.csv", "r") as file:
            next(file)
            for line in file:
                TableNumber, Desc, Seats, MinimumPlay, HasPowerOutlet, IsOccupied = line.strip().split(",")

                Table_object = Table(
                    table_number=int(TableNumber),
                    capacity=int(Seats)
                )
                self._tables[int(TableNumber)] = Table_object

    def get_table(self, table_number: int):
        tbl_num = int(table_number)
        if tbl_num in self._tables:
            return self._tables[tbl_num]
        else:
            print(f"Table {table_number} does not exist.")
            return None


class Session:
    def __init__(self, table_obj: Table, customer_obj: Customer, guest_count: int):
        self.table_obj = table_obj
        self.customer_obj = customer_obj
        self.guest_count = guest_count
        self._active_games = []
        self._ordered_food = []

    def add_offering(self, item_obj: Offering):
        if isinstance(item_obj, BoardGame):
            self._active_games.append(item_obj)
            print("Game successfully added to the table")
        elif isinstance(item_obj, FoodDrink):
            self._ordered_food.append(item_obj)
            print("Food item successfully added")
        else:
            print("Unknown item type! Please try again")

    def remove_offering(self, item_name: str):
        # Search active games
        for game in self._active_games:
            if game.name == item_name:
                self._active_games.remove(game)
                print("Game successfully removed from the table")
                return True

        # Search ordered food
        for food in self._ordered_food:
            if food.name == item_name:
                self._ordered_food.remove(food)
                print("Food item successfully removed from the table")
                return True

        print("Offering not found in the current session")
        return False

    def calculate_bill(self):
        total_bill = 0.0

        for food in self._ordered_food:
            total_bill += food.price

        for game in self._active_games:
            cover_charge = game.price * self.guest_count
            total_bill += cover_charge

        return total_bill


def main_menu():
    print("Loading Board Game Cafe System...")

    # 1. Initialize Managers and Load Data
    inventory = Inventory()
    inventory.load_file()

    table_manager = TableManager()
    table_manager.load_file()

    customers = {}

    with open("Customers.csv", "r") as file:
        next(file)
        for line in file:
            CustID, Name, MembershipType, Phone, Budget, LoyaltyPoints = line.strip().split(",")

            customers[CustID] = Customer(
                customer_id=CustID,
                name=Name,
                membership_type=MembershipType,
                phone=Phone,
                budget=float(Budget),
                loyalty_points=int(LoyaltyPoints)
            )

    active_sessions = {}  # Tracks Table Number -> Session Object
    is_running = True

    # 2. Main CLI Loop
    while is_running:
        print("\n" + "=" * 35)
        print("☕ Welcome to the Board Game Cafe 🎲")
        print("=" * 35)
        print("1. Allocate customers to a session")
        print("2. Add an offering")
        print("3. Remove an offering")
        print("4. Simulate servicing")
        print("5. Show the current bill")
        print("6. Recommend allocation")
        print("7. Exit")

        choice = input("\nPlease select an option (1-7): ")

        if choice == '1':
            print("\n--- Allocating Customer ---")
            cust_id = input("Enter Customer ID: ")
            table_num = int(input("Enter Table Number: "))
            guests = int(input("Enter number of guests: "))

            customer = customers.get(cust_id)
            table = table_manager.get_table(table_num)

            if customer is None or table is None:
                print("Invalid Customer ID or Table Number.")
            elif guests <= 0:
                print("Number of guests must be greater than zero.")
            elif guests > table.capacity:
                print(f"Number of guests exceeds the capacity of Table {table_num}.")
            elif table_num in active_sessions:
                print("Table already has an active session.")
            elif customer.current_table is not None:
                print("Customer already has an active session.")
            else:
                session = Session(table, customer, guests)
                active_sessions[table_num] = session
                customer.assign_table(table_num)

        elif choice == '2':
            print("\n--- Add Offering ---")
            table_num = int(input("Enter Table Number: "))
            item_name = input("Enter Offering Name: ")

            if table_num in active_sessions:
                item = inventory.get_item(item_name)
                if item:
                    active_sessions[table_num].add_offering(item)
            else:
                print("No active session at this table.")

        elif choice == '3':
            print("\n--- Remove Offering ---")
            table_num = int(input("Enter Table Number: "))
            item_name = input("Enter Offering Name: ")

            if table_num in active_sessions:
                active_sessions[table_num].remove_offering(item_name)
            else:
                print("No active session at this table.")

        elif choice == '4':
            print("\n--- Simulate Servicing ---")
            table_num = int(input("Enter Table Number: "))

            if table_num in active_sessions:
                session = active_sessions[table_num]
                for game in session._active_games:
                    game.service_item()
                for food in session._ordered_food:
                    food.service_item()
            else:
                print("No active session at this table.")

        elif choice == '5':
            print("\n--- Current Bill ---")
            table_num = int(input("Enter Table Number: "))

            if table_num in active_sessions:
                total = active_sessions[table_num].calculate_bill()
                print(f"Total Amount Due: ${total:.2f}")
            else:
                print("No active session at this table.")

        elif choice == '6':
            print("\n--- Recommend Allocation ---")
            print("Feature under construction.")

        elif choice == '7':
            print("\nSaving data and closing cafe. Goodbye!")
            with open("Sessions.csv", "w") as file:
                file.write("TableNumber,CustomerID,GuestCount,ActiveGames,OrderedFood\n")
                for table_num, session in active_sessions.items():
                    game_names = []
                    for game in session._active_games:
                        game_names.append(game.name)

                    food_names = []
                    for food in session._ordered_food:
                        food_names.append(food.name)

                    file.write(
                        f"{table_num},"
                        f"{session.customer_obj.customer_id},"
                        f"{session.guest_count},"
                        f"{';'.join(game_names)},"
                        f"{';'.join(food_names)}\n"
                    )
            is_running = False
        else:
            print("\nFeature under construction or invalid option.")


if __name__ == "__main__":
    main_menu()