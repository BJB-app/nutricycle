# -*- coding: utf-8 -*-
"""Menstrual app- NutriCycle

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IsmXzfitW72PRP7GDqwPuuPyVnMv88-m
"""

from datetime import datetime

# ===============================
# User class: encapsulates user data and preferences (Encapsulation)
# ===============================
class User:
    def __init__(self, name, cycle_start_date, cycle_length=28, period_length=5, preferences=None):
        # Private attributes: Encapsulation in action
        self.__name = name
        self.__cycle_start_date = datetime.strptime(cycle_start_date, "%d-%m-%Y")
        self.__cycle_length = cycle_length
        self.__period_length = period_length
        # Composition: user HAS a UserPreferences object
        self.__preferences = preferences if preferences else UserPreferences()

    # Getter methods for encapsulated data
    def get_name(self):
        return self.__name

    def get_cycle_start_date(self):
        return self.__cycle_start_date

    def get_cycle_length(self):
        return self.__cycle_length

    def get_period_length(self):
        return self.__period_length

    def get_allergies(self):  # Composition in use: delegates to UserPreferences
        return self.__preferences.get_allergies()

# ===============================
# UserPreferences: manages allergy list (Composition)
# ===============================
class UserPreferences:
    def __init__(self, allergies=None):
        # Private attribute to store allergies list
        self.__allergies = allergies if allergies else []

    def get_allergies(self):
        return self.__allergies

# ===============================
# Phase class: reusable structure for all menstrual phases
# ===============================
class Phase:
    def __init__(self, name, start_day, end_day, recommendations, avoid):
        self.__name = name
        self.__start_day = start_day
        self.__end_day = end_day
        self.__recommendations = recommendations
        self.__avoid = avoid

    def is_current_phase(self, cycle_day):
        return self.__start_day <= cycle_day <= self.__end_day

    def get_filtered_recommendations(self, allergies):
        return [food for food in self.__recommendations if food not in allergies]

    def get_name(self):
        return self.__name

    def get_avoid_list(self):
        return self.__avoid

# ===============================
# EducationalPhase subclass: demonstrates inheritance meaningfully
# ===============================
class EducationalPhase(Phase):
    def __init__(self, name, start_day, end_day, recommendations, avoid, info):
        super().__init__(name, start_day, end_day, recommendations, avoid)
        self.__info = info  # New attribute specific to this subclass

    def get_info(self):
        return self.__info

    # Overridden method — adds educational emphasis to each food
    def get_filtered_recommendations(self, allergies):
        base_list = super().get_filtered_recommendations(allergies)
        return [f"{item} (educational focus)" for item in base_list]

# ===============================
# CycleTracker: Composition — HAS-A list of Phase objects
# ===============================
class CycleTracker:
    def __init__(self, user):
        self.__user = user
        self.__phases = [
            Phase("Menstrual Phase", 1, user.get_period_length(), {
                "Fruits": ["berries", "apples", "grapes", "pomegranate", "watermelon", "plums", "cherries", "cranberries", "blackberries", "pears"],
                "Proteins": ["lentils", "chicken", "eggs", "tofu", "turkey", "beef", "tempeh", "kidney beans", "sardines", "anchovies"],
                "Greens": ["spinach", "kale", "chard", "broccoli", "cabbage", "seaweed", "parsley", "dandelion greens", "beet greens", "turnip greens"],
                "Healthy Fats": ["avocado", "flax seeds", "chia seeds", "walnuts", "olive oil", "pumpkin seeds", "almonds", "pecans", "hemp seeds", "sunflower seeds"]
            }, ["Caffeine", "Processed foods", "Sugary snacks"]),

            EducationalPhase("Follicular Phase", user.get_period_length() + 1, 14, {
                "Fruits": ["kiwi", "oranges", "papaya", "blueberries", "strawberries", "apples", "mango", "peaches", "nectarines", "cantaloupe"],
                "Proteins": ["tempeh", "quinoa", "chickpeas", "shrimp", "tuna", "edamame", "eggs", "tofu", "turkey", "black beans"],
                "Greens": ["arugula", "romaine", "bok choy", "asparagus", "zucchini", "green beans", "peas", "collard greens", "lettuce", "mustard greens"],
                "Healthy Fats": ["pumpkin seeds", "sunflower seeds", "hemp seeds", "almonds", "avocado", "macadamia nuts", "cashews", "hazelnuts", "olive oil", "ghee"]
            }, ["Excess sugar", "Alcohol", "Refined grains"],
            "The body begins preparing for ovulation. Energy and mental clarity often increase."),

            Phase("Ovulatory Phase", 15, 17, {
                "Fruits": ["raspberries", "pineapple", "grapefruit", "apricots", "nectarines", "melon", "grapes", "persimmon", "passionfruit", "lime"],
                "Proteins": ["turkey", "chicken breast", "tofu", "salmon", "edamame", "duck", "egg whites", "seitan", "lamb", "tuna"],
                "Greens": ["lettuce", "green beans", "peas", "cucumber", "okra", "kale", "spinach", "chard", "celery", "artichokes"],
                "Healthy Fats": ["olive oil", "macadamia nuts", "pecans", "hazelnuts", "almond butter", "pumpkin seeds", "flax oil", "avocado", "chia oil", "pine nuts"]
            }, ["Fried foods", "High sodium", "Soft drinks"]),

            Phase("Luteal Phase", 18, 29, {
                "Fruits": ["bananas", "figs", "dates", "mango", "plums", "apples", "cranberries", "dried apricots", "raisins", "grapes"],
                "Proteins": ["sardines", "red beans", "tempeh", "lean beef", "hummus", "chicken", "lentils", "split peas", "eggs", "tofu"],
                "Greens": ["brussels sprouts", "cauliflower", "leeks", "sweet potato", "beetroot", "carrots", "turnips", "kale", "green peas", "cabbage"],
                "Healthy Fats": ["dark chocolate", "peanut butter", "sesame seeds", "cashews", "pumpkin seeds", "walnuts", "sunflower butter", "ghee", "avocado", "coconut oil"]
            }, ["Salty snacks", "Heavy dairy", "Carbonated drinks"])
        ]

    def get_current_phase(self):
        today = datetime.today()
        days_since_start = (today - self.__user.get_cycle_start_date()).days
        cycle_day = (days_since_start % self.__user.get_cycle_length()) + 1

        # Loop through phases to find the current one — uses a for loop and conditional
        for phase in self.__phases:
            if phase.is_current_phase(cycle_day):
                return phase
        return None

    def get_user(self):
        return self.__user

