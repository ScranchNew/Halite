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
import enum
import logging

from hlt.entity import Position
from hlt.entity import Ship

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Greedy")
# Then we print our start message to the logs
logging.info("Starting my Greedy bot!")

game_state = 0
first_turn = True

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()
    
    if first_turn == 1:
        centre_place = Position(0,0)
        centre_place.x = game_map.get_me().all_ships()[0].x
        centre_place.y = game_map.get_me().all_ships()[0].y
        first_turn = False
    
    #logging.info("Centre.x: " + str(centre_place.x))
    #logging.info("Centre.y: " + str(centre_place.y))
    
    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    
    # Here I count and categorize all the planets in the game
    my_planets = []
    my_planets_not_full = []
    empty_planets = []
    enemy_planets = []
    
    planet_dict = game_map.nearby_planets_by_distance(centre_place)
    dist_list = sorted(planet_dict.keys())
    planet_list = []
    for dist in dist_list:
        planet_list.append(planet_dict.get(dist)[0])
    
    for planet in planet_list:
        if planet.is_owned() == False:
            empty_planets.append(planet)
            continue
        elif planet.owner == game_map.get_me():
            if planet.is_full() == False:
                my_planets_not_full.append(planet)
            my_planets.append(planet)
            continue
        else:
            enemy_planets.append(planet)
        continue
    
    logging.info("Listed the planets")
    
    # Find the centre of my empire
    if len(my_planets) > 0:
        for planet in my_planets:
            centre_place.x += planet.x
            centre_place.y += planet.y
        
        centre_place.x /= len(my_planets)
        centre_place.y /= len(my_planets)
    else:
        centre_place.x = game_map.get_me().all_ships()[0].x
        centre_place.y = game_map.get_me().all_ships()[0].y
        
    logging.info("New Centre.x: " + str(centre_place.x))
    logging.info("New Centre.y: " + str(centre_place.y))
    
    # Depending on the distribution I change the gamestate
    
    # Midgame (Gamestate 1) starts when there are less empty than occupied planets
    #if (len(my_planets) + len(enemy_planets)) > len(empty_planets):
        #game_state = 1
    # Lategame (Gamestate 2) starts when there are no empty planets left
    #elif (len(empty_planets) == 0):
        #game_state = 2
    
    # Rules for early game (state 0)
    if game_state == 0:
        active_ships = []
        for ship in game_map.get_me().all_ships():
            if str(ship.docking_status) == 'DockingStatus.UNDOCKED':
                active_ships.append(ship)
            continue
        
        logging.info("Listed active ships")
        
        closest_ship = active_ships[0]
        
        # Navigate ships to not already filled planets
        open_places = 0
        targets = []
        for planet in my_planets_not_full:
            logging.info("Not filled Planet: " + str(planet))
            logging.info("Ships - Spots: " + str(len(active_ships) - open_places))
            logging.info(" Docking spots: " + str(planet.num_docking_spots - len(planet.all_docked_ships())))
            if (len(active_ships) - open_places > 0):
                targets.append(planet)
                open_places += planet.num_docking_spots - len(planet.all_docked_ships())
                continue
            else:
                break
        targets.reverse()
        logging.info("Not filled Targets" + str(targets))
        for target in targets:
            logging.info("Current target: " + str(target))
            for places in range(1, planet.num_docking_spots - len(planet.all_docked_ships())):
                min_dist = 10000
                logging.info("Active ships: " + str(active_ships))
                for ship in active_ships:
                    dist_to_tgt = ship.calculate_distance_between(target)
                    if dist_to_tgt < min_dist:
                        min_dist = dist_to_tgt
                        closest_ship = ship
                logging.info("Closest ship: " + str(closest_ship))
                active_ships.remove(closest_ship)
                # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
                if closest_ship.can_dock(target):
                    # We add the command by appending it to the command_queue
                    logging.info("Nav command: " + str(closest_ship.dock(target)))
                    command_queue.append(closest_ship.dock(target))
                # Otherwise move towards it
                else:
                    navigate_command = closest_ship.navigate(closest_ship.closest_point_to(target), game_map, max_corrections=180, angular_step=3, speed=int(hlt.constants.MAX_SPEED*5/7), ignore_ships=False)
                    logging.info("Nav command: " + str(navigate_command))
                    # If we can
                    if navigate_command:
                        command_queue.append(navigate_command)
                if len(active_ships) < 1:
                    break
        
        logging.info("Navigated to not filled")
        
        # Navigate ships to empty planets
        open_places = 0
        targets = []
        for planet in empty_planets:
            logging.info("Empty Planet: " + str(planet))
            logging.info("Ships - Spots: " + str(len(active_ships) - open_places))
            logging.info(" Docking spots: " + str(planet.num_docking_spots))
            if (len(active_ships) - open_places > 0):
                targets.append(planet)
                open_places += planet.num_docking_spots
            else:
                break
        targets.reverse()
        logging.info("Empty Targets: " + str(targets) + " Docking spots: " + str(planet.num_docking_spots - len(planet.all_docked_ships())))
        for target in targets:
            logging.info("Current target: " + str(target))
            for places in range(1, planet.num_docking_spots):
                min_dist = 10000
                logging.info("Active ships: " + str(active_ships))
                for ship in active_ships:
                    dist_to_tgt = ship.calculate_distance_between(target)
                    if dist_to_tgt < min_dist:
                        min_dist = dist_to_tgt
                        closest_ship = ship
                logging.info("Closest ship: " + str(closest_ship))
                active_ships.remove(closest_ship)
                # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
                if closest_ship.can_dock(target):
                    # We add the command by appending it to the command_queue
                    logging.info("Nav command: " + str(closest_ship.dock(target)))
                    command_queue.append(closest_ship.dock(target))
                # Otherwise move towards it
                else:
                    navigate_command = closest_ship.navigate(closest_ship.closest_point_to(target), game_map, max_corrections=180, angular_step=3, speed=int(hlt.constants.MAX_SPEED*5/7), ignore_ships=False)
                    logging.info("Nav command: " + str(navigate_command))
                    # If we can
                    if navigate_command:
                        command_queue.append(navigate_command)
                if len(active_ships) < 1:
                    break
        
        logging.info("Navigated to empty")
        
        # Navigate ships to enemy planets
        targets = []
        ships_per_target = 5
        for to_kill in range(0, int(len(active_ships)/ships_per_target) - 1):
            targets.insert(0, enemy_planets[to_kill])
        logging.info("Enemy Targets" + str(targets))
        for target in targets:
            logging.info("Current target: " + str(target) + " Docking spots: " + str(planet.num_docking_spots - len(planet.all_docked_ships())))
            for num in range(1, ships_per_target):
                min_dist = 10000
                logging.info("Active ships: " + str(active_ships))
                for ship in active_ships:
                    dist_to_tgt = ship.calculate_distance_between(target)
                    if dist_to_tgt < min_dist:
                        min_dist = dist_to_tgt
                        closest_ship = ship
                logging.info("Closest ship: " + str(closest_ship))
                active_ships.remove(closest_ship)
                
                target_ship = target.all_docked_ships()[0]
                
                navigate_command = closest_ship.navigate(closest_ship.closest_point_to(target_ship), game_map, max_corrections=180, angular_step=3, speed=int(hlt.constants.MAX_SPEED), ignore_ships=True)
                logging.info("Nav command: " + str(navigate_command))
                if navigate_command:
                    command_queue.append(navigate_command)
                if len(active_ships) < 1:
                    break
         
        logging.info("Navigated to the enemy")
        
    # Rules for mid game (state 1)
    elif game_state == 1:
        pass
    # Rules for the late game (state 2)
    else:
        pass
    game.send_command_queue(command_queue)
    logging.info("Command queue: " + str(command_queue))
    
    logging.info("Turn complete")
    # TURN END
# GAME END