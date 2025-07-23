import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
class Pet:
    def __init__(self, name, species="Generic"):
        self.name = name
        self.species = species
        self.birth_time = datetime.now()
        self.last_interaction = datetime.now()
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.health = 100
        self.level = 1
        self.experience = 0
        self.total_interactions = 0
        self.interactions_today = 0
        self.last_fed = None
        self.last_played = None
        self.mood = "neutral"
        self.evolution_stage = "baby"
        self.evolution_points = 0
    def get_age(self):
        delta = datetime.now() - self.birth_time
        days = delta.days
        hours = delta.seconds // 3600
        if days == 0:
            return f"{hours} hours old"
        elif days == 1:
            return "1 day old"
        else:
            return f"{days} days old"
    def calculate_mood(self):
        score = (
            self.happiness * 0.4 +
            self.health * 0.3 +
            self.energy * 0.2 +
            (100 - self.hunger) * 0.1
        )
        if score >= 80:
            moods = ["ecstatic", "joyful", "content", "elated"]
        elif score >= 60:
            moods = ["happy", "cheerful", "playful", "satisfied"]
        elif score >= 40:
            moods = ["neutral", "calm", "okay", "decent"]
        elif score >= 20:
            moods = ["sad", "tired", "grumpy", "restless"]
        else:
            moods = ["depressed", "miserable", "sick", "angry"]
        random.seed(int(time.time() // 300))
        self.mood = random.choice(moods)
        return self.mood
    def feed(self, food_type="kibble"):
        if self.hunger <= 10:
            return {
                "success": False,
                "message": f"{self.name} is too full to eat right now!",
                "response": "Pushes food away"
            }
        effects = {
            "kibble": {"hunger": -20, "happiness": 5, "msg": "crunches happily"},
            "treat": {"hunger": -10, "happiness": 15, "msg": "wags tail excitedly"},
            "vegetable": {"hunger": -15, "happiness": 2, "health": 5, "msg": "chews reluctantly"},
            "meat": {"hunger": -25, "happiness": 10, "energy": 5, "msg": "devours greedily"},
            "fish": {"hunger": -20, "happiness": 12, "health": 3, "msg": "purrs with satisfaction"}
        }
        effect = effects.get(food_type, effects["kibble"])
        self.hunger = max(0, self.hunger + effect["hunger"])
        self.happiness = min(100, self.happiness + effect["happiness"])
        if "health" in effect:
            self.health = min(100, self.health + effect["health"])
        if "energy" in effect:
            self.energy = min(100, self.energy + effect["energy"])
        self.last_fed = datetime.now()
        self._update_interaction()
        return {
            "success": True,
            "message": f"{self.name} {effect['msg']}!",
            "response": self._get_food_response(food_type)
        }
    def play(self, activity="fetch"):
        if self.energy <= 10:
            return {
                "success": False,
                "message": f"{self.name} is too tired to play right now.",
                "response": "Yawns and lies down"
            }
        if self.hunger >= 80:
            return {
                "success": False,
                "message": f"{self.name} is too hungry to play. Feed them first!",
                "response": "Looks at empty food bowl"
            }
        activities = {
            "fetch": {"happiness": 15, "energy": -20, "msg": "runs around joyfully"},
            "tug": {"happiness": 12, "energy": -15, "msg": "pulls with determination"},
            "puzzle": {"happiness": 10, "energy": -10, "experience": 3, "msg": "thinks hard"},
            "cuddle": {"happiness": 20, "energy": -5, "msg": "snuggles contentedly"},
            "training": {"happiness": 8, "energy": -25, "experience": 5, "msg": "learns eagerly"}
        }
        effect = activities.get(activity, activities["fetch"])
        self.happiness = min(100, self.happiness + effect["happiness"])
        self.energy = max(0, self.energy + effect["energy"])
        if "experience" in effect:
            self.experience += effect["experience"]
        self.last_played = datetime.now()
        self._update_interaction()
        return {
            "success": True,
            "message": f"{self.name} {effect['msg']}!",
            "response": self._get_play_response(activity)
        }
    def rest(self):
        if self.energy >= 90:
            return {
                "success": False,
                "message": f"{self.name} is too energetic to rest right now!",
                "response": "Bounces around excitedly"
            }
        energy_gain = random.randint(20, 35)
        self.energy = min(100, self.energy + energy_gain)
        self.hunger = min(100, self.hunger + 5)  
        self._update_interaction()
        return {
            "success": True,
            "message": f"{self.name} takes a peaceful nap and feels refreshed!",
            "response": "Curls up and sleeps peacefully"
        }
    def get_status(self):
        mood = self.calculate_mood()
        time_since = self._time_since_last_interaction()
        return {
            "name": self.name,
            "species": self.species,
            "age": self.get_age(),
            "level": self.level,
            "mood": mood,
            "stats": {
                "hunger": self.hunger,
                "happiness": self.happiness,
                "energy": self.energy,
                "health": self.health
            },
            "experience": self.experience,
            "interactions_today": self.interactions_today,
            "total_interactions": self.total_interactions,
            "time_since_last_interaction": time_since,
            "last_fed": self._format_time(self.last_fed) if self.last_fed else "Never",
            "last_played": self._format_time(self.last_played) if self.last_played else "Never"
        }
    def update_passive_stats(self):
        now = datetime.now()
        hours_passed = (now - self.last_interaction).total_seconds() / 3600
        if hours_passed > 0:
            hunger_increase = min(hours_passed * 2, 20)
            self.hunger = min(100, self.hunger + hunger_increase)
            if hours_passed > 2:
                happiness_decrease = min((hours_passed - 2) * 1.5, 15)
                self.happiness = max(0, self.happiness - happiness_decrease)
            if self.energy < 80:
                energy_increase = min(hours_passed * 0.5, 10)
                self.energy = min(100, self.energy + energy_increase)
            if self.hunger > 80 or self.happiness < 20:
                health_decrease = min(hours_passed * 0.3, 5)
                self.health = max(0, self.health - health_decrease)
    def level_up_check(self):
        required_exp = self.level * 100
        if self.experience >= required_exp:
            self.level += 1
            self.experience -= required_exp
            return True
        return False
    def _update_interaction(self):
        self.last_interaction = datetime.now()
        self.interactions_today += 1
        self.total_interactions += 1
        self.experience += 5
    def _get_food_response(self, food_type):
        responses = {
            "kibble": ["*crunch crunch*", "*nom nom*", "*munch munch*"],
            "treat": ["*excited wagging*", "*happy yips*", "*bounces with joy*"],
            "vegetable": ["*chews slowly*", "*sighs*", "*eats reluctantly*"],
            "meat": ["*growls happily*", "*devours quickly*", "*licks lips*"],
            "fish": ["*purrs*", "*savors taste*", "*meows appreciation*"]
        }
        return random.choice(responses.get(food_type, responses["kibble"]))
    def _get_play_response(self, activity):
        responses = {
            "fetch": ["*runs excitedly*", "*brings back toy*", "*pants happily*"],
            "tug": ["*growls playfully*", "*pulls hard*", "*shakes toy*"],
            "puzzle": ["*tilts head*", "*paws at puzzle*", "*looks proud*"],
            "cuddle": ["*purrs softly*", "*nuzzles close*", "*relaxes*"],
            "training": ["*sits attentively*", "*performs trick*", "*wags tail*"]
        }
        return random.choice(responses.get(activity, responses["fetch"]))
    def _time_since_last_interaction(self):
        if not self.last_interaction:
            return "Unknown"
        delta = datetime.now() - self.last_interaction
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return f"{seconds} seconds ago"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = seconds // 86400
            return f"{days} day{'s' if days != 1 else ''} ago"
    def _format_time(self, time_obj):
        if not time_obj:
            return "Never"
        return time_obj.strftime("%Y-%m-%d %H:%M:%S")
    def to_dict(self):
        return {
            "name": self.name,
            "species": self.species,
            "birth_time": self.birth_time.isoformat(),
            "last_interaction": self.last_interaction.isoformat(),
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "health": self.health,
            "level": self.level,
            "experience": self.experience,
            "interactions_today": self.interactions_today,
            "total_interactions": self.total_interactions,
            "last_fed": self.last_fed.isoformat() if self.last_fed else None,
            "last_played": self.last_played.isoformat() if self.last_played else None,
            "mood": self.mood,
            "evolution_stage": self.evolution_stage,
            "evolution_points": self.evolution_points
        }
    @classmethod
    def from_dict(cls, data):
        pet = cls(data["name"], data.get("species", "Generic"))
        pet.birth_time = datetime.fromisoformat(data["birth_time"])
        pet.last_interaction = datetime.fromisoformat(data["last_interaction"])
        pet.hunger = data["hunger"]
        pet.happiness = data["happiness"]
        pet.energy = data["energy"]
        pet.health = data["health"]
        pet.level = data["level"]
        pet.experience = data["experience"]
        pet.interactions_today = data.get("interactions_today", 0)
        pet.total_interactions = data.get("total_interactions", 0)
        pet.last_fed = datetime.fromisoformat(data["last_fed"]) if data.get("last_fed") else None
        pet.last_played = datetime.fromisoformat(data["last_played"]) if data.get("last_played") else None
        pet.mood = data.get("mood", "neutral")
        pet.evolution_stage = data.get("evolution_stage", "baby")
        pet.evolution_points = data.get("evolution_points", 0)
        return pet