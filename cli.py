import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional
from pet import Pet
from game_manager import GameManager, GameStats, GameConfig
class TerminalPetsCLI:
    def __init__(self):
        self.game_manager = GameManager()
        self.game_stats = GameStats()
        self.game_config = GameConfig()
        self.running = True
        self.commands = {
            'help': self.show_help,
            'h': self.show_help,
            'status': self.show_status,
            'feed': self.feed_pet,
            'play': self.play_with_pet,
            'rest': self.pet_rest,
            'save': self.save_game,
            'quit': self.quit_game,
            'exit': self.quit_game,
            'info': self.show_pet_info,
            'mood': self.check_mood,
            'new': self.create_new_pet,
            'load': self.load_existing_pet,
            'clear': self.clear_screen,
            'personality': self.show_personality,
            'traits': self.show_personality,
            'memory': self.show_memory,
            'memories': self.show_memory,
            'evolution': self.show_evolution,
            'evolve': self.trigger_evolution,
            'insights': self.show_behavioral_insights,
            'patterns': self.show_behavioral_patterns,
            'environment': self.show_environment_info,
            'preferences': self.show_preferences
        }
        self.food_types = ["kibble", "treat", "vegetable", "meat", "fish"]
        self.activity_types = ["fetch", "tug", "puzzle", "cuddle", "training"]
    def start(self):
        self.clear_screen()
        self.show_banner()
        if self.game_manager.has_save_file():
            self.handle_existing_save()
        else:
            self.setup_new_game()
        self.main_loop()
    def show_banner(self):
        print("=" * 70)
        print("                          TERMINAL PETS")
        print("                     Virtual Pet Simulator")
        print("                         Version 2.0")
        print("                    Advanced Evolution Engine")
        print("=" * 70)
        print("\nWelcome! Your digital companion awaits...")
        print("New in v2.0: Personality traits, behavioral learning, environmental adaptation")
    def handle_existing_save(self):
        save_info = self.game_manager.get_save_info()
        if save_info:
            print(f"\nFound existing pet: {save_info['name']} (Level {save_info['level']})")
            choice = input("Load existing pet? (y/n): ").lower().strip()
            if choice in ['y', 'yes', '']:
                if self.game_manager.load_game():
                    print(f"Welcome back! {self.game_manager.pet.name} is happy to see you.")
                    self.show_pet_status_brief()
                else:
                    print("Error loading save. Starting new game...")
                    self.setup_new_game()
            else:
                self.setup_new_game()
        else:
            print("Save file corrupted. Starting new game...")
            self.setup_new_game()
    def setup_new_game(self):
        print("\n" + "-" * 50)
        print("Creating your new virtual pet...")
        name = self.get_pet_name()
        species = self.get_pet_species()
        pet = self.game_manager.create_new_pet(name, species)
        self.game_stats.update_pet_created(pet)
        print(f"\n{name} the {species} has been created!")
        print(f"Birth time: {pet.birth_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("Starting stats: Health 100, others at 50")
        self.show_basic_commands()
    def get_pet_name(self):
        while True:
            name = input("\nPet name: ").strip()
            if name and len(name) <= 20:
                return name
            elif not name:
                print("Please enter a name.")
            else:
                print("Name too long (max 20 characters).")
    def get_pet_species(self):
        print("\nPet type (Dog, Cat, Dragon, etc.):")
        species = input("Species (Enter for Generic): ").strip()
        return species if species else "Generic"
    def show_basic_commands(self):
        print("\nBasic commands:")
        print("  help     - Show all commands")
        print("  status   - Check pet condition")
        print("  feed     - Give food")
        print("  play     - Play activities")
        print("  quit     - Save and exit")
    def show_pet_status_brief(self):
        pet = self.game_manager.pet
        print(f"\nCurrent status:")
        print(f"  Hunger: {pet.hunger}/100")
        print(f"  Happiness: {pet.happiness}/100")
        print(f"  Energy: {pet.energy}/100")
        print(f"  Health: {pet.health}/100")
    def main_loop(self):
        print("\nGame ready. Type 'help' for commands.\n")
        while self.running:
            try:
                if self.game_manager.pet:
                    self.game_manager.pet.update_passive_stats()
                    if self.game_manager.pet.level_up_check():
                        print(f"\nLevel up! {self.game_manager.pet.name} is now level {self.game_manager.pet.level}!")
                    if self.game_config.get_setting("auto_save", True):
                        self.game_manager.auto_save()
                user_input = input("> ").strip().lower()
                if not user_input:
                    continue
                parts = user_input.split()
                command = parts[0]
                args = parts[1:] if len(parts) > 1 else []
                if command in self.commands:
                    self.commands[command](args)
                    self.game_stats.update_interaction()
                else:
                    print(f"Unknown command: '{command}'. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\nSaving game...")
                self.save_game([])
                self.running = False
            except EOFError:
                self.running = False
            except Exception as e:
                print(f"Error: {e}")
    def show_help(self, args):
        print("\nAvailable Commands:")
        print("-" * 40)
        print("Pet Care:")
        print("  feed [type]    - Feed pet (kibble/treat/vegetable/meat/fish)")
        print("  play [type]    - Play (fetch/tug/puzzle/cuddle/training)")
        print("  rest           - Let pet rest")
        print("\nInformation:")
        print("  status         - Show pet status")
        print("  info           - Detailed pet info")
        print("  mood           - Check pet mood")
        print("\nPersonality & Evolution (v2.0):")
        print("  personality    - Show personality traits")
        print("  memory         - View pet's memories")
        print("  evolution      - Check evolution status")
        print("  evolve         - Trigger evolution check")
        print("  insights       - Show behavioral insights")
        print("  patterns       - Show learned patterns")
        print("  environment    - Show environmental effects")
        print("  preferences    - Show learned preferences")
        print("\nGame:")
        print("  save           - Save game")
        print("  new            - Create new pet")
        print("  load           - Load saved pet")
        print("  clear          - Clear screen")
        print("  quit           - Save and exit")
    def show_status(self, args):
        if not self.game_manager.pet:
            print("No pet found. Create one first with 'new' command.")
            return
        pet = self.game_manager.pet
        status = pet.get_status()
        print(f"\n{status['name']} the {status['species']}")
        print("-" * 40)
        print(f"Age: {status['age']}")
        print(f"Level: {status['level']} (XP: {status['experience']}/100)")
        print(f"Mood: {status['mood']}")
        print("\nStats:")
        for stat_name, value in status['stats'].items():
            bar = self.create_stat_bar(value)
            print(f"  {stat_name.capitalize():10} [{bar}] {value:3}/100")
        print(f"\nInteractions today: {status['interactions_today']}")
        print(f"Total interactions: {status['total_interactions']}")
        if status['stats']['health'] < 50:
            print(f"\nWarning: {pet.name} is not feeling well!")
        if status['stats']['hunger'] > 80:
            print(f"Warning: {pet.name} is very hungry!")
    def create_stat_bar(self, value):
        filled = int(value / 5)  
        return "#" * filled + "-" * (20 - filled)
    def feed_pet(self, args):
        if not self.game_manager.pet:
            print("No pet to feed.")
            return
        food_type = args[0] if args and args[0] in self.food_types else "kibble"
        result = self.game_manager.pet.feed(food_type)
        if result["success"]:
            print(f"{result['message']}")
            print(f"New hunger level: {self.game_manager.pet.hunger}/100")
        else:
            print(f"{result['message']}")
    def play_with_pet(self, args):
        if not self.game_manager.pet:
            print("No pet to play with.")
            return
        activity = args[0] if args and args[0] in self.activity_types else "fetch"
        result = self.game_manager.pet.play(activity)
        if result["success"]:
            print(f"{result['message']}")
            print(f"Happiness: {self.game_manager.pet.happiness}/100, Energy: {self.game_manager.pet.energy}/100")
        else:
            print(f"{result['message']}")
    def pet_rest(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        result = self.game_manager.pet.rest()
        print(f"{result['message']}")
        if result["success"]:
            print(f"Energy restored to: {self.game_manager.pet.energy}/100")
    def check_mood(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        pet = self.game_manager.pet
        mood = pet.calculate_mood()
        print(f"\n{pet.name} is feeling {mood}")
        if pet.hunger > 70:
            print("Suggestion: Feed your pet")
        if pet.happiness < 40:
            print("Suggestion: Play with your pet")
        if pet.energy < 30:
            print("Suggestion: Let your pet rest")
    def show_pet_info(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        pet = self.game_manager.pet
        print(f"\nDetailed Info: {pet.name}")
        print(f"Species: {pet.species}")
        print(f"Born: {pet.birth_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Age: {pet.get_age()}")
        print(f"Level: {pet.level}")
        print(f"Total interactions: {pet.total_interactions}")
    def save_game(self, args):
        if self.game_manager.save_game():
            print("Game saved.")
        else:
            print("Save failed.")
    def create_new_pet(self, args):
        if self.game_manager.has_save_file():
            confirm = input("This will delete current pet. Continue? (y/n): ")
            if confirm.lower() not in ['y', 'yes']:
                print("Cancelled.")
                return
            self.game_manager.delete_save_file()
        self.setup_new_game()
    def load_existing_pet(self, args):
        if self.game_manager.load_game():
            print(f"Loaded {self.game_manager.pet.name}")
        else:
            print("Load failed.")
    def clear_screen(self, args=None):
        os.system('clear' if os.name == 'posix' else 'cls')
    def quit_game(self, args):
        print("\nThanks for playing!")
        if self.game_manager.pet:
            self.save_game([])
            print(f"{self.game_manager.pet.name} will miss you!")
        self.running = False
    def show_personality(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        pet = self.game_manager.pet
        if not hasattr(pet, 'personality_traits'):
            print("Personality system not available for this pet.")
            return
        print(f"\n{pet.name}'s Personality Profile:")
        print("=" * 40)
        for name, trait in pet.personality_traits.items():
            level = trait.get_level()
            bar = self.create_stat_bar(trait.strength)
            print(f"  {name.capitalize():12} [{bar}] {trait.strength:3.0f}/100 ({level})")
        print(f"\nPersonality Summary: {pet.get_personality_summary()}")
        recent_changes = []
        for trait in pet.personality_traits.values():
            if trait.development_history:
                recent_changes.extend(trait.development_history[-2:])  
        if recent_changes:
            recent_changes.sort(key=lambda x: x["timestamp"], reverse=True)
            print(f"\nRecent personality developments:")
            for change in recent_changes[:3]:  
                trait_name = change.get("reason", "").split()[-1] if change.get("reason") else "unknown"
                print(f"  - {change['timestamp'].strftime('%m/%d %H:%M')}: {change['reason']}")
    def show_memory(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        pet = self.game_manager.pet
        if not hasattr(pet, 'memory'):
            print("Memory system not available for this pet.")
            return
        memory = pet.memory
        print(f"\n{pet.name}'s Memory Bank:")
        print("=" * 40)
        print(f"Total experiences: {len(memory.experiences)}")
        if memory.experiences:
            print("\nRecent experiences:")
            for exp in memory.experiences[-5:]:  
                timestamp = exp["timestamp"].strftime("%m/%d %H:%M")
                impact = "positive" if exp["emotional_impact"] > 0 else "negative" if exp["emotional_impact"] < 0 else "neutral"
                print(f"  {timestamp}: {exp['type']} - {impact} impact")
                if exp["details"]:
                    detail_str = str(exp["details"])[:50] + "..." if len(str(exp["details"])) > 50 else str(exp["details"])
                    print(f"    Details: {detail_str}")
        print(f"\nMost common activities:")
        for activity, data in list(memory.behavior_patterns.items())[:3]:
            print(f"  {activity}: {data['count']} times")
    def show_evolution(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        pet = self.game_manager.pet
        print(f"\n{pet.name}'s Evolution Status:")
        print("=" * 40)
        print(f"Current stage: {pet.evolution_stage}")
        print(f"Evolution points: {getattr(pet, 'evolution_points', 0)}")
        if hasattr(pet, 'memory'):
            experiences = len(pet.memory.experiences)
            print(f"Total experiences: {experiences}")
            next_requirements = {
                "baby": ("juvenile", 100),
                "juvenile": ("adolescent", 250), 
                "adolescent": ("adult", 500),
                "adult": ("elder", 1000)
            }
            if pet.evolution_stage in next_requirements:
                next_stage, required_exp = next_requirements[pet.evolution_stage]
                progress = min(100, (experiences / required_exp) * 100)
                bar = self.create_stat_bar(progress)
                print(f"Progress to {next_stage}: [{bar}] {experiences}/{required_exp}")
            else:
                print("Maximum evolution stage reached!")
    def trigger_evolution(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        pet = self.game_manager.pet
        if hasattr(pet, 'evolve_based_on_experience'):
            if pet.evolve_based_on_experience():
                print(f"\nEvolution occurred! {pet.name} is now a {pet.evolution_stage}!")
                print("New abilities and traits have been unlocked!")
            else:
                print(f"{pet.name} is not ready to evolve yet.")
                print("Continue interacting to gain more experience.")
        else:
            print("Evolution system not available for this pet.")
    def show_behavioral_insights(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        pet = self.game_manager.pet
        insights = pet.get_behavioral_insights()
        print(f"\n{pet.name}'s Behavioral Insights:")
        print("=" * 40)
        for insight in insights:
            print(f"  - {insight}")
        if hasattr(pet, 'favorite_activities') and pet.favorite_activities:
            print("\nActivity enjoyment levels:")
            for activity, data in pet.favorite_activities.items():
                avg_enjoyment = data["enjoyment_total"] / max(1, data["times_played"])
                print(f"  {activity}: {avg_enjoyment:.1f}/20 enjoyment (played {data['times_played']} times)")
        if hasattr(pet, 'preferred_foods') and pet.preferred_foods:
            print("\nFood satisfaction levels:")
            for food, data in pet.preferred_foods.items():
                avg_satisfaction = data["satisfaction_total"] / max(1, data["times_eaten"])
                print(f"  {food}: {avg_satisfaction:.1f}/20 satisfaction (eaten {data['times_eaten']} times)")
    def show_behavioral_patterns(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        pet = self.game_manager.pet
        if not hasattr(pet, 'memory'):
            print("Pattern learning not available for this pet.")
            return
        memory = pet.memory
        print(f"\n{pet.name}'s Learned Patterns:")
        print("=" * 40)
        if memory.time_patterns:
            print("Activity patterns by time of day:")
            for hour in sorted(memory.time_patterns.keys()):
                activities = memory.time_patterns[hour]
                if activities:
                    total_activities = sum(activities.values())
                    most_common = max(activities.items(), key=lambda x: x[1])
                    print(f"  {hour:2d}:00 - Most active: {most_common[0]} ({most_common[1]}/{total_activities} activities)")
        if hasattr(pet, 'interaction_frequency_history'):
            recent_days = pet.interaction_frequency_history[-7:]  
            if recent_days:
                avg_interactions = sum(day["interactions"] for day in recent_days) / len(recent_days)
                print(f"\nAverage daily interactions (last 7 days): {avg_interactions:.1f}")
    def show_environment_info(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        pet = self.game_manager.pet
        from pet import EnvironmentSensor
        time_mod = EnvironmentSensor.get_time_of_day_modifier()
        seasonal_mod = EnvironmentSensor.get_seasonal_modifier()
        print(f"\nEnvironmental Status:")
        print("=" * 40)
        hour = datetime.now().hour
        print(f"Current time: {hour}:00")
        print(f"Preferred activity: {time_mod.get('activity_preference', 'any')}")
        print(f"Energy modifier: {time_mod.get('energy', 1.0):.1f}x")
        print(f"Happiness modifier: {time_mod.get('happiness', 1.0):.1f}x")
        month = datetime.now().month
        season = EnvironmentSensor._get_season(month)
        print(f"\nCurrent season: {season}")
        print(f"Health modifier: {seasonal_mod.get('health', 1.0):.1f}x")
        print(f"Energy modifier: {seasonal_mod.get('energy', 1.0):.1f}x")
        print(f"Happiness modifier: {seasonal_mod.get('happiness', 1.0):.1f}x")
        if hasattr(pet, 'environmental_sensitivity'):
            sensitivity = pet.environmental_sensitivity
            sensitivity_desc = "highly sensitive" if sensitivity > 1.3 else "moderately sensitive" if sensitivity > 0.7 else "less sensitive"
            print(f"\n{pet.name} is {sensitivity_desc} to environmental changes ({sensitivity:.2f})")
    def show_preferences(self, args):
        if not self.game_manager.pet:
            print("No pet found.")
            return
        pet = self.game_manager.pet
        print(f"\n{pet.name}'s Learned Preferences:")
        print("=" * 40)
        if hasattr(pet, 'preferred_foods') and pet.preferred_foods:
            print("Food preferences (by satisfaction):")
            food_items = [(food, data["satisfaction_total"] / max(1, data["times_eaten"])) 
                         for food, data in pet.preferred_foods.items()]
            food_items.sort(key=lambda x: x[1], reverse=True)
            for food, avg_satisfaction in food_items:
                preference = "loves" if avg_satisfaction > 15 else "likes" if avg_satisfaction > 10 else "tolerates"
                print(f"  {food}: {preference} ({avg_satisfaction:.1f}/20)")
        if hasattr(pet, 'favorite_activities') and pet.favorite_activities:
            print("\nActivity preferences (by enjoyment):")
            activity_items = [(activity, data["enjoyment_total"] / max(1, data["times_played"])) 
                            for activity, data in pet.favorite_activities.items()]
            activity_items.sort(key=lambda x: x[1], reverse=True)
            for activity, avg_enjoyment in activity_items:
                preference = "adores" if avg_enjoyment > 15 else "enjoys" if avg_enjoyment > 10 else "accepts"
                print(f"  {activity}: {preference} ({avg_enjoyment:.1f}/20)")
        if hasattr(pet, 'memory') and pet.memory.time_patterns:
            print("\nTime preferences:")
            best_times = {}
            for hour, activities in pet.memory.time_patterns.items():
                total = sum(activities.values())
                if total > 5:  
                    best_times[hour] = total
            if best_times:
                sorted_times = sorted(best_times.items(), key=lambda x: x[1], reverse=True)
                for hour, count in sorted_times[:3]:  
                    print(f"  {hour:2d}:00 - Very active ({count} interactions)")