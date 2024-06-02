from uuid import uuid4
import random
import math

acc_types = ["user", "admin"]

accounts = [
    {
        "_id": str(uuid4()),
        "first_name": "Alice",
        "last_name": "Johnson",
        "password": "Alic3@2023",
        "account_type": random.choice(acc_types),
        "email": "alice.johnson@example.com"
    },
    {
        "_id": str(uuid4()),
        "first_name": "Bob",
        "last_name": "Smith",
        "password": "Bob$mith1",
        "email": "bob.smith@example.com",
        "account_type": random.choice(acc_types)
    },
    {
        "_id": str(uuid4()),
        "first_name": "Carol",
        "last_name": "Williams",
        "password": "Carol@123",
        "account_type": random.choice(acc_types),
        "email": "carol.williams@example.com"
    },
    {
        "_id": str(uuid4()),
        "first_name": "David",
        "last_name": "Brown",
        "password": "D@vid2021",
        "account_type": random.choice(acc_types),
        "email": "david.brown@example.com"
    },
    {
        "_id": str(uuid4()),
        "first_name": "Eve",
        "last_name": "Davis",
        "password": "Ev3#Davis",
        "account_type": random.choice(acc_types),
        "email": "eve.davis@example.com"
    }
]

def format_name_for_file(name, extension):
    return name.lower().replace(' ', '_') + extension

# Data samples for Themes with specific Items
themes_samples = [
    {
        "_id": str(uuid4()),
        "name": "Animals",
        "description": "A collection of various animals.",
        "image": format_name_for_file("Animals", ".png"),
        "items": [
            {
                "id": str(uuid4()),
                "name": "Lion",
                "image": format_name_for_file("Lion", ".png"),
                "sound": format_name_for_file("Lion", ".mp3")
            },
            {
                "id": str(uuid4()),
                "name": "Elephant",
                "image": format_name_for_file("Elephant", ".png"),
                "sound": format_name_for_file("Elephant", ".mp3")
            },
            {
                "id": str(uuid4()),
                "name": "Monkey",
                "image": format_name_for_file("Monkey", ".png"),
                "sound": format_name_for_file("Monkey", ".mp3")
            }
        ],
        "background": format_name_for_file("Animals", ".jpg")
    },
    {
        "_id": str(uuid4()),
        "name": "Numbers",
        "description": "Learn about different numbers.",
        "image": format_name_for_file("Numbers", ".png"),
        "items": [
            {
                "id": str(uuid4()),
                "name": "One",
                "image": format_name_for_file("One", ".png"),
                "sound": format_name_for_file("One", ".mp3")
            },
            {
                "id": str(uuid4()),
                "name": "Two",
                "image": format_name_for_file("Two", ".png"),
                "sound": format_name_for_file("Two", ".mp3")
            },
            {
                "id": str(uuid4()),
                "name": "Three",
                "image": format_name_for_file("Three", ".png"),
                "sound": format_name_for_file("Three", ".mp3")
            }
        ],
        "background": format_name_for_file("Numbers", ".jpg")
    },
    {
        "_id": str(uuid4()),
        "name": "School supplies",
        "description": "Common items found in school.",
        "image": format_name_for_file("School supplies", ".png"),
        "items": [
            {
                "id": str(uuid4()),
                "name": "Pencil",
                "image": format_name_for_file("Pencil", ".png"),
                "sound": format_name_for_file("Pencil", ".mp3")
            },
            {
                "id": str(uuid4()),
                "name": "Notebook",
                "image": format_name_for_file("Notebook", ".png"),
                "sound": format_name_for_file("Notebook", ".mp3")
            },
            {
                "id": str(uuid4()),
                "name": "Eraser",
                "image": format_name_for_file("Eraser", ".png"),
                "sound": format_name_for_file("Eraser", ".mp3")
            }
        ],
        "background": format_name_for_file("School supplies", ".jpg")
    },
    {
        "_id": str(uuid4()),
        "name": "Classroom activities",
        "description": "Activities done in the classroom.",
        "image": format_name_for_file("Classroom activities", ".png"),
        "items": [
            {
                "id": str(uuid4()),
                "name": "Reading",
                "image": format_name_for_file("Reading", ".png"),
                "sound": format_name_for_file("Reading", ".mp3")
            },
            {
                "id": str(uuid4()),
                "name": "Writing",
                "image": format_name_for_file("Writing", ".png"),
                "sound": format_name_for_file("Writing", ".mp3")
            },
            {
                "id": str(uuid4()),
                "name": "Drawing",
                "image": format_name_for_file("Drawing", ".png"),
                "sound": format_name_for_file("Drawing", ".mp3")
            }
        ],
        "background": format_name_for_file("Classroom activities", ".jpg")
    },
    {
        "_id": str(uuid4()),
        "name": "Colors",
        "description": "Different colors to learn.",
        "image": format_name_for_file("Colors", ".png"),
        "items": [
            {
                "id": str(uuid4()),
                "name": "Red",
                "image": format_name_for_file("Red", ".png"),
                "sound": format_name_for_file("Red", ".mp3")
            },
            {
                "id": str(uuid4()),
                "name": "Blue",
                "image": format_name_for_file("Blue", ".png"),
                "sound": format_name_for_file("Blue", ".mp3")
            },
            {
                "id": str(uuid4()),
                "name": "Green",
                "image": format_name_for_file("Green", ".png"),
                "sound": format_name_for_file("Green", ".mp3")
            }
        ],
        "background": format_name_for_file("Colors", ".jpg")
    }
]

