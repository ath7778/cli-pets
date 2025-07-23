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
            'clear': self.clear_screen
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
        print("                         Version 1.0")
        print("=" * 70)
        print("\nWelcome! Your digital companion awaits...")
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
def main():
    try:
        cli = TerminalPetsCLI()
        cli.start()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()