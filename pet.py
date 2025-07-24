import json
import time
import random
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
class PersonalityTrait:
    def __init__(self, name, base_strength=50, min_val=0, max_val=100):
        self.name = name
        self.strength = base_strength
        self.min_val = min_val
        self.max_val = max_val
        self.development_history = []
        self.last_changed = datetime.now()
    def modify(self, change_amount, reason=""):
        old_strength = self.strength
        self.strength = max(self.min_val, min(self.max_val, self.strength + change_amount))
        if self.strength != old_strength:
            self.development_history.append({
                "timestamp": datetime.now(),
                "old_value": old_strength,
                "new_value": self.strength,
                "change": change_amount,
                "reason": reason
            })
            self.last_changed = datetime.now()
    def get_level(self):
        if self.strength >= 80:
            return "very high"
        elif self.strength >= 60:
            return "high"
        elif self.strength >= 40:
            return "moderate"
        elif self.strength >= 20:
            return "low"
        else:
            return "very low"
class PetMemory:
    def __init__(self, max_memories=100):
        self.max_memories = max_memories
        self.experiences = []
        self.behavior_patterns = {}
        self.preferences = {}
        self.time_patterns = {}
    def add_experience(self, experience_type, details, emotional_impact=0):
        experience = {
            "timestamp": datetime.now(),
            "type": experience_type,
            "details": details,
            "emotional_impact": emotional_impact,
            "context": self._get_current_context()
        }
        self.experiences.append(experience)
        if len(self.experiences) > self.max_memories:
            self.experiences = self.experiences[-self.max_memories:]
        self._update_patterns(experience)
    def _get_current_context(self):
        now = datetime.now()
        return {
            "hour": now.hour,
            "day_of_week": now.weekday(),
            "month": now.month,
            "season": self._get_season(now.month)
        }
    def _get_season(self, month):
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "autumn"
    def _update_patterns(self, experience):
        exp_type = experience["type"]
        context = experience["context"]
        if exp_type not in self.behavior_patterns:
            self.behavior_patterns[exp_type] = {"count": 0, "contexts": []}
        self.behavior_patterns[exp_type]["count"] += 1
        self.behavior_patterns[exp_type]["contexts"].append(context)
        hour = context["hour"]
        if hour not in self.time_patterns:
            self.time_patterns[hour] = {}
        if exp_type not in self.time_patterns[hour]:
            self.time_patterns[hour][exp_type] = 0
        self.time_patterns[hour][exp_type] += 1
    def get_preferred_activity_time(self, activity_type):
        best_hour = 12  
        max_count = 0
        for hour, activities in self.time_patterns.items():
            count = activities.get(activity_type, 0)
            if count > max_count:
                max_count = count
                best_hour = hour
        return best_hour
    def get_experience_count(self, experience_type):
        return self.behavior_patterns.get(experience_type, {}).get("count", 0)
