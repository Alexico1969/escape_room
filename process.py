def process(inp, inventory, room_data):
    inp = inp.lower()

    if inp == "help":
        return "Try things like: 'look around', 'look at table', 'take key', 'use key', 'open door'"
    elif inp == "look around":
        things = room_data.furniture.split(",")
        if len(things) == 1:
            return f"You look around and you see a {things[0]}"
        else:
            temp = f"You look around and you see a {things[0]} "
            things.pop(0)
            for i in things:
                temp += f"and a {i}"
        return temp
    
    return "I'm not sure what you mean by that."