

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def incoming_attack(state):
    for fleet in state.enemy_fleets():
        if fleet.destination_planet in state.my_planets():
            return True
    return False
    
def have_some_planets(state):
    return len(state.my_planets()) >= 5