# ===============================
# NutriCycleApp: user interaction logic + output
# ===============================
class NutriCycleApp:
    def __init__(self, user):
        self.__tracker = CycleTracker(user)

    def show_recommendations(self):
        current_phase = self.__tracker.get_current_phase()
        user = self.__tracker.get_user()

        if current_phase:
            print(f"\nUser: {user.get_name()}")
            print(f"Current Phase: {current_phase.get_name()}")

            # Demonstrate Inheritance: EducationalPhase includes extra info
            if isinstance(current_phase, EducationalPhase):
                print("Phase Info:", current_phase.get_info())

            filtered_recommendations = current_phase.get_filtered_recommendations(user.get_allergies())
            print("Recommended Foods:", ", ".join(filtered_recommendations) if filtered_recommendations else "No safe foods available")
            print("Foods to Avoid:", ", ".join(current_phase.get_avoid_list()))
        else:
            print("Could not determine the phase.")

# ===============================
# Predefined users stored using a dictionary
# ===============================
saved_users = {
    "baya": User("BAYA", "20-03-2025", 28, 5, UserPreferences([])),
    "ana": User("ANA", "18-03-2025", 29, 6, UserPreferences(["Sugar"])),
    "maïté": User("MAÏTÉ", "15-03-2025", 27, 4, UserPreferences(["Gluten"])),
    "margaux": User("MARGAUX", "22-03-2025", 30, 7, UserPreferences(["Dairy"]))
}

# ===============================
# Main loop (Loops + Conditionals)
# ===============================
while True:
    print("\n=== NutriCycle App ===")
    print("1. Create a new user")
    print("2. Load existing user")
    print("3. Exit")
    choice = input("Choose an option (1/2/3): ").strip()

    if choice == "1":
        # Loop through each field to allow user to confirm input
        while True:
            while True:
                name = input("Enter your name: ")
                if input(f"You entered: {name}. Is this correct? (yes/no): ").strip().lower() == "yes": break

            while True:
                cycle_start = input("Enter your last period start date (DD-MM-YYYY): ")
                if input(f"You entered: {cycle_start}. Is this correct? (yes/no): ").strip().lower() == "yes": break

            while True:
                cycle_length = int(input("Enter your cycle length in days: "))
                if input(f"You entered: {cycle_length}. Is this correct? (yes/no): ").strip().lower() == "yes": break

            while True:
                period_length = int(input("How many days does your period last? "))
                if input(f"You entered: {period_length}. Is this correct? (yes/no): ").strip().lower() == "yes": break

            while True:
                allergies = input("Enter any food allergies, separated by commas (or press enter if none): ").split(',')
                allergies = [a.strip() for a in allergies if a]
                if input(f"You entered: {', '.join(allergies) if allergies else 'None'}. Is this correct? (yes/no): ").strip().lower() == "yes": break

            new_user = User(name, cycle_start, cycle_length, period_length, UserPreferences(allergies))
            saved_users[name.lower()] = new_user
            app = NutriCycleApp(new_user)
            app.show_recommendations()
            break

    elif choice == "2":
        search = input("Enter the name of the user to load: ").strip().lower()
        if search in saved_users:
            app = NutriCycleApp(saved_users[search])
            app.show_recommendations()
        else:
            print("User not found. Try again or create a new user.")

    elif choice == "3":
        print("Exiting the app. Goodbye!")
        break

    else:
        print("Invalid option. Please enter 1, 2, or 3.")