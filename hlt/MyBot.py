"""
Welcome to your first Halite-II bot!
This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet
Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Settler")
# Then we print our start message to the logs
logging.info("Starting my Settler bot!")

class game_state_list(Enum):
        EARLY = 0
        MID = 1
        LATE = 2

game_state = EARLY

game_map = game.update_map()

centre_place = Position(0,0)
centre_place.x = map.get_me().all_ships()[0].x
centre_place.y = map.get_me().all_ships()[0].y

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    
    # Here I count and categorize all the planets in the game
    my_planets = []
    my_planets_not_full = []
    empty_planets = []
    enemy_planets = []
    
    for entity in game_map.nearby_entities_by_distance(centre_place):
        if entity.is_planet
            if entity.is_owned() == false:
                empty_planets.append(entity)
                continue
            elif entity.owner == map.get_me():
                if entity.is_full() == false:
                    my_planets_not_full.append(entity)
                my_planets.append(entity)
                continue
            else:
                enemy_planets.append(entity)
        continue
    
    # Find the centre of my empire
    if len(my_planets) > 0:
        for planet in my_planets:
            centre_place.x += planet.x
            centre_place.y += planet.y
        
        centre_place.x /= len(my_planets)
        centre_place.y /= len(my_planets)
    else:
        centre_place.x = map.get_me().all_ships()[0].x
        centre_place.y = map.get_me().all_ships()[0].y
    
    # Depending on the distribution I change the gamestate
    
    # Midgame (Gamestate 1) starts when there are less empty than occupied planets
    if (len(my_planets) + len(enemy_planets)) > len(empty_planets):
        #game_state = MID
    # Lategame (Gamestate 2) starts when there are no empty planets left
    elif (len(empty_planets) == 0):
        #game_state = LATE
    
    # Rules for early game (state 0)
    if game_state = EARLY:
        active_ships = []
        for ship in map.get_me().all_ships():
            if ship.docking_status = 0:
                active_ships.append(ship)
            continue
        
        # Navigate ships to not already filled planets
        open_places = 0
        targets = []
        for planet in my_planets_not_full:
            if (len(active_ships) - open_places > 0):
                targets.append(planet)
                open_places += planet.num_docking_spots - len(planet.all_docked_ships())
                continue
            else:
                break
        targets.reverse()
        for target in targets:
            for places in range(1, planet.num_docking_spots - len(planet.all_docked_ships())):
                min_dist = 10000
                closest_ship
                for ship in active_ships:
                    dist = ship.calculate_distance_between(target)
                    if dist < min_dist:
                        min_dist = dist
                        closest_ship = ship
                active_ships.remove(closest_ship)
                navigate_command = ship.navigate(ship.closest_point_to(target), game_map, max_corrections=180, angular_step=3, speed=int(hlt.constants.MAX_SPEED*5/7), ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
                continue
        
        # Navigate ships to empty planets
        open_places = 0
        targets = []
        for planet in empty_planets:
            if (len(active_ships) - open_places > 0):
                targets.append(planet)
                open_places += planet.num_docking_spots)
                continue
            else:
                break
        targets.reverse()
        for target in targets:
            for places in range(1, planet.num_docking_spots):
                min_dist = 10000
                closest_ship
                for ship in active_ships:
                    dist = ship.calculate_distance_between(target)
                    if dist < min_dist:
                        min_dist = dist
                        closest_ship = ship
                active_ships.remove(closest_ship)
                navigate_command = ship.navigate(ship.closest_point_to(target), game_map, max_corrections=180, angular_step=3, speed=int(hlt.constants.MAX_SPEED*5/7), ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
                continue
        
        # Navigate ships to enemy planets
        targets = []
        ships_per_target = 5
        for to_kill in range(0, floor(len(active_ships)/ships_per_target) - 1):
            targets.insert(0, enemy_planets[to_kill])
        for target in targets:
            for num in range(1, ships_per_target):
                min_dist = 10000
                closest_ship
                for ship in active_ships:
                    dist = ship.calculate_distance_between(target)
                    if dist < min_dist:
                        min_dist = dist
                        closest_ship = ship
                active_ships.remove(closest_ship)
                
                target_ship = target.all_docked_ships()[0]
                
                navigate_command = ship.navigate(ship.closest_point_to(target_ship), game_map, max_corrections=180, angular_step=3, speed=int(hlt.constants.MAX_SPEED), ignore_ships=True)
                if navigate_command:
                    command_queue.append(navigate_command)
                continue
                
    # Rules for mid game (state 1)
    elif game_state = MID:
        
    # Rules for the late game (state 2)
    else:
        
    game.send_command_queue(command_queue)
    # TURN END
# GAME END