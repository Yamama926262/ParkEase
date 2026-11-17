
Feature: Automatic parking fee payment
  As a registered ParkEase driver, I want my parking fee to be
  charged automatically from my wallet when I exit, so that I
  can leave the plaza without queuing at a payment booth.

  @smoke
  Scenario: Successful EV payment
    Given the driver is registered and logged in
    And the driver has a linked EV
    And wallet balance is Rs. 1,000
    And the vehicle is parked for 3 hours and 40 minutes
    When the driver exits the parking plaza
    Then the message should be "Payment successful – gate opening"
    And parking fee should be Rs. 280
    And EV discount should be Rs. 70
    And service charge should be Rs. 20
    And total payable should be Rs. 230
    And final wallet balance should be Rs. 770
    And the gate should open

  @boundary
  Scenario Outline: Petrol parking fee calculation
    Given a petrol car is parked for <minutes> minutes
    When the driver exits
    Then parking fee should be Rs. <fee>
    And total payable should be Rs. <total>

    Examples: Free and rounding
      | minutes | fee | total |
      | 15      | 0   | 0     |
      | 16      | 100 | 120   |
      | 60      | 100 | 120   |
      | 61      | 160 | 180   |

    Examples: Daily cap
      | minutes | fee | total |
      | 720     | 760 | 780   |
      | 721     | 800 | 820   |

  @negative
  Scenario: Payment fails due to insufficient balance
    Given the driver is registered and logged in
    And the driver has a linked petrol vehicle
    And wallet balance is Rs. 119
    And the vehicle is parked for 60 minutes
    When the driver exits the parking plaza
    Then the message should be "Insufficient wallet balance"
    And wallet balance should remain Rs. 119
    And nothing should be deducted
    And the gate should remain closed
