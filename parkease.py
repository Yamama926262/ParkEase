
class ExitResult:
    def __init__(self, message, parking_fee=0, ev_discount=0,
                 service_charge=0, total_payable=0, gate_open=False):
        self.message = message
        self.parking_fee = parking_fee
        self.ev_discount = ev_discount
        self.service_charge = service_charge
        self.total_payable = total_payable
        self.gate_open = gate_open


class ParkEase:
    def __init__(self):
        self.registered_drivers = set()
        self.logged_in_driver = None
        self.vehicles = {}
        self.wallet = 0

    def register(self, driver):
        self.registered_drivers.add(driver)

    def login(self, driver):
        if driver in self.registered_drivers:
            self.logged_in_driver = driver

    def linkVehicle(self, plate, electric):
        if self.logged_in_driver:
            self.vehicles[plate] = (self.logged_in_driver, electric)

    def setWallet(self, rupees):
        self.wallet = rupees

    def walletBalance(self):
        return self.wallet

    def exit(self, plate, minutesParked):
        if not self.logged_in_driver:
            return ExitResult("Driver not logged in")

        if plate not in self.vehicles:
            return ExitResult("Vehicle not linked")

        driver, electric = self.vehicles[plate]

        if driver != self.logged_in_driver:
            return ExitResult("Vehicle not linked")

        # Free exit within 15 minutes
        if minutesParked <= 15:
            return ExitResult("Free exit", gate_open=True)

        # Calculate started hours
        hours = (minutesParked + 59) // 60
        parking_fee = 100 + (hours - 1) * 60

        # Apply parking fee cap
        parking_fee = min(parking_fee, 800)          ### ---- Temporarily removed
        
       # parking_fee = parking_fee     # ------------ CHANGED MADE --------------#

        # Apply EV discount after cap
        discount = 0
        if electric:
            discount = int(parking_fee * 0.25)

        service_charge = 20
        total = parking_fee - discount + service_charge

        # Check wallet balance
        if self.wallet < total:
            return ExitResult(
                "Insufficient wallet balance",
                parking_fee, discount, service_charge,
                total, False
            )

        # Deduct payment
        self.wallet -= total

        return ExitResult(
            "Payment successful – gate opening",
            parking_fee, discount, service_charge,
            total, True
        )