class EnvironmentSensor:
    @staticmethod
    def get_entropy_seed():
        import os
        import time
        entropy_data = f"{time.time()}{os.getpid()}{random.random()}"
        return int(hashlib.md5(entropy_data.encode()).hexdigest()[:8], 16)
    @staticmethod
    def get_time_of_day_modifier():
        hour = datetime.now().hour
        if 6 <= hour < 10:  
            return {"energy": 1.1, "happiness": 1.0, "activity_preference": "training"}
        elif 10 <= hour < 14:  
            return {"energy": 1.0, "happiness": 1.1, "activity_preference": "fetch"}
        elif 14 <= hour < 18:  
            return {"energy": 0.9, "happiness": 1.0, "activity_preference": "puzzle"}
        elif 18 <= hour < 22:  
            return {"energy": 0.8, "happiness": 1.1, "activity_preference": "cuddle"}
        else:  
            return {"energy": 0.6, "happiness": 0.9, "activity_preference": "rest"}
    @staticmethod
    def get_seasonal_modifier():
        month = datetime.now().month
        season = EnvironmentSensor._get_season(month)
        modifiers = {
            "spring": {"happiness": 1.2, "energy": 1.1, "health": 1.05},
            "summer": {"happiness": 1.1, "energy": 1.2, "health": 1.0},
            "autumn": {"happiness": 0.9, "energy": 1.0, "health": 1.1},
            "winter": {"happiness": 0.8, "energy": 0.9, "health": 0.95}
        }
        return modifiers.get(season, {"happiness": 1.0, "energy": 1.0, "health": 1.0})
    @staticmethod
    def _get_season(month):
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "autumn"
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
        self.personality_traits = self._initialize_personality()
        self.memory = PetMemory()
        self.behavioral_adaptations = {}
        self.environmental_sensitivity = random.uniform(0.5, 1.5)
        self.mood = "neutral"
        self.evolution_stage = "baby"
        self.evolution_points = 0
        self.current_entropy_seed = EnvironmentSensor.get_entropy_seed()
        self.interaction_frequency_history = []
        self.favorite_activities = {}
        self.preferred_foods = {}
        self.circadian_preferences = self._initialize_circadian_rhythm()
        self.seasonal_adaptations = {}
    def _initialize_personality(self):
        base_traits = {
            "curiosity": random.randint(30, 70),
            "loyalty": random.randint(40, 80),
            "mischief": random.randint(20, 60),
            "independence": random.randint(25, 75),
            "sociability": random.randint(35, 85),
            "intelligence": random.randint(30, 70),
            "playfulness": random.randint(40, 90),
            "calmness": random.randint(20, 80)
        }
        traits = {}
        for name, strength in base_traits.items():
            traits[name] = PersonalityTrait(name, strength)
        return traits
    def _initialize_circadian_rhythm(self):
        return {
            "morning_energy": random.uniform(0.8, 1.2),
            "afternoon_playfulness": random.uniform(0.9, 1.3),
            "evening_sociability": random.uniform(0.7, 1.1),
            "night_restfulness": random.uniform(1.0, 1.5)
        }
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
        base_score = (
            self.happiness * 0.4 +
            self.health * 0.3 +
            self.energy * 0.2 +
            (100 - self.hunger) * 0.1
        )
        personality_modifier = 1.0
        if hasattr(self, 'personality_traits'):
            if self.personality_traits.get("calmness"):
                calmness = self.personality_traits["calmness"].strength / 100
                personality_modifier += (calmness - 0.5) * 0.2
            if self.personality_traits.get("sociability"):
                sociability = self.personality_traits["sociability"].strength / 100
                hours_since_interaction = (datetime.now() - self.last_interaction).total_seconds() / 3600
                if hours_since_interaction > 2:
                    personality_modifier -= sociability * 0.1
        env_modifier = 1.0
        if hasattr(self, 'environmental_sensitivity'):
            time_mod = EnvironmentSensor.get_time_of_day_modifier()
            seasonal_mod = EnvironmentSensor.get_seasonal_modifier()
            env_modifier *= time_mod.get("happiness", 1.0) * self.environmental_sensitivity * 0.3
            env_modifier *= seasonal_mod.get("happiness", 1.0) * self.environmental_sensitivity * 0.2
            env_modifier = max(0.5, min(1.5, env_modifier))
        final_score = base_score * personality_modifier * env_modifier
        if hasattr(self, 'current_entropy_seed'):
            random.seed(self.current_entropy_seed + int(time.time() // 600))  
            entropy_variation = random.uniform(-5, 5)
            final_score += entropy_variation
        if final_score >= 90:
            moods = ["blissful", "euphoric", "radiant", "transcendent"]
        elif final_score >= 80:
            moods = ["ecstatic", "joyful", "elated", "exuberant"]
        elif final_score >= 70:
            moods = ["happy", "cheerful", "upbeat", "content"]
        elif final_score >= 60:
            moods = ["pleased", "satisfied", "positive", "good"]
        elif final_score >= 50:
            moods = ["neutral", "calm", "steady", "balanced"]
        elif final_score >= 40:
            moods = ["subdued", "quiet", "pensive", "reflective"]
        elif final_score >= 30:
            moods = ["sad", "melancholy", "downcast", "blue"]
        elif final_score >= 20:
            moods = ["distressed", "troubled", "upset", "worried"]
        elif final_score >= 10:
            moods = ["miserable", "dejected", "despondent", "anguished"]
        else:
            moods = ["devastated", "broken", "hopeless", "despairing"]
        random.seed(int(time.time() // 300) + hash(self.name))
        self.mood = random.choice(moods)
        return self.mood
    def feed(self, food_type="kibble"):
        if self.hunger <= 10:
            return {
                "success": False,
                "message": f"{self.name} is too full to eat right now!",
                "response": self._get_personality_based_response("too_full", food_type)
            }
        base_effects = {
            "kibble": {"hunger": -20, "happiness": 5, "msg": "crunches steadily"},
            "treat": {"hunger": -10, "happiness": 15, "msg": "devours excitedly"},
            "vegetable": {"hunger": -15, "happiness": 2, "health": 5, "msg": "nibbles carefully"},
            "meat": {"hunger": -25, "happiness": 10, "energy": 5, "msg": "tears into hungrily"},
            "fish": {"hunger": -20, "happiness": 12, "health": 3, "msg": "savors delicately"}
        }
        effect = base_effects.get(food_type, base_effects["kibble"])
        if hasattr(self, 'personality_traits'):
            if food_type != "kibble" and self.personality_traits.get("curiosity"):
                curiosity_bonus = (self.personality_traits["curiosity"].strength / 100) * 5
                effect["happiness"] += curiosity_bonus
            if self.personality_traits.get("intelligence"):
                self._update_food_preference(food_type, effect.get("happiness", 0))
        env_modifiers = EnvironmentSensor.get_time_of_day_modifier()
        seasonal_modifiers = EnvironmentSensor.get_seasonal_modifier()
        hunger_change = effect["hunger"]
        happiness_change = effect["happiness"] * env_modifiers.get("happiness", 1.0)
        self.hunger = max(0, self.hunger + hunger_change)
        self.happiness = min(100, self.happiness + happiness_change)
        if "health" in effect:
            health_change = effect["health"] * seasonal_modifiers.get("health", 1.0)
            self.health = min(100, self.health + health_change)
        if "energy" in effect:
            energy_change = effect["energy"] * env_modifiers.get("energy", 1.0)
            self.energy = min(100, self.energy + energy_change)
        if hasattr(self, 'memory'):
            emotional_impact = happiness_change / 10  
            self.memory.add_experience("feeding", {
                "food_type": food_type,
                "satisfaction": happiness_change,
                "hunger_before": self.hunger - hunger_change
            }, emotional_impact)
        self.last_fed = datetime.now()
        self._update_interaction()
        self._adapt_personality_from_feeding(food_type, happiness_change)
        return {
            "success": True,
            "message": f"{self.name} {effect['msg']}!",
            "response": self._get_advanced_response("feeding", food_type, happiness_change)
        }
    def play(self, activity="fetch"):
        if self.energy <= 10:
            return {
                "success": False,
                "message": f"{self.name} is too tired to play right now.",
                "response": self._get_personality_based_response("too_tired", activity)
            }
        if self.hunger >= 80:
            return {
                "success": False,
                "message": f"{self.name} is too hungry to play. Feed them first!",
                "response": self._get_personality_based_response("too_hungry", activity)
            }
        base_activities = {
            "fetch": {"happiness": 15, "energy": -20, "msg": "bounds joyfully"},
            "tug": {"happiness": 12, "energy": -15, "msg": "tugs determinedly"},
            "puzzle": {"happiness": 10, "energy": -10, "experience": 3, "msg": "concentrates intently"},
            "cuddle": {"happiness": 20, "energy": -5, "msg": "snuggles warmly"},
            "training": {"happiness": 8, "energy": -25, "experience": 5, "msg": "focuses eagerly"}
        }
        effect = base_activities.get(activity, base_activities["fetch"])
        if hasattr(self, 'personality_traits'):
            if self.personality_traits.get("playfulness"):
                playfulness_bonus = (self.personality_traits["playfulness"].strength / 100) * 5
                effect["happiness"] += playfulness_bonus
            if activity in ["puzzle", "training"] and self.personality_traits.get("intelligence"):
                intelligence_bonus = (self.personality_traits["intelligence"].strength / 100) * 3
                effect["experience"] = effect.get("experience", 0) + intelligence_bonus
            if self.personality_traits.get("independence"):
                independence = self.personality_traits["independence"].strength / 100
                if activity == "cuddle":
                    effect["happiness"] *= (1 - independence * 0.3)
                elif activity in ["fetch", "puzzle"]:
                    effect["happiness"] *= (1 + independence * 0.2)
        env_modifiers = EnvironmentSensor.get_time_of_day_modifier()
        preferred_activity = env_modifiers.get("activity_preference", "fetch")
        if activity == preferred_activity:
            effect["happiness"] *= 1.2  
        happiness_change = effect["happiness"]
        energy_change = effect["energy"]
        self.happiness = min(100, self.happiness + happiness_change)
        self.energy = max(0, self.energy + energy_change)
        if "experience" in effect:
            self.experience += effect["experience"]
        if hasattr(self, 'memory'):
            emotional_impact = happiness_change / 10
            self.memory.add_experience("playing", {
                "activity": activity,
                "enjoyment": happiness_change,
                "energy_before": self.energy - energy_change
            }, emotional_impact)
        self._update_activity_preference(activity, happiness_change)
        self.last_played = datetime.now()
        self._update_interaction()
        self._adapt_personality_from_playing(activity, happiness_change)
        return {
            "success": True,
            "message": f"{self.name} {effect['msg']}!",
            "response": self._get_advanced_response("playing", activity, happiness_change)
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
        status = {
            "name": self.name,
            "species": self.species,
            "age": self.get_age(),
            "level": self.level,
            "mood": mood,
            "evolution_stage": getattr(self, 'evolution_stage', 'baby'),
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
        if hasattr(self, 'personality_traits'):
            status["personality"] = self.get_personality_summary()
        if hasattr(self, 'memory'):
            status["behavioral_insights"] = self.get_behavioral_insights()
            status["total_memories"] = len(self.memory.experiences)
        if hasattr(self, 'environmental_sensitivity'):
            status["environmental_sensitivity"] = round(self.environmental_sensitivity, 2)
        env_context = EnvironmentSensor.get_time_of_day_modifier()
        status["current_time_preference"] = env_context.get("activity_preference", "none")
        season_context = EnvironmentSensor.get_seasonal_modifier()
        current_season = EnvironmentSensor._get_season(datetime.now().month)
        status["current_season"] = current_season
        return status
    def update_passive_stats(self):
        now = datetime.now()
        hours_passed = (now - self.last_interaction).total_seconds() / 3600
        if hours_passed > 0:
            hunger_increase = min(hours_passed * 2, 20)
            env_modifiers = EnvironmentSensor.get_time_of_day_modifier()
            seasonal_modifiers = EnvironmentSensor.get_seasonal_modifier()
            if hasattr(self, 'personality_traits'):
                independence = self.personality_traits.get("independence", PersonalityTrait("independence", 50))
                if hours_passed > 2:
                    isolation_resistance = independence.strength / 100
                    happiness_decrease = min((hours_passed - 2) * 1.5 * (1 - isolation_resistance * 0.5), 15)
                    self.happiness = max(0, self.happiness - happiness_decrease)
                sociability = self.personality_traits.get("sociability", PersonalityTrait("sociability", 50))
                if hours_passed > 4:
                    social_need = sociability.strength / 100
                    loneliness_penalty = social_need * 5
                    self.happiness = max(0, self.happiness - loneliness_penalty)
                calmness = self.personality_traits.get("calmness", PersonalityTrait("calmness", 50))
                stress_resistance = calmness.strength / 100
                if self.hunger > 80 or self.happiness < 20:
                    health_decrease = min(hours_passed * 0.3 * (1 - stress_resistance * 0.3), 5)
                    self.health = max(0, self.health - health_decrease)
            else:
                if hours_passed > 2:
                    happiness_decrease = min((hours_passed - 2) * 1.5, 15)
                    self.happiness = max(0, self.happiness - happiness_decrease)
                if self.hunger > 80 or self.happiness < 20:
                    health_decrease = min(hours_passed * 0.3, 5)
                    self.health = max(0, self.health - health_decrease)
            if hasattr(self, 'environmental_sensitivity'):
                env_effect = self.environmental_sensitivity
                energy_modifier = env_modifiers.get("energy", 1.0)
                if self.energy < 80:
                    energy_increase = min(hours_passed * 0.5 * energy_modifier * env_effect, 10)
                    self.energy = min(100, self.energy + energy_increase)
                health_modifier = seasonal_modifiers.get("health", 1.0)
                if health_modifier != 1.0:
                    health_change = (health_modifier - 1.0) * 2 * env_effect
                    self.health = max(0, min(100, self.health + health_change))
            self.hunger = min(100, self.hunger + hunger_increase)
            if hasattr(self, 'current_entropy_seed'):
                if int(hours_passed) > 0:
                    self.current_entropy_seed = EnvironmentSensor.get_entropy_seed()
            if hasattr(self, 'interaction_frequency_history'):
                current_day = now.date()
                if not self.interaction_frequency_history or self.interaction_frequency_history[-1]["date"] != current_day:
                    self.interaction_frequency_history.append({
                        "date": current_day,
                        "interactions": self.interactions_today
                    })
                    self.interactions_today = 0  
                if len(self.interaction_frequency_history) > 30:
                    self.interaction_frequency_history = self.interaction_frequency_history[-30:]
            if hasattr(self, 'evolve_based_on_experience'):
                self.evolve_based_on_experience()
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
        data = {
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
            "evolution_points": getattr(self, 'evolution_points', 0)
        }
        if hasattr(self, 'personality_traits'):
            data["personality_traits"] = {}
            for name, trait in self.personality_traits.items():
                data["personality_traits"][name] = {
                    "strength": trait.strength,
                    "last_changed": trait.last_changed.isoformat(),
                    "development_history": [
                        {
                            "timestamp": entry["timestamp"].isoformat(),
                            "old_value": entry["old_value"],
                            "new_value": entry["new_value"],
                            "change": entry["change"],
                            "reason": entry["reason"]
                        } for entry in trait.development_history[-10:]  
                    ]
                }
        if hasattr(self, 'memory'):
            data["memory"] = {
                "experiences": [
                    {
                        "timestamp": exp["timestamp"].isoformat(),
                        "type": exp["type"],
                        "details": exp["details"],
                        "emotional_impact": exp["emotional_impact"],
                        "context": exp["context"]
                    } for exp in self.memory.experiences[-50:]  
                ],
                "behavior_patterns": self.memory.behavior_patterns,
                "preferences": self.memory.preferences,
                "time_patterns": self.memory.time_patterns
            }
        if hasattr(self, 'environmental_sensitivity'):
            data["environmental_sensitivity"] = self.environmental_sensitivity
        if hasattr(self, 'interaction_frequency_history'):
            data["interaction_frequency_history"] = [
                {
                    "date": entry["date"].isoformat(),
                    "interactions": entry["interactions"]
                } for entry in self.interaction_frequency_history
            ]
        if hasattr(self, 'favorite_activities'):
            data["favorite_activities"] = self.favorite_activities
        if hasattr(self, 'preferred_foods'):
            data["preferred_foods"] = self.preferred_foods
        if hasattr(self, 'circadian_preferences'):
            data["circadian_preferences"] = self.circadian_preferences
        if hasattr(self, 'current_entropy_seed'):
            data["current_entropy_seed"] = self.current_entropy_seed
        return data
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
        if "personality_traits" in data:
            pet.personality_traits = {}
            for name, trait_data in data["personality_traits"].items():
                trait = PersonalityTrait(name, trait_data["strength"])
                trait.last_changed = datetime.fromisoformat(trait_data["last_changed"])
                trait.development_history = []
                for entry in trait_data.get("development_history", []):
                    trait.development_history.append({
                        "timestamp": datetime.fromisoformat(entry["timestamp"]),
                        "old_value": entry["old_value"],
                        "new_value": entry["new_value"],
                        "change": entry["change"],
                        "reason": entry["reason"]
                    })
                pet.personality_traits[name] = trait
        if "memory" in data:
            pet.memory = PetMemory()
            memory_data = data["memory"]
            for exp_data in memory_data.get("experiences", []):
                experience = {
                    "timestamp": datetime.fromisoformat(exp_data["timestamp"]),
                    "type": exp_data["type"],
                    "details": exp_data["details"],
                    "emotional_impact": exp_data["emotional_impact"],
                    "context": exp_data["context"]
                }
                pet.memory.experiences.append(experience)
            pet.memory.behavior_patterns = memory_data.get("behavior_patterns", {})
            pet.memory.preferences = memory_data.get("preferences", {})
            pet.memory.time_patterns = memory_data.get("time_patterns", {})
        pet.environmental_sensitivity = data.get("environmental_sensitivity", random.uniform(0.5, 1.5))
        if "interaction_frequency_history" in data:
            pet.interaction_frequency_history = []
            for entry in data["interaction_frequency_history"]:
                pet.interaction_frequency_history.append({
                    "date": datetime.fromisoformat(entry["date"]).date(),
                    "interactions": entry["interactions"]
                })
        pet.favorite_activities = data.get("favorite_activities", {})
        pet.preferred_foods = data.get("preferred_foods", {})
        pet.circadian_preferences = data.get("circadian_preferences", pet._initialize_circadian_rhythm())
        pet.current_entropy_seed = data.get("current_entropy_seed", EnvironmentSensor.get_entropy_seed())
        return pet
    def _update_food_preference(self, food_type, satisfaction):
        if food_type not in self.preferred_foods:
            self.preferred_foods[food_type] = {"satisfaction_total": 0, "times_eaten": 0}
        self.preferred_foods[food_type]["satisfaction_total"] += satisfaction
        self.preferred_foods[food_type]["times_eaten"] += 1
    def _update_activity_preference(self, activity, enjoyment):
        if activity not in self.favorite_activities:
            self.favorite_activities[activity] = {"enjoyment_total": 0, "times_played": 0}
        self.favorite_activities[activity]["enjoyment_total"] += enjoyment
        self.favorite_activities[activity]["times_played"] += 1
    def _adapt_personality_from_feeding(self, food_type, satisfaction):
        if not hasattr(self, 'personality_traits'):
            return
        if food_type != "kibble" and satisfaction > 10:
            self.personality_traits["curiosity"].modify(0.5, f"enjoyed {food_type}")
        if hasattr(self, 'last_fed') and self.last_fed:
            hours_since_last = (datetime.now() - self.last_fed).total_seconds() / 3600
            if hours_since_last < 6:  
                self.personality_traits["loyalty"].modify(0.3, "regular feeding")
    def _adapt_personality_from_playing(self, activity, enjoyment):
        if not hasattr(self, 'personality_traits'):
            return
        trait_mappings = {
            "puzzle": ("intelligence", 0.4),
            "training": ("intelligence", 0.6),
            "fetch": ("playfulness", 0.3),
            "tug": ("mischief", 0.2),
            "cuddle": ("sociability", 0.4)
        }
        if activity in trait_mappings and enjoyment > 5:
            trait, modifier = trait_mappings[activity]
            self.personality_traits[trait].modify(modifier, f"enjoyed {activity}")
    def _get_personality_based_response(self, situation, context=""):
        if not hasattr(self, 'personality_traits'):
            return "Looks at you meaningfully"
        responses = {
            "too_full": {
                "high_mischief": ["Knocks over food bowl playfully", "Hides the food for later"],
                "high_independence": ["Walks away with dignity", "Gives you a pointed look"],
                "high_sociability": ["Nuzzles you apologetically", "Sits close but doesn't eat"],
                "default": ["Pushes food away gently", "Looks satisfied"]
            },
            "too_tired": {
                "high_playfulness": ["Tries to play but stumbles sleepily", "Wags tail weakly"],
                "high_independence": ["Curls up independently", "Finds a quiet spot to rest"],
                "high_sociability": ["Leans against you tiredly", "Falls asleep near you"],
                "default": ["Yawns and lies down", "Stretches and settles"]
            },
            "too_hungry": {
                "high_mischief": ["Steals attention from the activity", "Dramatically flops down"],
                "high_intelligence": ["Points toward food bowl", "Brings you to food area"],
                "high_sociability": ["Follows you around hopefully", "Makes pleading eyes"],
                "default": ["Looks at empty food bowl", "Stomach rumbles audibly"]
            }
        }
        situation_responses = responses.get(situation, {})
        highest_trait = max(self.personality_traits.items(), 
                          key=lambda x: x[1].strength)
        trait_name, trait_obj = highest_trait
        response_key = f"high_{trait_name}" if trait_obj.strength > 70 else "default"
        if response_key in situation_responses:
            return random.choice(situation_responses[response_key])
        else:
            return random.choice(situation_responses.get("default", ["Reacts characteristically"]))
    def _get_advanced_response(self, action_type, context, satisfaction):
        if not hasattr(self, 'memory'):
            return self._get_basic_response(action_type, context)
        is_favorite = False
        if action_type == "feeding" and context in self.preferred_foods:
            avg_satisfaction = (self.preferred_foods[context]["satisfaction_total"] / 
                              max(1, self.preferred_foods[context]["times_eaten"]))
            is_favorite = avg_satisfaction > 12
        elif action_type == "playing" and context in self.favorite_activities:
            avg_enjoyment = (self.favorite_activities[context]["enjoyment_total"] / 
                           max(1, self.favorite_activities[context]["times_played"]))
            is_favorite = avg_enjoyment > 12
        base_responses = self._get_basic_response(action_type, context)
        if is_favorite:
            enhanced_responses = [
                f"Shows obvious delight - this is clearly a favorite!",
                f"Remembers how much they love this and gets extra excited",
                f"Reacts with learned enthusiasm from past experiences"
            ]
            return random.choice(enhanced_responses)
        elif satisfaction > 15:
            return f"{base_responses} - and seems to be learning to love it!"
        else:
            return base_responses
    def _get_basic_response(self, action_type, context):
        if action_type == "feeding":
            return self._get_food_response(context)
        elif action_type == "playing":
            return self._get_play_response(context)
        else:
            return "Reacts appropriately"
    def get_personality_summary(self):
        if not hasattr(self, 'personality_traits'):
            return "Personality still developing..."
        summary = []
        for name, trait in self.personality_traits.items():
            level = trait.get_level()
            if trait.strength > 60:  
                summary.append(f"{level} {name}")
        if not summary:
            return "Balanced personality"
        return ", ".join(summary[:3])  
    def get_behavioral_insights(self):
        insights = []
        if hasattr(self, 'preferred_foods') and self.preferred_foods:
            best_food = max(self.preferred_foods.items(), 
                          key=lambda x: x[1]["satisfaction_total"] / max(1, x[1]["times_eaten"]))
            insights.append(f"Favorite food: {best_food[0]}")
        if hasattr(self, 'favorite_activities') and self.favorite_activities:
            best_activity = max(self.favorite_activities.items(),
                              key=lambda x: x[1]["enjoyment_total"] / max(1, x[1]["times_played"]))
            insights.append(f"Favorite activity: {best_activity[0]}")
        if hasattr(self, 'memory') and self.memory.time_patterns:
            most_active_hour = max(self.memory.time_patterns.items(),
                                 key=lambda x: sum(x[1].values()))
            insights.append(f"Most active time: {most_active_hour[0]}:00")
        return insights if insights else ["Still learning and adapting..."]
    def evolve_based_on_experience(self):
        if not hasattr(self, 'memory'):
            return False
        total_experiences = len(self.memory.experiences)
        if total_experiences > 100 and self.evolution_stage == "baby":
            self.evolution_stage = "juvenile"
            self._apply_evolution_changes("juvenile")
            return True
        elif total_experiences > 250 and self.evolution_stage == "juvenile":
            self.evolution_stage = "adolescent"
            self._apply_evolution_changes("adolescent")
            return True
        elif total_experiences > 500 and self.evolution_stage == "adolescent":
            self.evolution_stage = "adult"
            self._apply_evolution_changes("adult")
            return True
        elif total_experiences > 1000 and self.evolution_stage == "adult":
            self.evolution_stage = "elder"
            self._apply_evolution_changes("elder")
            return True
        return False
    def _apply_evolution_changes(self, new_stage):
        stage_bonuses = {
            "juvenile": {"intelligence": 5, "curiosity": 3},
            "adolescent": {"independence": 8, "playfulness": 5},
            "adult": {"loyalty": 10, "calmness": 7},
            "elder": {"intelligence": 15, "calmness": 12}
        }
        if new_stage in stage_bonuses and hasattr(self, 'personality_traits'):
            for trait, bonus in stage_bonuses[new_stage].items():
                if trait in self.personality_traits:
                    self.personality_traits[trait].modify(bonus, f"evolved to {new_stage}")
        if new_stage in ["adult", "elder"]:
            self.health = min(100, self.health + 5)