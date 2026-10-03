# ==============================================================================
# Student Details:
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

3. AI ASSISTANCE (Val):

I consulted the RMIT Val AI assistant to help structure the algorithmic logic for Tasks 8 and 10:
- For Task 8 (Billing & Checkout), Val recommended separating the one-off cover charge 
  (calculated by guest count) from the itemized running total. I implemented this in 
  `Session.calculate_bill()`. Val also outlined a strict state-transition order for checkout 
  (calculate -> record -> mark completed -> release table), which I implemented in Option 5.
- For Task 10 (Recommendation), Val suggested a "tightest fit" filter for tables 
  (`table.capacity >= party_size` then choosing the minimum). I implemented this in Option 6.
  Val also suggested calculating a "gap" between a customer's historical game complexity 
  and available games. I implemented this in the `recommend_game()` function.

4. REFERENCES (IEEE FORMAT):

[1] RMIT University, "Programming Fundamentals (COSC2531) Course Notes & Lectorial Slides,"
    School of Computing Technologies, RMIT University, Melbourne, Australia, 2026.

[2] Python Software Foundation, "Python 3.12 Documentation: time — Time access and conversions,"
    Python.org, 2026. [Online]. Available: https://docs.python.org/3/library/time.html.

[3] RMIT University, "Val AI Assistant," val.rmit.edu.au, 2026. [Online]. 
    Available: https://val.rmit.edu.au/s/c6ce747c-7a91-40e1-a462-35ffed97057f.
