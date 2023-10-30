def process(inp, inventory, room_data, room, level):

    
    inp = inp.lower()
    inp = inp.replace('the ', ' ')
    inp = inp.replace(' a ', ' ')

    print("===============")
    print()
    print(f"level: {level}")
    dl1 = room_data.door_locked
    print(f"door_locked: {dl1}")
    print()
    print(f"room: {room}")
    print()
    print("===============")

    if inp == "exit room" or inp == "exit" or inp == "leave room" or inp == "leave" or inp == "open door":
        if room_data.door_locked:
            return "The door is locked"
        else:
            return "You exit the room"
    
    elif room[level].type ==  "computer":
        right_answer = room[level].expected_output
        if inp == right_answer:
            room[level].door_locked = False
            return "You hear a clicking sound. The door unlocks."
        else:
            return "That's not the right answer"

    elif "computer" in inp and room_data.type == "code":
        words = inp.split(" ")
        if words[0] in ["open", "use", "type"]:
            room[level].type = "computer"
            return "You open the computer. It asks you for a code."
        else:
            return "What would you like to do with the computer?"

    elif inp == "help":
        return "Try things like: 'look around', 'look at table', 'unlock door', 'exit room'"
    
    elif inp == "look around" or inp == "look room":
        things = room_data.furniture.split(",")
        if len(things) == 1:
            return f"You look around and you see a {things[0]}"
        else:
            temp = f"You look around and you see a {things[0]} "
            things.pop(0)
            for i in things:
                temp += f"and a {i} "
        return temp
    
    elif "look" in inp:
        if "at" in inp:
            thing = inp.split("at ")[1]
            thing = thing.replace(' ', '')
            if thing in room_data.furniture:
                if room_data.objects[thing] != "":
                    detail = room_data.objects[thing]
                    detail = detail.replace('<', '')
                    detail = detail.replace('>', '')
                    return f"You look at the {thing} and you see a {detail}"
                else:
                    return f"You look at the {thing} and you see nothing special"
            elif thing in room_data.objects.values() or "<" + thing + ">" in room_data.objects.values():
                    return f"You look at the {thing} and you see nothing special"
            else:
                return f"You don't see a {thing} in the room"
            
    elif "take" in inp:
        thing = inp.split("take ")[1]
        thing = thing.replace(' ', '')
        #print("User command: ", inp)
        #print("Thing: ", thing)
        #print("room_data.objects: ", room_data.objects)
        if thing in room_data.objects.values() or "<" + thing + ">" in room_data.objects.values():
            if thing[0] == "<":
                return f"You can't take the {thing}"
            else:
                for key, value in room_data.objects.items():
                    if value == thing:
                        inventory.append(thing)
                        room_data.objects[key] = ""
                        return f"You take the {thing}"
            
        else:
            return f"You don't see a {thing} in the room"
        
    elif "get" in inp:
        thing = inp.split("get ")[1]
        thing = thing.replace(' ', '')
        #print("User command: ", inp)
        #print("Thing: ", thing)
        #print("room_data.objects: ", room_data.objects)
        if thing in room_data.objects.values() or "<" + thing + ">" in room_data.objects.values():
            if thing[0] == "<":
                return f"You can't take the {thing}"
            else:
                thing = thing.replace('<', '')
                thing = thing.replace('>', '')
                for key, value in room_data.objects.items():
                    if value == thing:
                        inventory.append(thing)
                        room_data.objects[key] = ""
                        return f"You take the {thing}"
           
        else:
            return f"You don't see a {thing} in the room"
    
    elif "unlock" in inp:
        if room_data.type == "inventory":
            thing = inp.split("unlock ")[1]
            thing = thing.replace(' ', '')
            if thing == "door":
                if "key" in inventory:
                    room_data.door_locked = False
                    return f"You unlock the door"
                else:
                    return f"You don't have a key"
                
            else:
                return f"You don't see a {thing} in the room"
        else:
            return "It's not that kind of lock"

    if "walk" in inp or "run" in inp or "jump "in inp:
        return "Ah.. that felt good !"

    words = inp.split(" ")
    bad_words = ["hit","break","smash","kick"]

    for word in words:
        if word in bad_words:
            return "That's a bit aggressive... :-)"

    
    return "I'm not sure what you mean by that."