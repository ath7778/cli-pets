import json
import os
from datetime import datetime
from typing import Optional
from pet import Pet
class GameManager:
    def __init__(self, save_file="pet_save.json"):
        self.save_file = save_file
        self.pet = None
        self.game_active = False
    def create_new_pet(self, name, species="Generic"):
        self.pet = Pet(name, species)
        self.game_active = True
        self.save_game()
        return self.pet
    def load_game(self):
        if not os.path.exists(self.save_file):
            return False
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            self.pet = Pet.from_dict(data)
            self.game_active = True
            self.pet.update_passive_stats()
            return True
        except (json.JSONDecodeError, KeyError, ValueError):
            return False
    def save_game(self):
        if not self.pet:
            return False
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.pet.to_dict(), f, indent=2)
            return True
        except Exception:
            return False
    def has_save_file(self):
        return os.path.exists(self.save_file)
    def delete_save_file(self):
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
            return True
        except Exception:
            return False
    def get_save_info(self):
        if not os.path.exists(self.save_file):
            return None
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            birth_time = datetime.fromisoformat(data["birth_time"])
            age_delta = datetime.now() - birth_time
            return {
                "name": data["name"],
                "species": data.get("species", "Generic"),
                "level": data["level"],
                "age_days": age_delta.days,
                "last_interaction": data["last_interaction"],
                "health": data["health"]
            }
        except Exception:
            return None
    def auto_save(self):
        if self.pet and self.game_active:
            self.save_game()
class GameStats:
    def __init__(self, stats_file="game_stats.json"):
        self.stats_file = stats_file
        self.stats = {
            "total_pets_created": 0,
            "total_interactions": 0,
            "highest_level_reached": 0,
            "longest_living_pet_days": 0,
            "first_pet_created": None,
            "last_game_session": None
        }
        self.load_stats()
    def load_stats(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    loaded_stats = json.load(f)
                self.stats.update(loaded_stats)
            except Exception:
                pass
    def save_stats(self):
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception:
            pass
    def update_pet_created(self, pet):
        self.stats["total_pets_created"] += 1
        if not self.stats["first_pet_created"]:
            self.stats["first_pet_created"] = datetime.now().isoformat()
        self.save_stats()
    def update_interaction(self):
        self.stats["total_interactions"] += 1
        self.stats["last_game_session"] = datetime.now().isoformat()
        self.save_stats()
    def update_pet_level(self, level):
        if level > self.stats["highest_level_reached"]:
            self.stats["highest_level_reached"] = level
            self.save_stats()
    def get_stats_summary(self):
        return {
            "Total Pets Created": self.stats["total_pets_created"],
            "Total Interactions": self.stats["total_interactions"],
            "Highest Level Reached": self.stats["highest_level_reached"],
            "First Pet Created": self.stats["first_pet_created"],
            "Last Game Session": self.stats["last_game_session"]
        }
class GameConfig:
    def __init__(self, config_file="game_config.json"):
        self.config_file = config_file
        self.config = {
            "auto_save": True,
            "max_pet_name_length": 20,
            "difficulty_level": "normal",
            "debug_mode": False
        }
        self.load_config()
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                self.config.update(loaded_config)
            except Exception:
                pass
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass
    def get_setting(self, key, default=None):
        return self.config.get(key, default)
    def set_setting(self, key, value):
        self.config[key] = value
        self.save_config()