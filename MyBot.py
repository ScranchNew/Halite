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

from hlt.entity import Entity
from hlt.entity import Position
from hlt.entity import Ship

def closest_entity(entity, entity_list):
    """
    Determine the closest entity to the given entity in the list

    :param Entity entity: The entity you want to get the closest object to
    :return: The closest Entity
    :rtype: Entity
    """
    closest = None
    min_dist = 10000
    for ent in entity_list:
        dist = entity.calculate_distance_between(ent) < min_dist
        if dist < min_dist:
            closest = ent
            min_dist = dist
    return closest


# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Greedy")
# Then we print our start message to the logs
logging.info("Starting my Greedy bot!")

first_turn = True

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
        first_turn = False
    
    #logging.info("Centre.x: " + str(centre_place.x))
    #logging.info("Centre.y: " + str(centre_place.y))
    
    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    
    # Here I count and categorize all the planets in the game
    
    empty_planets = []
    my_planets = []
    my_planets_not_full = []
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
    
    # Find the centre of my empire
    centre_place.x = 0
    centre_place.y = 0
    
    for ship in game_map.get_me().all_ships():
        centre_place.x += ship.x
        centre_place.y += ship.y
    
    if len(my_planets) > 0:
        for planet in my_planets:
            centre_place.x += 2 * planet.x
            centre_place.y += 2 * planet.y
        
        centre_place.x /= 2 * len(my_planets) + len(game_map.get_me().all_ships())
        centre_place.y /= 2 * len(my_planets) + len(game_map.get_me().all_ships())
    else:
        centre_place.x /= len(game_map.get_me().all_ships())
        centre_place.y /= len(game_map.get_me().all_ships())
    
    entity_dict = game_map.nearby_entities_by_distance(centre_place)
    dist_list = sorted(entity_dict.keys())
    entity_list = []
    for dist in dist_list:
        entity_list.append(entity_dict.get(dist))
    
    logging.info("Entities by distance to Centre: " + str(entity_list))
    
    active_ships = []
    
    for ship in game_map.get_me().all_ships():
        if str(ship.docking_status) == 'DockingStatus.UNDOCKED':
            active_ships.append(ship)
    
    active_ship_num = len(active_ships)
    target_list = []
    
    logging.info("active_ship_num: " + str(active_ship_num))
    
    '''
    Now I add all usefull targets to the target_list
    '''
    
    for entity in entity_list:
        if active_ship_num > 0:
            if str(entity[0])[:11] == "Entity Ship":
                if entity[0].owner == game_map.get_me(): #Not my ships
                    continue
                elif entity[0].docking_status == 'DockingStatus.UNDOCKED':    #But enemy ships that are not docked
                    active_ship_num -= 2
                    target_list.append([entity[0], 2, "Enemy ship"])
                    continue
                else:
                    continue
            elif str(entity[0])[:13] == "Entity Planet":
                if entity[0].is_owned():
                    logging.info("entity[0].owner: " + str(entity[0].owner))
                    logging.info("game_map.get_me(): " + str(game_map.get_me()))
                    if entity[0].owner == game_map.get_me():
                        if entity[0].is_full():       #Not my full planets
                            continue
                        else:                         #But ones with open places
                            active_ship_num -= entity[0].num_docking_spots - len(entity[0].all_docked_ships())
                            target_list.append([entity[0], entity[0].num_docking_spots - len(entity[0].all_docked_ships()), "Planet"])
                            continue
                    else:                             #Also enemy planets
                        active_ship_num -= 3 * len(entity[0].all_docked_ships())
                        target_list.append([entity[0], 3 * len(entity[0].all_docked_ships()), "Enemy planet"])
                        continue
                else:                                 #And empty ones
                    active_ship_num -= entity[0].num_docking_spots
                    target_list.append([entity[0], entity[0].num_docking_spots, "Planet"])
                    continue
            else:
                continue
    
    logging.info("target_list:" + str(target_list))
    
    if len(target_list) > 0:
        target = target_list.pop()                        #The last target only gets limited ships
        docking_allowed = True
        for ship_num in range(target[1] + active_ship_num):
            ship = closest_entity(target[0], active_ships)
            logging.info("ship: " + str(ship))
            active_ships.remove(ship)
            if target[2] == "Planet":
                #If I can dock, I'll try to
                if ship.can_dock(target[0]) and docking_allowed:
                    docking_allowed = False
                    command_queue.append(ship.dock(target[0]))
                    continue
                #Otherwise move towards it
                else:
                    navigate_command = ship.navigate(ship.closest_point_to(target[0]), game_map, max_corrections=180, angular_step=5, speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                    if navigate_command:
                        command_queue.append(navigate_command)
                        continue
            elif target[2] == "Enemy ship":
                #Just fly towards enemy ships
                navigate_command = ship.navigate(ship.closest_point_to(target[0]), game_map, max_corrections=180, angular_step=5, speed=int(hlt.constants.MAX_SPEED), ignore_ships=True)
                if navigate_command:
                    command_queue.append(navigate_command)
                continue
            elif target[2] == "Enemy planet":
                #For planets fly to the closest base
                target_ship = closest_entity(ship, target[0].all_docked_ships())
                navigate_command = ship.navigate(ship.closest_point_to(target_ship), game_map, max_corrections=180, angular_step=5, speed=int(hlt.constants.MAX_SPEED), ignore_ships=True)
                if navigate_command:
                    command_queue.append(navigate_command)
                continue
            else:
                continue
                    
        for target in target_list:
            for ship_num in range(target[1]):
                ship = closest_entity(target[0], active_ships)
                active_ships.remove(ship)
                if target[2] == "Planet":
                    #If I can dock, I'll try to
                    if ship.can_dock(target[0]) and docking_allowed:
                        docking_allowed = False
                        command_queue.append(ship.dock(target[0]))
                        continue
                    #Otherwise move towards it
                    else:
                        navigate_command = ship.navigate(ship.closest_point_to(target[0]), game_map, max_corrections=180, angular_step=5, speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                        if navigate_command:
                            command_queue.append(navigate_command)
                            continue
                elif target[2] == "Enemy ship":
                    #Just fly towards enemy ships
                    navigate_command = ship.navigate(ship.closest_point_to(target[0]), game_map, max_corrections=180, angular_step=5, speed=int(hlt.constants.MAX_SPEED), ignore_ships=True)
                    if navigate_command:
                        command_queue.append(navigate_command)
                    continue
                elif target[2] == "Enemy planet":
                    #For planets fly to the closest base
                    target_ship = closest_entity(ship, target[0].all_docked_ships())
                    navigate_command = ship.navigate(ship.closest_point_to(target_ship), game_map, max_corrections=180, angular_step=5, speed=int(hlt.constants.MAX_SPEED), ignore_ships=True)
                    if navigate_command:
                        command_queue.append(navigate_command)
                    continue
                else:
                    continue
    
    game.send_command_queue(command_queue)
    
    logging.info("Command queue" + str(command_queue))
    logging.info(" ")
    
    # TURN END
# GAME END