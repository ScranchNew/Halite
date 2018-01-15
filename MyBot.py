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
    
    if first_turn == True:
        enemies = game_map.all_players()
        enemies.remove(game_map.get_me())
        
        centre_place = Position(0,0)
        centre_place.x = game_map.get_me().all_ships()[0].x
        centre_place.y = game_map.get_me().all_ships()[0].y
        
        centre_enemy = Position(0,0)
        for enemy in enemies:
            centre_enemy.x += enemy.all_ships()[0].x
            centre_enemy.y += enemy.all_ships()[0].y
        centre_enemy.x /= len(enemies)
        centre_enemy.y /= len(enemies)
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
    centre_place.x = 0
    centre_place.y = 0

    if len(my_planets) > 0:
        for planet in my_planets:
            centre_place.x += planet.x
            centre_place.y += planet.y
        
        centre_place.x /= len(my_planets)
        centre_place.y /= len(my_planets)
    else:
        for ship in game_map.get_me().all_ships():
            centre_place.x += ship.x
            centre_place.y += ship.y
        
        centre_place.x /= len(game_map.get_me().all_ships())
        centre_place.y /= len(game_map.get_me().all_ships())
        
    logging.info("New Centre.x: " + str(centre_place.x))
    logging.info("New Centre.y: " + str(centre_place.y))
    
    '''    # Find the centre of the enemy
    
    centre_enemy.x = 0
    centre_enemy.y = 0
    
    if len(enemy_planets) > 0:
        for planet in enemy_planets:
            centre_enemy.x += planet.x
            centre_enemy.y += planet.y
        
        centre_enemy.x /= len(enemy_planets)
        centre_enemy.y /= len(enemy_planets)
    else:
        enemy_ships = game_map._all_ships()
        for my_ship in game_map.get_me().all_ships():
            enemy_ships.remove(my_ship)
        for ship in enemy_ships:
            centre_place.x += ship.x
            centre_place.y += ship.y
        
        centre_place.x /= len(enemy_ships)
        centre_place.y /= len(enemy_ships)
        
    logging.info("Enemy Centre.x: " + str(centre_enemy.x))
    logging.info("Enemy Centre.y: " + str(centre_enemy.y))
    
    # Now I list and categorize all ships by distance to the enemy
    
    
    my_ships = []
    my_active_ships = []
    enemy_ships = []
    
    ship_dict = game_map.nearby_ships_by_distance(centre_enemy)
    dist_list = sorted(ship_dict.keys())
    ship_list = []
    for dist in dist_list:
        ship_list.append(ship_dict.get(dist)[0])
    
    
    
    for ship in ship_list:
        if ship.owner == game_map.get_me():
            if ship.docking_status == 'DockingStatus.UNDOCKED':
                my_active_ships.append(ship)
            my_ships.append(ship)
            continue
        else:
            enemy_ships.append(ship)
        continue
    
    # Depending on the distribution I change the gamestate
    
    # Midgame (Gamestate 1) starts when there are less empty than occupied planets
    if (len(my_planets) + len(enemy_planets)) > len(empty_planets):
        #game_state = 1
    # Lategame (Gamestate 2) starts when there are no empty planets left
    elif (len(empty_planets) == 0):
        #game_state = 2
    '''
    
    # Rules for early game (state 0)
    if game_state == 0:
        active_ships = []
        active = False
        for ship in game_map.get_me().all_ships():
            if str(ship.docking_status) == 'DockingStatus.UNDOCKED':
                active_ships.append(ship)
                active = True
            continue
        
        logging.info("Listed active ships")
        logging.info("active ships: " + str(active_ships))
        
        '''mining_num = int(len(active_ships)*2/3)
        if mining_num < 2:
            mining_num = len(active_ships)
        war_num = len(active_ships) - mining_num
        
        war_ships = active_ships[mining_num:len(active_ships)]
        active_ships = active_ships[0:mining_num]'''
        
        if active:
            closest_ship = active_ships[0]
            
            # Navigate ships to not already filled planets
            ships_left = len(active_ships)
            targets = []
            
            for planet in my_planets_not_full:
                logging.info("Not filled Planet: " + str(planet))
                logging.info("Ships left: " + str(ships_left))
                logging.info("Docking spots: " + str(planet.num_docking_spots - len(planet.all_docked_ships())))
                
                targets.append(planet)
                if (ships_left <= planet.num_docking_spots - len(planet.all_docked_ships())):
                    break
                ships_left -= planet.num_docking_spots - len(planet.all_docked_ships())
                
            targets.reverse()
            logging.info("Not filled Targets" + str(targets))
            first_target = True
            for target in targets:
                docking_allowed = True
                logging.info("Current target: " + str(target) + " Docking spots: " + str(target.num_docking_spots))
                logging.info("range: " + str(target.num_docking_spots - len(target.all_docked_ships())))
                for places in range(target.num_docking_spots - len(target.all_docked_ships())):
                    if first_target and (places >= ships_left):
                        logging.info("Breaking at " + str(ships_left))
                        first_target = False
                        break
                    logging.info("searching for ship " + str(places))
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
                        if docking_allowed:
                            docking_allowed = False
                            logging.info("Nav command: " + str(closest_ship.dock(target)))
                            command_queue.append(closest_ship.dock(target))
                    # Otherwise move towards it
                    else:
                        navigate_command = closest_ship.navigate(closest_ship.closest_point_to(target), game_map, max_corrections=180, angular_step=5, speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                        logging.info("Nav command: " + str(navigate_command))
                        # If we can
                        if navigate_command:
                            command_queue.append(navigate_command)
                    if len(active_ships) < 1:
                        break
            
            logging.info("Navigated to not filled")
            
            # Navigate ships to empty planets
            ships_left = len(active_ships)
            targets = []
            
            for planet in empty_planets:
                logging.info("Not filled Planet: " + str(planet))
                logging.info("Ships left: " + str(ships_left))
                logging.info("Docking spots: " + str(planet.num_docking_spots))
                
                targets.append(planet)
                if (ships_left < planet.num_docking_spots):
                    break
                ships_left -= planet.num_docking_spots
            
            targets.reverse()
            logging.info("Empty Targets: " + str(targets))
            first_target = True
            for target in targets:
                docking_allowed = True
                logging.info("Current target: " + str(target) + " Docking spots: " + str(target.num_docking_spots))
                logging.info("range: " + str(target.num_docking_spots))
                for places in range(target.num_docking_spots):
                    if first_target and (places >= ships_left):
                        logging.info("Breaking at " + str(ships_left))
                        first_target = False
                        break
                    logging.info("searching for ship " + str(places))
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
                        if docking_allowed:
                            docking_allowed = False
                            logging.info("Nav command: " + str(closest_ship.dock(target)))
                            command_queue.append(closest_ship.dock(target))
                    # Otherwise move towards it
                    else:
                        navigate_command = closest_ship.navigate(closest_ship.closest_point_to(target), game_map, max_corrections=180, angular_step=5, speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                        logging.info("Nav command: " + str(navigate_command))
                        # If we can
                        if navigate_command:
                            command_queue.append(navigate_command)
                    if len(active_ships) < 1:
                        break
                
            logging.info("Navigated to empty")
            
            # Navigate ships to enemy planets
            '''active_ships = war_ships + active_ships'''
            
            if len(enemy_planets) >= 3:
                target_num = 3
            else:
                target_num = len(enemy_planets)
            targets = []
            if target_num > 0:
                targets = enemy_planets
                logging.info("Enemy Targets" + str(targets))
                
                while len(active_ships) > 0:
                    for n in range(target_num):
                        min_dist = 10000
                        if len(active_ships) > 0:
                            for ship in active_ships:
                                dist_to_tgt = ship.calculate_distance_between(targets[n])
                                if dist_to_tgt < min_dist:
                                    min_dist = dist_to_tgt
                                    closest_ship = ship
                            active_ships.remove(closest_ship)
                            target_ship = targets[n].all_docked_ships()[0]
                            navigate_command = closest_ship.navigate(closest_ship.closest_point_to(target_ship), game_map, max_corrections=180, angular_step=5, speed=int(hlt.constants.MAX_SPEED), ignore_ships=True)
                            logging.info("Nav command: " + str(navigate_command))
                            if navigate_command:
                                command_queue.append(navigate_command)
                        else:
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