male_images = ["male_1.png", "male_2.png", "male_3.png"]
female_images = ["female_1.png", "female_2.png", "female_3.png"]

def create_score(theme: str):
    points = [random.random() * 100 for _ in range(3) ]
    points.sort()
    
    times = [10 + random.random() * 340 for _ in range(3)]
    times.sort()

    return {
        "points": {
            "min": points[0],
            "max": points[2],
            "current": points[1]
        },
        "time": {
            "min": times[0],
            "max": times[2],
            "current": times[1]
        },
        "theme": theme,
        "elements": random.randint(1, 20)
    }

def create_score_list():
    selected = random.sample(themes_samples, k=random.randint(1, len(themes_samples) - 1))
    themes = [theme["_id"] 
              for theme in selected]
    return [create_score(theme) for theme in themes]



achievements_keys = {
    "points": "Complete {theme} with at least {value} points",
    "min_time": "Complete {theme} in less than {value} seconds",
    "n_games": "Complete {theme} {value} times"

}

def create_achievement():
    key = random.choice(list(achievements_keys.keys()))
    theme = random.choice(themes_samples)
    return {
        "_id": str(uuid4()),
        "key": key,
        "value": random.randint(1, 100),
        "theme": theme["_id"],
        "description": achievements_keys[key].format(theme=theme["name"], value=random.randint(1, 100))
    }

achievements = [create_achievement() for _ in range(30)]

def get_achievements():
    max_n_achievements = math.floor(len(achievements) * 0.75)
    selected = random.sample(achievements, k=random.randint(1, max_n_achievements))
    return [achievement["_id"] for achievement in selected]

guests = [
    {
        "_id": str(uuid4()),
        "name": "John",
        "host": random.choice(accounts)["_id"],
        "image": random.choice(male_images),
        "scores": create_score_list(),
        "achievements": get_achievements()
    },
    {
        "_id": str(uuid4()),
        "name": "Emily",
        "host": random.choice(accounts)["_id"],
        "image": random.choice(female_images),
        "scores": create_score_list(),
        "achievements": get_achievements()
    },
    {
        "_id": str(uuid4()),
        "name": "Michael",
        "host": random.choice(accounts)["_id"],
        "image": random.choice(male_images),
        "scores": create_score_list(),
        "achievements": get_achievements()
    },
    {
        "_id": str(uuid4()),
        "name": "Sarah",
        "host": random.choice(accounts)["_id"],
        "image": random.choice(female_images),
        "scores": create_score_list(),
        "achievements": get_achievements()
    },
    {
        "_id": str(uuid4()),
        "name": "David",
        "host": random.choice(accounts)["_id"],
        "image": random.choice(male_images),
        "scores": create_score_list(),
        "achievements": get_achievements()
    }
]

data = {
    "accounts": accounts,
    "themes": themes_samples,
    "guests": guests,
    "achievements": achievements
}

def save():
    import json

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


save()