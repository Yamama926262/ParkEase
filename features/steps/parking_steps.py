
from behave import given, when, then, register_type
from parse import with_pattern
from parkease import ParkEase


# Convert amounts such as Rs. 1,000 into integers
@with_pattern(r"Rs\.\s*[\d,]+")
def parse_amount(value):
    return int(value.replace("Rs.", "").replace(",", "").strip())


register_type(amount=parse_amount)


# Given steps

@given('the driver is registered and logged in')
def login_driver(context):
    context.app.register("Ali")
    context.app.login("Ali")


@given('the driver has a linked EV')
def link_ev(context):
    context.app.linkVehicle("EV-123", True)


@given('the driver has a linked petrol vehicle')
def link_petrol(context):
    context.app.linkVehicle("PET-123", False)


@given('wallet balance is {amount:amount}')
def set_wallet(context, amount):
    context.app.setWallet(amount)


@given('the vehicle is parked for {hours:d} hours and {minutes:d} minutes')
def set_ev_time(context, hours, minutes):
    context.minutes = hours * 60 + minutes


@given('a petrol car is parked for {minutes:d} minutes')
def set_petrol_time(context, minutes):
    context.app.register("Ali")
    context.app.login("Ali")
    context.app.linkVehicle("PET-123", False)
    context.app.setWallet(10000)
    context.minutes = minutes


@given('the vehicle is parked for {minutes:d} minutes')
def set_parking_time(context, minutes):
    context.minutes = minutes


# When steps

@when('the driver exits the parking plaza')
def exit_vehicle(context):
    if "EV-123" in context.app.vehicles:
        plate = "EV-123"
    else:
        plate = "PET-123"

    context.result = context.app.exit(plate, context.minutes)


@when('the driver exits')
def exit_petrol(context):
    context.result = context.app.exit("PET-123", context.minutes)


# Then steps

@then('the message should be "{message}"')
def check_message(context, message):
    assert context.result.message == message, (
        f"Expected message: {message}, "
        f"Actual message: {context.result.message}"
    )


@then('parking fee should be {amount:amount}')
def check_fee(context, amount):
    assert context.result.parking_fee == amount, (
        f"Expected parking fee: {amount}, "
        f"Actual parking fee: {context.result.parking_fee}"
    )


@then('EV discount should be {amount:amount}')
def check_discount(context, amount):
    assert context.result.ev_discount == amount, (
        f"Expected EV discount: {amount}, "
        f"Actual EV discount: {context.result.ev_discount}"
    )


@then('service charge should be {amount:amount}')
def check_service(context, amount):
    assert context.result.service_charge == amount, (
        f"Expected service charge: {amount}, "
        f"Actual service charge: {context.result.service_charge}"
    )


@then('total payable should be {amount:amount}')
def check_total(context, amount):
    assert context.result.total_payable == amount, (
        f"Expected total: {amount}, "
        f"Actual total: {context.result.total_payable}"
    )


@then('final wallet balance should be {amount:amount}')
def check_final_wallet(context, amount):
    actual = context.app.walletBalance()
    assert actual == amount, (
        f"Expected wallet: {amount}, Actual wallet: {actual}"
    )


@then('wallet balance should remain {amount:amount}')
def check_wallet(context, amount):
    actual = context.app.walletBalance()
    assert actual == amount, (
        f"Expected wallet: {amount}, Actual wallet: {actual}"
    )


@then('nothing should be deducted')
def check_nothing_deducted(context):
    assert context.app.walletBalance() == 119, (
        f"Expected wallet: 119, "
        f"Actual wallet: {context.app.walletBalance()}"
    )


@then('the gate should open')
def check_gate_open(context):
    assert context.result.gate_open is True, "Expected gate to be open"


@then('the gate should remain closed')
def check_gate_closed(context):
    assert context.result.gate_open is False, "Expected gate to remain closed"
