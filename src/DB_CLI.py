from itertools import product
from Database import Database

class DB_CLI:
    def __init__(self, db_path):
        self.db_path = db_path
        self.controller = None
        self.leaderSpeed = []
        self.startBraking = []
        self.frameErrorRate = []

    def run(self):
        self.display_header()
        self.select_controller()
        self.input_values()
        self.print_summary()
        self.ask_to_add_to_db()

    def display_header(self):
        print("CLI - Fill Database with enVar's")
        print("Available controllers: ")
        for i, controller in enumerate(ControllerType):
            print(f"    ({i+1}) {controller.name}")

    def select_controller(self):
        controllers = list(ControllerType)
        while True:
            try:
                controller_number = int(input("Choose a number of controller: "))
                if 1 <= controller_number <= len(controllers):
                    self.controller = controllers[controller_number-1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(controllers)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def input_values(self):
        self.leaderSpeed = self.input_list("Enter 'leaderSpeed' values (separated by comma): ")
        self.startBraking = self.input_list("Enter 'startBraking' values (separated by comma): ")
        self.frameErrorRate = self.input_list("Enter 'frameErrorRate' values (separated by comma): ")

    def input_list(self, prompt):
        while True:
            values = input(prompt)
            if not values:
                print("This field cannot be empty. Please enter values separated by comma.")
            else:
                return [value.strip() for value in values.split(',')]

    def print_summary(self):
        print("\nSummary of Entered Information:")
        print(f"Selected Controller: {self.controller.name} (Value: {self.controller.value})")
        self.print_values("Leader Speed", self.leaderSpeed)
        self.print_values("Braking", self.startBraking)
        self.print_values("Error Rate", self.frameErrorRate)

    def print_values(self, label, values):
        formatted_values = ", ".join(values)
        print(f"{label}: [{formatted_values}]")

    def ask_to_add_to_db(self):
        while True:
            choice = input("Enter 'y' to add values to DB, 'n' to exit program: ").lower()
            if choice == 'y':
                self.add_to_db()
                break
            elif choice == 'n':
                print("Exiting program.")
                exit()
            else:
                print("Invalid input. Please enter 'y' to add or 'n' to exit.")

    def generate_combinations(self):
        # Stellen Sie sicher, dass jede Liste mindestens einen Eintrag hat, um korrekte Kombinationen zu erzeugen.
        # Wenn eine Liste leer ist, fügen Sie einen Standardwert hinzu (z.B. None oder einen spezifischen Wert).
        if not self.leaderSpeed:
            self.leaderSpeed.append(None)
        if not self.startBraking:
            self.startBraking.append(None)
        if not self.frameErrorRate:
            self.frameErrorRate.append(None)

        # Erzeuge alle möglichen Kombinationen aus den drei Listen
        combinations = list(product(self.leaderSpeed, self.startBraking, self.frameErrorRate))
        
        # Optional: Entfernen Sie die Kombinationen mit None, falls Sie None als Platzhalter für leere Listen verwendet haben.
        # combinations = [combo for combo in combinations if None not in combo]

        return combinations


    def add_to_db(self):
        db = Database(self.db_path)
        db.connect()
        db.add_enVar(controller=self.controller,  values=self.generate_combinations())
        db.disconnect()
    
if __name__ == '__main__':
    cli_app = DB_CLI("C:\\Users\\timos\\Documents\\Work\\11_WiSe2324\\01_BA\\04_Git\\AutoOptSimRunner\\data.db")
    cli_app.run()