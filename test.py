
def hotel_cost(nights):
    return 140 * nights

def plane_ride_cost(city):
    if city == "Charlotte":
        return 183
    elif city == "Tampa":
        return 220
    elif city == "Pittsburgh":
        return 222
    elif city == "Los Angeles":
        return 475

def rental_car_cost(days):

    base = 40 * days

    if days >= 7:
        base -= 50
    elif days >= 3 and days < 7:
        base -= 20
    return base

def trip_cost(city,days,spending_money):
    total = plane_ride_cost(city) + hotel_cost(days) + rental_car_cost(days) + spending_money
    return total




print trip_cost("Los Angles", 5, 600)