"""

import time
import os
import datetime
 
class Customer:
    """Represents a registered customer and tracks their tab and rented items."""
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
        self.current_table = table_number
        print(f"🪑 {self.name} is now seated at Table {table_number}.")
 
    def rent_game(self, game_name: str) -> None:
        self.rented_games.append(game_name)
        print(f"🎲 {self.name} checked out '{game_name}' from the library.")
 
    def return_game(self, game_name: str) -> None:
        if game_name in self.rented_games:
            self.rented_games.remove(game_name)
            print(f"📥 {self.name} returned '{game_name}' to the library.")
        else:
            print(f"⚠️ {self.name} does not have '{game_name}' checked out.")
 
    def add_to_tab(self, amount: float, description: str) -> None:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.tab_total += amount
        self.loyalty_points += int(amount)
        print(f"☕ Added {description} (${amount:.2f}) to {self.name}'s tab. New total: ${self.tab_total:.2f}")
 
    def settle_tab(self) -> float:
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
    """Base class for all serviceable items in the cafe."""
    def __init__(self, name: str, price: float, service_time: int, offering_id: str = ""):
        self.name = name
        self.price = price
        self.service_time = service_time
        self.offering_id = offering_id
 
    def service_item(self):
        pass
 
 
class BoardGame(Offering):
    """Subclass handling physical game rentals."""
    def __init__(self, name: str, price: float, service_time: int, player_count_range: str, complexity: str, offering_id: str = ""):
        super().__init__(name, price, service_time, offering_id)
        self.player_count_range = player_count_range 
        self.complexity = complexity
        self.checked_out = False
 
    def service_item(self):
        print(f"Fetching '{self.name}' from the cafe library...")
        time.sleep(0.5)
        print(f"Verifying pieces for a {self.player_count_range} player game...")
        time.sleep(0.5)
        print(f"'{self.name}' (Complexity: {self.complexity}) is checked out and delivered to the table!")
 
 
class FoodDrink(Offering):
    """Subclass handling kitchen preparation."""
    def __init__(self, name: str, price: float, service_time: int, prep_time: int, temperature: str, offering_id: str = ""):
        super().__init__(name, price, service_time, offering_id)
        self.prep_time = prep_time
        self.temperature = temperature
 
    def service_item(self):
        print(f"Sending '{self.name}' order to the kitchen...")
        time.sleep(0.5)
        print(f"Preparing food (Estimated prep time: {self.prep_time} mins)...")
        time.sleep(0.5)
        print(f"Serving '{self.name}' {self.temperature} to the table!")
 
 
class Inventory:
    """Manages the catalogue of all available offerings loaded from CSV."""
    def __init__(self):
        self._items = {}
        self._cover_charge = 10.00
 
    def load_file(self):
        with open("Offerings.csv", "r") as file:
            next(file)
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 10:
                    OfferingID, Name, Price, Category, Subcategory, MinPlayers, MaxPlayers, Complexity, IsAvailable, PrepTime = parts[:10]
 
                    if Category == "Board game":
                        game = BoardGame(
                            name=Name,
                            price=float(Price),
                            service_time=0,
                            offering_id=OfferingID,
                            player_count_range=f"{MinPlayers}-{MaxPlayers}",
                            complexity=Complexity
                        )
                        self._items[Name] = game
                        self._items[OfferingID] = game
 
                    elif Category == "Consumable":
                        food_drink = FoodDrink(
                            name=Name,
                            price=float(Price),
                            service_time=0,
                            prep_time=int(PrepTime),
                            temperature="hot"
                        )
                        self._items[Name] = food_drink
                        self._items[OfferingID] = food_drink
 
                    elif Category == "Fee":
                        self._cover_charge = float(Price)
 
    def get_item(self, item_name: str, show_message: bool = True):
        key = item_name.strip()
        if key in self._items:
            return self._items[key]
        short_id_match = self._find_by_short_id(key) # Sessions.csv uses short IDs such as MON-01
        if short_id_match is not None:
            return short_id_match
        if show_message:
            print(f"{item_name} is not in the catalogue.")
        return None
 
    def _find_by_short_id(self, key: str):
        """Matches short IDs (e.g. MON-01, CAT-01) to full IDs (e.g. MONO-01, CATAN-01)."""
        found = None
        if "-" in key:
            prefix, number = key.split("-", 1)
            if len(prefix) >= 3:
                for item in self.get_all_items():
                    if "-" in item.offering_id and found is None:
                        item_prefix, item_number = item.offering_id.split("-", 1)
                        if item_number == number and item_prefix.startswith(prefix):
                            found = item
        return found
 
    def get_cover_charge(self) -> float:
        return self._cover_charge
 
    def get_all_items(self) -> list:
        unique_items = []
        for item in self._items.values():
            if item not in unique_items:
                unique_items.append(item)
        return unique_items
 
    def get_board_games(self) -> list:
        games = []
        for item in self.get_all_items():
            if isinstance(item, BoardGame):
                games.append(item)
        return games
 
 
class Table:
    def __init__(self, table_number: int, capacity: int):
        self.table_number = table_number
        self.capacity = capacity
 
 
class TableManager:
    """Manages physical cafe layout and capacities."""
    def __init__(self):
        self._tables = {}
 
    def load_file(self):
        with open("Tables.csv", "r") as file:
            next(file)
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    TableNumber, Desc, Seats, MinimumPlay, HasPowerOutlet, IsOccupied = parts[:6]
 
                    Table_object = Table(
                        table_number=int(TableNumber),
                        capacity=int(Seats)
                    )
                    self._tables[int(TableNumber)] = Table_object
 
    def get_all_tables(self) -> list:
        return list(self._tables.values())
 
    def get_table(self, table_number: int):
        tbl_num = int(table_number)
        if tbl_num in self._tables:
            return self._tables[tbl_num]
        else:
            print(f"Table {table_number} does not exist.")
            return None
 
 
def current_time_string() -> str:
    """Returns the current time in the same style as Sessions.csv (e.g. 7/09/2026 14:00PM)."""
    now = datetime.datetime.now()
    return f"{now.day}/{now.strftime('%m/%Y %H:%M%p')}"
 
 
class Session:
    """Represents an active stay at a table, managing orders and running bills."""
    def __init__(self, table_obj: Table, customer_obj: Customer, guest_count: int, cover_charge: float = 10.00, session_id: str = "", start_time: str = ""):
        self.session_id = session_id
        self.start_time = start_time if start_time != "" else current_time_string()
        self.table_obj = table_obj
        self.customer_obj = customer_obj
        self.guest_count = guest_count
        self._active_games = [] # Games currently checked out (max 1 at a time)
        self._games_used = [] # Every different game borrowed this session (max 2)
        self._ordered_food = []
        self.cover_charge_per_guest = cover_charge
 
    def add_offering(self, item_obj: Offering):
        # Business logic for game limits and stock checks
        if isinstance(item_obj, BoardGame):
            if len(self._active_games) >= 1:
                print("A game is already checked out. Remove (return) it before borrowing another game.")
            elif item_obj not in self._games_used and len(self._games_used) >= 2:
                print("Game limit reached: only 2 different games can be borrowed per session.")
            elif item_obj.checked_out:
                print(f"'{item_obj.name}' is currently checked out at another table.")
            else:
                item_obj.checked_out = True
                if item_obj not in self._games_used: # A game can be played as many times as desired
                    self._games_used.append(item_obj)
                self._active_games.append(item_obj)
                print(f"Game '{item_obj.name}' successfully added to the table.")
        elif isinstance(item_obj, FoodDrink):
            self._ordered_food.append(item_obj)
            print(f"Food item '{item_obj.name}' successfully added.")
        else:
            print("Unknown item type! Please try again")
 
    def remove_offering(self, item_name: str):
        found = False
        idx = 0
        
        while not found and idx < len(self._active_games):
            if self._active_games[idx].name == item_name:
                self._active_games[idx].checked_out = False
                self._active_games.pop(idx)
                print("Game successfully removed from the table")
                found = True
            idx += 1
 
        idx = 0
        while not found and idx < len(self._ordered_food):
            if self._ordered_food[idx].name == item_name:
                self._ordered_food.pop(idx)
                print("Food item successfully removed from the table")
                found = True
            idx += 1
 
        if not found:
            print("Offering not found in the current session")
            
        return found
 
    def release_games(self):
        for game in self._active_games:
            game.checked_out = False
 
    def restore_games(self, used_games: list, active_game):
        """Rebuilds the game state of a saved session (games used and the game still checked out)."""
        for game in used_games:
            if game not in self._games_used:
                self._games_used.append(game)
        if active_game is not None and not active_game.checked_out:
            active_game.checked_out = True
            self._active_games.append(active_game)
            if active_game not in self._games_used:
                self._games_used.append(active_game)
 
    def last_game_id(self) -> str:
        """ID of the game currently checked out, otherwise the last game used."""
        if len(self._active_games) > 0:
            return self._active_games[0].offering_id
        if len(self._games_used) > 0:
            return self._games_used[-1].offering_id
        return ""
 
    def games_used_string(self) -> str:
        return ";".join([game.offering_id for game in self._games_used])
 
    def game_checked_out_string(self) -> str:
        return "True" if len(self._active_games) > 0 else "False"
 
    def calculate_bill(self) -> float:
        total_bill = 0.0
        cover_charge = self.cover_charge_per_guest * self.guest_count
        total_bill += cover_charge
        
        for food in self._ordered_food:
            total_bill += food.price
            
        # Game hire is covered by the per-guest cover charge, so games add no extra cost
 
        return total_bill
 
    def print_itemized_bill(self):
        print(f"\n--- Itemized Bill for Table {self.table_obj.table_number} ---")
        print(f"Customer: {self.customer_obj.name}")
        
        cover = self.cover_charge_per_guest * self.guest_count
        print(f"- Cover Charge ({self.guest_count} guests @ ${self.cover_charge_per_guest:.2f}):${cover:.2f}")
        
        for game in self._active_games:
            print(f"- Game Hire: {game.name} (included in cover charge)")
            
        for food in self._ordered_food:
            print(f"- Consumable: {food.name} (${food.price:.2f})")
            
        print("-" * 35)
        print(f"Total Amount Due: ${self.calculate_bill():.2f}")
 
 
def get_valid_int(prompt: str) -> int:
    """Keeps asking until the user enters a valid integer."""
    valid = False
    value = 0
    while not valid:
        user_input = input(prompt)
        try:
            value = int(user_input)
            valid = True
        except ValueError:
            print("Invalid input. Please enter a whole number.")
    return value
 
 
def find_customer(customers: dict, key: str):
    """Finds a customer by ID or by name."""
    key = key.strip()
    if key in customers:
        return customers[key]
    found = None
    for customer in customers.values():
        if found is None and customer.name.lower() == key.lower():
            found = customer
    return found
 
 
def get_past_game(customer_id: str, session_rows: list, inventory: Inventory):
    """Retrieves the customer's most recent game from saved session history."""
    past_game = None
    for row in session_rows:
        game_id = row[2]
        if game_id == "" and len(row) > 9: # Fall back to the GamesUsed column
            game_id = row[9].split(";")[-1]
        if row[1] == customer_id and game_id != "":
            game = inventory.get_item(game_id.split(";")[-1].strip(), False)
            if isinstance(game, BoardGame):
                past_game = game
    return past_game
 
 
