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
