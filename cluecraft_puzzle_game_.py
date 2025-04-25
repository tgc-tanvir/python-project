from pathlib import Path
import os

def user() :
  print("1. Register")
  print("2. Log In")
  user_choice = input("Write 1 or 2 : ")
  if user_choice == "1" :
    Register()
  elif user_choice == "2" :
    Log_in()
  else :
    print("Invalid input")


#Admin Part.....................................................................
def Admin() :
    print("Admin")
    file_path = "/content"

    file_names = [file for file in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, file))]

    print(file_names)

    username = input("Enter which file you want to edit or delete : ")
    if username == "" :
      print("Invalid Input")
      Admin()
      return
    file_path = Path(username)

    if not file_path.exists():
      print("Username not found")
      Admin()
      return
    print("1. Edit")
    print("2. Delete")
    print("3. Exit")
    user_choice = input("Write 1 or 2 : ")
    if user_choice == "1" :
      with open(username, 'r') as file:
        lines = file.readlines()
        user_data = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in lines}
        print(user_data)
        user_data["Username"] = input("Username : ")
        user_data["Email"] = input("Email : ")
        user_data["Password"] = input("Password : ")
        user_data["Role"] = input("Role : ")
        with open(username, 'w') as file:
          for key, value in user_data.items():
            file.write(f"{key}: {value}\n")
            print("File edited successfully!")
        Admin()
    elif user_choice == "2":
      os.remove(username)
      print("File deleted successfully!")
      Admin()
    elif user_choice == "3":
      user()
    else:
      print("Invalid input")
      Admin()
      return



#Register part..................................................................
def Register() :
    print("Register")
    username = input("Enter username : ")
    email= input("Enter email : ")
    password = input("Enter password : ")
    role = "User"
    file_path = Path(username)
    if username == "" or email == "" or password == "" or file_path.exists() :
      print("Username is already taken or Invalid Input")
      Register()
      return

    with open(username, 'w') as file:
      file.write(f"Username : {username}\n")
      file.write(f"Email : {email}\n")
      file.write(f"Password : {password}\n")
      file.write(f"Score : {0}\n")
      file.write(f"Role : {role}\n")
    print("Registration successful!")
    user()

#Log In Part.....................................................................
def Log_in():
    print("Log In")
    username = input("Enter username : ")
    password = input("Enter password : ")

    if username == "" or password == "" :
      print("Invalid Input")
      Log_in()
      return

    file_path = Path(username)

    if not file_path.exists():
      print("Username not found")
      Log_in()
      return

    with open(username, 'r') as file:
      lines = file.readlines()
      user_data = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in lines}

      stored_username = user_data.get("Username")
      stored_email = user_data.get("Email")
      stored_password = user_data.get("Password")
      stored_score = user_data.get("Score")
      stored_role = user_data.get("Role")

      if stored_password == password:
        if stored_role == "admin":
            Admin()
        else:
            print("Login successful!")
            print("Name :" + username)
            print("Email :" + stored_email)
            print(f"Score: {stored_score}")

            cluecraft_puzzle(stored_username,stored_score)
            return
      else:
            print("Incorrect password")
            Log_in()
            return

    print("Incorrect username or password")
    Log_in()

#FIle rewrite with updated score............

def update_score(username, new_score):
    with open(username, 'r') as file:
       lines = file.readlines()
    for i in range(len(lines)):
       if "Score" in lines[i]:
         lines[i] = f"Score : {new_score}\n"
         break
    with open(username, 'w') as file:
      file.writelines(lines)
      print("Score : " + str(new_score))



#The game part starts from here....................................................

#Desplay the cluecraft..........
def display_grid(grid):
    """Display the Clue Craft grid."""
    for row in grid:
        print(" ".join(row))
    print()