def next_session_id(active_sessions: dict, session_rows: list) -> str:
    highest = 100
    all_ids = [row[0] for row in session_rows]
    for session in active_sessions.values():
        all_ids.append(session.session_id)
    for session_id in all_ids:
        number = session_id.replace("SES-", "")
        if number.isdigit() and int(number) > highest:
            highest = int(number)
    return f"SES-{highest + 1}"
 
 
def start_session(table, customer, guests, inventory, active_sessions, session_rows):
    session = Session(table, customer, guests, inventory.get_cover_charge(), next_session_id(active_sessions, session_rows))
    active_sessions[table.table_number] = session
    customer.assign_table(table.table_number)
    return session
 
 
def recommend_game(guests: int, past_game, inventory: Inventory):
    """Selects the best available game for the group size based on complexity gap."""
    best_game = None
    best_gap = None
    for game in inventory.get_board_games():
        min_p, max_p = map(int, game.player_count_range.split("-"))
        if min_p <= guests <= max_p and not game.checked_out:
            gap = 0.0
            if past_game is not None:
                gap = abs(float(game.complexity) - float(past_game.complexity))
                if game is past_game:
                    gap = -1.0
            if best_gap is None or gap < best_gap:
                best_game = game
                best_gap = gap
    return best_game
 
 
