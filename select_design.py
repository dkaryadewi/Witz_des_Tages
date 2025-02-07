import json
import random

# ----------------- Load JSON data ----------------- 
def load_designs(file_path="./design.json"):
    with open(file_path, "r") as file:
        return json.load(file)

# ----------------- Check if today's date falls within any range ----------------- 
def find_design(datum, designs):
    today_str = datum.strftime("%m-%d")

    for design in designs:
        if design["from"] and design["until"]:
            if design["from"] <= today_str <= design["until"]:
                return design["designNr"]

    random_choices = [d["designNr"] for d in designs if not d["from"] and not d["until"]]
    
    if random_choices:
        return random.choice(random_choices)

    return None

# ----------------- Run all of the functions ----------------- 
def pick_design(mydate):
    designs = load_designs("./design.json")
    
    selected_design = find_design(mydate, designs)
    print(mydate)
    print(f"Selected Design: {selected_design}")
    return selected_design