def cluecraft_puzzle(username,score):
    user_score = int(score)
    ans = False
    print("Welcome to the Clue Craft Puzzle Game!")
    print("Fill in the blanks in the grid with the correct words.")
    print("Use the clues provided to guess the correct words.\n")

    grid = [
        ['c', '_', '_', 'p', '_', '_', 's'],
        ['_', '_', '_', 'a', '_', '_', '_'],
        ['_', 'o', '_', '_', 'n', '_', 'y'],
        ['_', '_', '_', 'k', '_', '_', '_'],
        ['_', 'e', '_', 'i', 'c', '_', 'e'],
        ['_', '_', '_', '_', '_', '_', '_'],
        ['_', 'u', '_', '_', 'e', 'r', '_']
    ]

    solution = [
        ['c', 'o', 'm', 'p', 'a', 's', 's'],
        ['_', '_', '_', 'a', '_', 'm', '_'],
        ['j', 'o', 'u', 'r', 'n', 'e', 'y'],
        ['_', '_', '_', 'k', '_', 'l', '_'],
        ['v', 'e', 'h', 'i', 'c', 'l', 'e'],
        ['_', '_', '_', 'n', '_', 'e', '_'],
        ['s', 'u', 'r', 'g', 'e', 'r', 'y'],
    ]

#Restricted rows & columns..........
    restricted_rows = [1, 3, 5]
    restricted_columns = [0, 1, 2, 4, 6]
    print("Here is your cluecraft puzzle:")
    display_grid(grid)

    print("Clues:")
    print("1. Row 1: Device for finding directions.")
    print("2. Column 3: Place to leave your car temporarily.")
    print("3. Row 3: A trip or voyage from one place to another.")
    print("4. Row 5: A means of transport on wheels.")
    print("5. Column 6: A keen nose, or someone who detects scents.")
    print("6. Row 7: Medical procedure performed by a doctor.")


    for attempt in range(1, 12):
        input_data = input("Enter direction and number (e.g., 'row 1' or 'column 3'): ").strip().lower()

        if "row" in input_data:
            direction = "row"
        elif "column" in input_data:
            direction = "column"
        elif "exit" in input_data:
            print("Your score is : " + str(user_score))
            print("Exiting the game.")
            print("Thank you for playing Clue Craft game.")
            return
        else:
            print("Invalid input! Please enter 'row <number>' or 'column <number>'.")
            continue

#Data taking from user & placing them in the cluecraft..........
        try:
            index = int(input_data.split()[1]) - 1
        except (IndexError, ValueError):
            print("Invalid format! Please use 'row <number>' or 'column <number>'.")
            continue

        if (direction == "row" and index in restricted_rows) or (direction == "column" and index in restricted_columns):
            print(f"Sorry, you cannot fill in row {index+1} or column {index+1}. Try a different one.\n")
            continue

        word = input("Enter the missing letters serially: ").lower()
        if word == "exit":
            print("Your score is : " + str(user_score))
            print("Exiting the game.")
            print("Thank you for playing Clue Craft game.")
            return

        if direction == 'row':
            col_index = 0
            for i in range(len(grid[index])):
                if grid[index][i] == '_':
                  if solution[index][i] == word[col_index]:
                    grid[index][i] = word[col_index]
                    col_index += 1
                    ans = True

                  else :
                    print(f"Incorrect word! Try again.\n")
                    ans = False
                    break
            if ans == True :
              user_score += 5
              update_score(username,user_score)
            else :
              user_score -= 5
              update_score(username,user_score)
              continue

        elif direction == 'column':
            row_index = 0
            for i in range(len(grid)):
                if grid[i][index] == '_':
                  if solution[i][index] == word[row_index]:
                    grid[i][index] = word[row_index]
                    row_index += 1
                    ans = True
                  else :
                    print(f"Incorrect word! Try again.\n")
                    ans = False
                    break
            if ans == True :
              user_score += 5
              update_score(username,user_score)
            else :
              user_score -= 5
              update_score(username,user_score)
              continue


        display_grid(grid)

        if grid == solution:
            print("Congratulations! You've completed the Clue Craft puzzle!")
            return

    print("Sorry, you've used all attempts! Here's the solution:")
    display_grid(solution)



#Main function calling part.....................................................

user()