def main_menu():
    print("Loading Board Game Cafe System...") 
 
    # 1. Initialize core managers and load static CSV data
    inventory = Inventory()
    inventory.load_file()
 
    table_manager = TableManager()
    table_manager.load_file()
 
    customers = {}
    with open("Customers.csv", "r") as file:
        next(file)
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 6:
                CustID, Name, MembershipType, Phone, Budget, LoyaltyPoints = parts[:6]
 
                customers[CustID] = Customer(
                    customer_id=CustID,
                    name=Name,
                    membership_type=MembershipType,
                    phone=Phone,
                    budget=float(Budget),
                    loyalty_points=int(LoyaltyPoints)
                )
 
    active_sessions = {}
    saved_session_rows = []
 
    # 2. Restore prior sessions on startup to persist data between runs
    if os.path.exists("Sessions.csv"):
        with open("Sessions.csv", "r") as file:
            headers = next(file)
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 9:
                    status = parts[8].strip()
 
                    if status.lower() == "completed":
                        if len(parts) == 9: # Older file format without the two extra columns
                            parts = parts + [parts[2], "False"]
                        saved_session_rows.append(parts)
 
                    elif status.lower() == "active":
                        c_id = parts[1]
                        g_id_or_name = parts[2]
                        t_num = int(parts[3])
                        g_count = int(parts[6])
 
                        customer = customers.get(c_id)
                        table = table_manager.get_table(t_num)
 
                        # Extra columns: GamesUsed (all games this session), GameCheckedOut (True/False)
                        games_used_text = parts[9] if len(parts) > 9 else g_id_or_name
                        if len(parts) > 10:
                            game_is_out = parts[10].strip().lower() == "true"
                        else:
                            game_is_out = g_id_or_name != ""
 
                        if customer and table:
                            if t_num not in active_sessions:
                                restored_session = Session(table, customer, g_count, inventory.get_cover_charge(), parts[0], parts[4])
                                active_sessions[t_num] = restored_session
                                customer.assign_table(t_num)
 
                                used_games = []
                                for game_str in games_used_text.split(';'):
                                    if game_str.strip() != "":
                                        used_item = inventory.get_item(game_str)
                                        if isinstance(used_item, BoardGame):
                                            used_games.append(used_item)
 
                                active_game = None
                                if game_is_out and g_id_or_name != "":
                                    out_item = inventory.get_item(g_id_or_name.split(';')[0])
                                    if isinstance(out_item, BoardGame):
                                        active_game = out_item
 
                                restored_session.restore_games(used_games, active_game)
 
    is_running = True
 
    # 3. Main Interface Loop
    while is_running:
        print("\n" + "=" * 35)
        print("☕ Welcome to the Board Game Cafe 🎲")
        print("=" * 35)
        print("1. Allocate customers to a session")
        print("2. Add an offering")
        print("3. Remove an offering")
        print("4. Simulate servicing")
        print("5. Show the current bill & Checkout")
        print("6. Recommend allocation")
        print("7. Exit")
 
        choice = input("\nPlease select an option (1-7): ")
 
        if choice == '1':
            print("\n--- Allocating Customer ---")
            cust_id = input("Enter Customer ID or Name: ")
            table_num = get_valid_int("Enter Table Number: ")
            guests = get_valid_int("Enter number of guests: ")
 
            customer = find_customer(customers, cust_id)
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
                start_session(table, customer, guests, inventory, active_sessions, saved_session_rows)
 
        elif choice == '2':
            print("\n--- Add Offering ---")
            table_num = get_valid_int("Enter Table Number: ")
            item_name = input("Enter Offering Name: ")
 
            if table_num in active_sessions:
                item = inventory.get_item(item_name)
                if item:
                    active_sessions[table_num].add_offering(item)
            else:
                print("No active session at this table.")
 
        elif choice == '3':
            print("\n--- Remove Offering ---")
            table_num = get_valid_int("Enter Table Number: ")
            item_name = input("Enter Offering Name: ")
 
            if table_num in active_sessions:
                active_sessions[table_num].remove_offering(item_name)
            else:
                print("No active session at this table.")
 
        elif choice == '4':
            print("\n--- Simulate Servicing ---")
            table_num = get_valid_int("Enter Table Number: ")
 
            if table_num in active_sessions:
                session = active_sessions[table_num]
                for game in session._active_games:
                    game.service_item()
                for food in session._ordered_food:
                    food.service_item()
            else:
                print("No active session at this table.")
 
        elif choice == '5':
            print("\n--- Current Bill & Checkout ---")
            table_num = get_valid_int("Enter Table Number: ")
 
            if table_num in active_sessions:
                session = active_sessions[table_num]
                session.print_itemized_bill()
                
                checkout_prompt = input("\nDo you want to settle the bill and check out? (y/n): ")
                if checkout_prompt.lower() == 'y':
                    session.customer_obj.tab_total = session.calculate_bill()
                    final_cost = session.calculate_bill()
                    session.customer_obj.settle_tab()
 
                    # Preserve the completed session in Sessions.csv history
                    completed_row = [
                        session.session_id,
                        session.customer_obj.customer_id,
                        session.last_game_id(),
                        str(table_num),
                        session.start_time,
                        current_time_string(),
                        str(session.guest_count),
                        f"{final_cost:.2f}",
                        "Completed",
                        session.games_used_string(),
                        "False"
                    ]
                    saved_session_rows.append(completed_row)
 
                    session.release_games()
                    del active_sessions[table_num]
                    print(f"Checkout complete. Table {table_num} is now available.")
            else:
                print("No active session at this table.")
 
        elif choice == '6':
            print("\n--- Recommend Allocation ---")
            cust_id = input("Enter Customer ID or Name: ")
            guests = get_valid_int("Enter number of guests: ")
            
            customer = find_customer(customers, cust_id)
            if customer is None:
                print("Invalid Customer ID or Name.")
            elif customer.current_table is not None:
                print("Customer already has an active session.")
            else:
                # Find the tightest fit table based on capacity
                best_table = None
                for table in table_manager.get_all_tables():
                    t_num = table.table_number
                    if t_num not in active_sessions and table.capacity >= guests:
                        if best_table is None or table.capacity < best_table.capacity:
                            best_table = table
 
                # Retrieve past preference and calculate best matching game
                past_game = get_past_game(customer.customer_id, saved_session_rows, inventory)
                best_game = recommend_game(guests, past_game, inventory)
                
                if best_table is None:
                    print(f"Sorry, no available tables can accommodate {guests} guests right now.")
                elif best_game is None:
                    print(f"Sorry, we don't have suitable games for {guests} players.")
                else:
                    print(f" Recommended Table: Table {best_table.table_number} (Capacity: {best_table.capacity})")
                    print(f" Recommended Game: {best_game.name} (For {best_game.player_count_range} players)")
                    if past_game is not None:
                        print(f"   (Based on your previous game: {past_game.name})")
                    
                    accept = input("Do you want to proceed with this recommendation? (y/n): ")
                    if accept.lower() == 'y':
                        session = start_session(best_table, customer, guests, inventory, active_sessions, saved_session_rows)
                        session.add_offering(best_game)
                        print("Session started successfully based on recommendation!")
 
        elif choice == '7':
            print("\nSaving data and closing cafe. Goodbye!")
            
            # Serialize active session objects back into the CSV format
            with open("Sessions.csv", "w") as file:
                file.write("SessionID,CustomerID,GameID,TableNumber,StartTime,EndTime,GuestNumber,Cost,Status,GamesUsed,GameCheckedOut\n")
 
                for row in saved_session_rows:
                    file.write(",".join(row) + "\n")
 
                for table_num, session in active_sessions.items():
                    file.write(
                        f"{session.session_id},"
                        f"{session.customer_obj.customer_id},"
                        f"{session.last_game_id()},"
                        f"{table_num},"
                        f"{session.start_time},"
                        f","
                        f"{session.guest_count},"
                        f"{session.calculate_bill():.2f},"
                        f"Active,"
                        f"{session.games_used_string()},"
                        f"{session.game_checked_out_string()}\n"
                    )
 
            is_running = False
            
        else:
            print("\nInvalid option. Please try again.")
 
if __name__ == "__main__":
    main_menu()