import json
import os
import hashlib

class BackendSystem:
    def __init__(self):
        self.db_file = "database.json"
        
        self.master_library = [
            {"title": "The Hobbit", "genre": "Fantasy"},
            {"title": "Harry Potter", "genre": "Fantasy"},
            {"title": "Dune", "genre": "Sci-Fi"},
            {"title": "Foundation", "genre": "Sci-Fi"},
            {"title": "1984", "genre": "Dystopian"},
            {"title": "Brave New World", "genre": "Dystopian"}
        ]
        self.data = self.load_db()

    def load_db(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {"users": {}, "collections": {}}

    def save_db(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        if username in self.data["users"]:
            return False, "User already exists!"
        self.data["users"][username] = self.hash_password(password)
        self.data["collections"][username] = []
        self.save_db()
        return True, "Account created!"

    def login(self, username, password):
        hashed = self.hash_password(password)
        if username in self.data["users"] and self.data["users"][username] == hashed:
            return True
        return False

    def add_book(self, username, title, genre):
        book = {"title": title, "genre": genre.capitalize()}
        self.data["collections"][username].append(book)
        self.save_db()


system = BackendSystem()
current_user = None

while True:
    if not current_user:
        print("\n--- SYSTEM ACCESS ---")
        choice = input("1. Login | 2. Register | 3. Exit: ")
        
        if choice == '1':
            user = input("Username: ").strip()
            pw = input("Password: ").strip()
            if system.login(user, pw):
                current_user = user
                print(f"Login successful! Welcome.")
            else:
                print("Error: Invalid credentials.")
        
        elif choice == '2':
            user = input("New Username: ").strip()
            pw = input("New Password: ").strip()
            success, msg = system.register(user, pw)
            print(msg)
            
        elif choice == '3':
            break
    else:
        print(f"\n--- {current_user.upper()}'S BOOKSHELF ---")
        print("1. View My Books | 2. Add Book | 3. Discover/Recommend | 4. Logout")
        action = input("Select action: ")

        if action == '1':
            books = system.data["collections"][current_user]
            if not books:
                print("Your shelf is empty.")
            else:
                for b in books: print(f" - {b['title']} [{b['genre']}]")

        elif action == '2':
            title = input("Title: ")
            genre = input("Genre: ")
            system.add_book(current_user, title, genre)
            print(f"'{title}' added!")

        elif action == '3':
            print("\n--- DISCOVERY MENU ---")
            print("1. Show Master Library (All Books)")
            print("2. Get Recommendations by Genre")
            sub_choice = input("Select: ")

            if sub_choice == '1':
                print("\n[ FULL MASTER LIBRARY ]")
                for book in system.master_library:
                    print(f" - {book['title']} ({book['genre']})")

            elif sub_choice == '2':
                print("\nPick a genre:")
                print("1. Fantasy | 2. Sci-Fi | 3. Dystopian | 4. Other")
                genre_num = input("Choice: ")
                
                target_genre = ""
                if genre_num == '1': target_genre = "Fantasy"
                elif genre_num == '2': target_genre = "Sci-Fi"
                elif genre_num == '3': target_genre = "Dystopian"
                elif genre_num == '4': target_genre = input("Enter genre: ").capitalize()

                if target_genre:
                    recs = [b['title'] for b in system.master_library if b['genre'] == target_genre]
                    print(f"\nRecommendations for {target_genre}:")
                    if recs:
                        for rec in recs: print(f" - {rec}")
                    else:
                        print("No books found for that genre.")
            else:
                print("Invalid choice.")

        elif action == '4':
            current_user = None