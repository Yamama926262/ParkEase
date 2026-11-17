
from parkease import ParkEase

def before_scenario(context, scenario):
    context.app = ParkEase()
    context.result = None
    context.minutes = 0
