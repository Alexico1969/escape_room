from database import get, store, update_user
from flask import session

def process(inp, inventory, room_data, rooms, level, objects):

    score = session['score']
    score -= 1
    session['score'] = score
    username = session['user']
    update_user(username, inventory, level, score)

    inp = inp.lower()
    inp = inp.replace('the ', ' ')
    inp = inp.replace(' a ', ' ')
    inp = inp.replace(' an ', ' ')

    door_status = session['door_status']

    try:

        if room_data.type == "end":
            return "This is the last level for now. More levels will be added soon. Thanks for playing !"

        if inp == "exit room" or inp == "exit" or inp == "leave room" or inp == "leave" or inp == "open door":
            
            if door_status == "locked":
                return "The door is locked"
            else:
                return "You exit the room"
        
        elif rooms[level].type ==  "computer":
            right_answer = rooms[level].expected_output
            if right_answer in inp:
                session["door_status"] = "unlocked"
                rooms[level].type = "code"
                return "You hear a clicking sound. The door unlocks."
            elif "close" in inp or "stop" in inp:
                rooms[level].type = "code"
                return "You close the computer"
            else:
                return "That's not the right answer"

        elif "computer" in inp and room_data.type == "code":
            words = inp.split(" ")
            if words[0] in ["open", "use", "type"]:
                rooms[level].type = "computer"
                return "You open the computer. It asks you for a code."
            else:
                return "What would you like to do with the computer?"

        elif inp == "help":
            return "Try things like: 'look around', 'look at table', 'unlock door', 'exit room'"
        
        elif inp == "look around" or inp == "look room":

            things = room_data.furniture.split(",")
            print(f"--->  things: {things}")
            if len(things) == 1:
                return f"You look around and you see a {things[0]}"
            else:
                temp = f"You look around and you see a {things[0]}"
                things.pop(0)
                for i in things:
                    temp += f", a {i}"
            return temp
        
        elif "look" in inp:
            if "at" in inp:
                thing = inp.split("at ")[1]
                thing = thing.replace(' ', '')
                if thing in room_data.furniture:
                    if objects[thing] != "":
                        detail = objects[thing]
                        detail = detail.replace('<', '')
                        detail = detail.replace('>', '')
                        return f"You look at the {thing} and you see a {detail}"
                    else:
                        return f"You look at the {thing} and you see nothing special"
                elif thing in objects.values() or "<" + thing + ">" in objects.values():
                        return f"You look at the {thing} and you see nothing special"
                else:
                    return f"You don't see a {thing} in the room"
                
        elif "take" in inp or "get" in inp:
            if "take" in inp:
                thing = inp.split("take ")[1]
            else:
                thing = inp.split("get ")[1]
            thing = thing.replace(' ', '')
            if thing in objects.values() or "<" + thing + ">" in objects.values():
                if "<" + thing + ">" in objects.values():
                    return f"You can't take the {thing}"
                else:
                    for key, value in objects.items():
                        if value == thing:
                            username, score, level, inventory, objects, door_status = get()
                            inventory.append(thing)
                            objects[key] = ""
                            store(username, score, level, inventory, objects)
                            return f"You take the {thing}"
                
            else:
                return f"You don't see a {thing} in the room"

        
        elif "unlock" in inp:
            if room_data.type == "inventory":
                thing = inp.split("unlock ")[1]
                thing = thing.split(" ")[0]
                thing = thing.replace(' ', '')
                if thing == "door":
                    if "key" in inventory:
                        session['door_status'] = "unlocked"
                        return f"You unlock the door"
                    else:
                        return f"You don't have a key"
                    
                else:
                    return f"You don't see a {thing} in the room"
            else:
                return "It's not that kind of lock"

        if "walk" in inp or "run" in inp or "jump "in inp:
            return "Ah.. that felt good !"

        if level == 14:
            if 'listen' in inp and 'door' in inp:
                return "You hear a faint noise of a person breathing behind the door"
            if 'listen' in inp:
                return "You hear a faint noise coming from the door"
            if 'talk' in inp:
                if 'person' in inp:
                    return "You talk to the person behind the door. They ask you to give them something. Anything."
                else:
                    return "Are you talking to yourself?"
            if 'push' in inp:
                if 'key' in inp:
                    if 'key' in inventory:
                        session["door_status"] = "unlocked"
                        inventory.remove('key')
                        update_user(username, inventory, level, score)
                        store(username, score, level, inventory, objects)
                        return "You push the key under the door. You hear the person behind the door pick it up. They unlock the door for you !"
                    else:
                        return "You don't have a key"
            if 'give' in inp:
                return "How? The door is locked."


        if "listen" in inp:
            return "You hear nothing special"

        words = inp.split(" ")
        bad_words = ["hit","break","smash","kick"]

        for word in words:
            if word in bad_words:
                return "That's a bit aggressive... :-)"

    
        return "I'm not sure what you mean by that."
    except:
        return "Really? Ahhh. no. Try something else."