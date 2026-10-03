class Customer:
    """Represents a customer visiting the board game cafe."""

    def __init__(self, customer_id: int, name: str, phone: str):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.current_table = None
        self.rented_games = []
        self.tab_total = 0.0
        self.loyalty_points = 0

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


# --- Quick Cafe Scenario Test ---
if __name__ == "__main__":
    # 1. Customer walks into the cafe
    guest = Customer(customer_id=402, name="Alex Mercer", phone="0412-345-678")
    print(guest)

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
