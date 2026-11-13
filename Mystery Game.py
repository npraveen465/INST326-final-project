import random
import copy

def view_weapons_and_items(inventory):
    """ Displays the weapons and items the player is currently holding
    

    Args:
        inventory(dict): A dictionary holding item or weapon names as its key
        and quantity as its value

    Returns:
        Tuple: A tuple containing two dictionaries:
        
        weapon_damage (dict) = A dictionary that holds the weapon name, 
        the quantity of the weapon, and the weapon damage output.
        
        items_available (dict) = A dictionary that holds item name,
        quantity of the item, and the description of the item. 
    """
    weapon_damage= {}
    items_avaliable= {}
    
    weapon_stats = {
        "Great Sword": 50,
        "Dagger": 10,
        "Sword": 30,
        "Iron Mace": 40,
        "Axe": 20,
        "Throwing Knife": 10,
        "Slingshot": 20,
        "Bow":30,
        "Long Bow": 40,
        "Crossbow": 50    
    }
    
    item_description = {
        "Health Potion": "Restores 40 health points",
        "Lamp": "Can be used to explore dark rooms",
        "Strength Potion": "Gives an extra 20 damage for next attack",
        "Treasure Key": "Can be used to open chests",
        "Apple": "Restores 10 health points"
           
    }
    
    for item, quantity in inventory.items():
        
        if quantity <= 0:
            continue
        
        if item in weapon_stats:
            
            weapon_damage[item] = {
                "Quantity": quantity,
                "Damage": weapon_stats[item] 
            }
            
        elif item in item_description:
            items_avaliable[item] = {
                "Quantity": quantity,
                "Description": item_description[item]
            }
        
    return weapon_damage, items_avaliable

def simulate_boss_battle(boss_stats, player_stats, inventory):
    """Simulates a battle between the player and a specific boss looked up from the dictionary.

    Args:
        boss_stats (dict): Dictionary mapping boss names (str) to their attribute dictionaries 
                           (e.g., {'Corrupted Guard': {'health': 70, 'attack': 12}}).
        player_stats (dict): Dictionary containing player attributes (e.g., 'name', 'health', 'base_attack').
        inventory (list): A list of item/weapon strings currently held by the player.

    Side Effects:
        - Modifies the player's health in player_stats.
        - Modifies the selected boss's health inside boss_stats.
        - Removes used consumable items from the inventory list.
        - Prints the battle logs to keep track of who is winning.

    Returns:
        dict: A summary of the battle outcome, including 'boss_fought', 'winner', 
              'turns_taken', 'remaining_player_health', and 'remaining_boss_health'.
    """
    boss_name = current_room_boss
    
    if boss_name not in boss_stats:
        print(f"Error: Boss '{boss_name}' not found in database!")
        return None

    current_boss = boss_stats[boss_name]

    if current_boss["health"] <= 0:
        print(f"{boss_name} has already been defeated!")
        return None

    weapon_damage = {
        "Great Sword": 50, "Dagger": 10, "Sword": 30, "Iron Mace": 40,
        "Axe": 20, "Throwing Knife": 10, "Slingshot": 20, "Bow": 30,
        "Long Bow": 40, "Crossbow": 50
    }
    
    consumables = {
        "Health Potion": {"heal": 40, "buff": 0},
        "Apple": {"heal": 10, "buff": 0},
        "Strength Potion": {"heal": 0, "buff": 20}
    }

    turns = 0
    damage_buff = 0
    player_name = player_stats.get("name", "The Player")

    print(f"\n=== BATTLE START: {player_name} vs. {boss_name} ===")

    while player_stats["health"] > 0 and current_boss["health"] > 0:
        turns += 1
        print(f"\n--- Turn {turns} ---")
        print(f"{player_name} HP: {player_stats['health']} | {boss_name} HP: {current_boss['health']}")

        # --- PLAYER'S TURN ---
        action = input("Choose an action ([A]ttack or [U]se Item): ").strip().lower()

        if action == "u":
            usable_items = [item for item in inventory if item in consumables]
            if not usable_items:
                print("You have no usable items! You lose your turn fumbling through your bag.")
            else:
                print(f"Usable items: {', '.join(usable_items)}")
                chosen_item = input("Type the exact name of the item to use: ").strip()
                
                if chosen_item in usable_items:
                    effect = consumables[chosen_item]
                    if effect["heal"] > 0:
                        player_stats["health"] += effect["heal"]
                        print(f"Used {chosen_item}! Restored {effect['heal']} HP.")
                    if effect["buff"] > 0:
                        damage_buff += effect["buff"]
                        print(f"Used {chosen_item}! Next attack gains +{effect['buff']} damage.")
                    
                    inventory.remove(chosen_item)
                else:
                    print("Invalid item name. Turn wasted!")
        else:
            owned_weapons = [w for w in inventory if w in weapon_damage]
            if owned_weapons:
                best_weapon = max(owned_weapons, key=lambda w: weapon_damage[w])
                dmg = weapon_damage[best_weapon] + damage_buff
                weapon_used = best_weapon
            else:
                dmg = player_stats.get("base_attack", 5) + damage_buff
                weapon_used = "fists"

            damage_buff = 0 
            
            current_boss["health"] = max(0, current_boss["health"] - dmg)
            print(f"{player_name} attacks {boss_name} with {weapon_used} for {dmg} damage!")

        if current_boss["health"] <= 0:
            break

        boss_dmg = max(1, current_boss["attack"] + random.randint(-5, 5))
        player_stats["health"] = max(0, player_stats["health"] - boss_dmg)
        print(f"{boss_name} strikes back for {boss_dmg} damage!")

    winner = player_name if player_stats["health"] > 0 else boss_name
    print(f"\n=== BATTLE OVER: {winner} wins in {turns} turns! ===")

    return {
        "boss_fought": boss_name,
        "winner": winner,
        "turns_taken": turns,
        "remaining_player_health": player_stats["health"],
        "remaining_boss_health": current_boss["health"]
    }
    

def reset_endings(player_input, player, checkpoint, endings):
    """Handle resets and endings of the game. 

    Args:
        player_input(int): Player input for when they want to prematurely exit a scenario or option. 
        player_stats(dict): The player's current stats ('name', 'health', 'base_attack')
        inventory (list): The player's current inventory.
        boss_stats (dict): Boss names assigned to their attribute dictionaries. 
        checkpoint (dict): A saved place with the keys "player_stats", "inventory", and "boss_stats", taken before 
            an option or at the start of the game. 
        endings (dict): Assigns an ending name to its text. {"quit": "..."}.

    Side Effects:
        - Resets all player information back to the checkpoint.
        - Shows ending results.

    Returns:
        None

    Raises:
        ValueError: If player_input is not 1 or 2. 
    """

    if player_input == 1:
        player_stats.clear()
        player_stats.update(copy.deepcopy(checkpoint["player_stats"]))

        boss_stats.clear()
        boss_stats.update(copy.deepcopy(checkpoint["boss_stats"]))

        saved_inventory = copy.deepcopy(checkpoint["inventory"])
        if isinstance(inventory, list):
            inventory[:] = saved_inventory
        else:
            inventory.clear()
            inventory.update(saved_inventory)

        print(endings.get("reset", "Your progress has been reset."))

    elif player_input == 2:
        print(endings.get("quit", "You have left the adventure."))
        print(f"Health remaining: {player_stats.get('health', 0)}")
        print(f"Items held: {list(inventory)}")

    else: 
        raise ValueError("Invalid input. Enter 1 or 2!"
