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

    def __init__(self, name: str, price: float, service_time: int ):
        self.name=name
        self.price=price
        self.service_time=service_time

    def service_item(self):
        pass

class BoardGame(Offering):

    def __init__(self, name: str, price: float, service_time: int, player_count_range: str, complexity: str):
        super().__init__(name, price, service_time)
        self.player_count_range=player_count_range
        self.complexity=complexity

    def service_item(self):
        # Divergent behavior for a game
        print(f" Checking out '{self.name}' ({self.complexity} complexity) to the table.")

class FoodDrink(Offering):
    def __init__(self, name: str, price: float, service_time: int, prep_time: int, temperature: str):
        super().__init__(name, price, service_time)
        self.prep_time=prep_time
        self.temperature=temperature

    def service_item(self):
        # Divergent behavior for food/drink
        print(f" Preparing a {self.temperature} '{self.name}'. It will take {self.prep_time} mins.")

class Inventory():

    def __init__(self):
        self._items = {} # Private dictionary to store offerings

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

class Table():

    def __init__(self,table_number: int, capacity: int):
        self.table_number=table_number
        self.capacity=capacity

class TableManager():

    def __init__(self):
        self._tables = {}

    def load_file(self):

        with open("Tables.csv","r") as file:
            next(file)
            for line in file:
                TableNumber,Desc,Seats,MinimumPlay,HasPowerOutlet,IsOccupied=line.strip().split(",")
                Table_object=Table(table_number=int(TableNumber), capacity=int(Seats))
                self._tables[int(TableNumber)] = Table_object

    def get_table(self, table_number: int):
        tbl_num = int(table_number)
        if tbl_num in self._tables:
            return self._tables[tbl_num]
        else:
            print(f" Table {table_number} does not exist.")
            return None

class Session:

    def __init__(self, table_obj: Table, customer_obj: Customer, guest_count: int):
        self.table_obj = table_obj
        self.customer_obj = customer_obj
        self.guest_count = guest_count

        self._active_games = []
        self._ordered_food = []


# --- Quick Cafe Scenario Test ---
if __name__ == "__main__":
    # 1. Customer walks into the cafe

    customers = {}

    with open("Customers.csv","r") as file:
        next(file)
        for line in file:
            CustID, Name, MembershipType, Phone, Budget, LoyaltyPoints = line.strip().split(",")
            guest = Customer(customer_id=CustID,
                name=Name,
                membership_type=MembershipType,
                phone=Phone,
                budget=float(Budget),
                loyalty_points=int(LoyaltyPoints))
            customers[CustID] = guest

        

    # 2. Staff seats them and they grab a game
    guest.assign_table(12)
    guest.rent_game("Carcassonne")
    
    # 3. They order refreshments and a cover charge
    guest.add_to_tab(10.00, "Cafe Board Game Cover Charge")
    guest.add_to_tab(6.50, "Flat White & Anzac Biscuit")
    print(guest)

    # 4. They switch games
    guest.return_game("Carcassonne")
    guest.rent_game("Catan")

    # 5. End of the night: return game and pay
    guest.return_game("Catan")
    guest.settle_tab()
    print(guest)


