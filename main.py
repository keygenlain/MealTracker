import sqlite3
import sys
import random
con = sqlite3.connect("meals.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS meals (name TEXT NOT NULL, date TEXT NOT NULL)")
cur.execute("SELECT * FROM meals")
# Actually does stuff
def main():
    while True:
        print("Meal Tracker\n\n1. Add Meal\n2. List Meals\n3. Exit")
        choice = input() # Grabs the user's choice
        match choice:
            case "1":
                add_meal()
            case "2":
                list_meals()
            case "3":
                sys.exit()
# Adds a meal based on a name and date given by the user
def add_meal():
    print("Enter the name of the meal.")
    meal_name = input()
    print("Now, enter the date you ate it on.")
    meal_date = input()
    sql_update_meals(meal_name, meal_date) # Updates the SQLite DB
def list_meals():
    cur.execute("SELECT name, date FROM meals")
    meals = cur.fetchall()
    for meal in meals:
        print(meal) # Recursively prints meals on the list until there are none left
def sql_update_meals(name, date):
    add_meal_query = "INSERT INTO meals (id, name, date) VALUES (?, ?, ?)"
    cur.execute(add_meal_query, (name, date))
    con.commit() # Actually commits to the DB
main() # Runs the program