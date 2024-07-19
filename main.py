import random
import string
import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
import pickle


#function to generate the key for the access
def get_key():
    try:
        key = Fernet.generate_key()
        with open("key.key", "wb") as file:
            file.write(key)
        print("Key stored in key.key")
    except Exception as e:
        print(f"Error while the generation of the key: {e}")


#function for the load of the key , need it for the access an the encryption/decryption
def load_key():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            with open(file_path, "rb") as file:
                stored_key = file.read()
                return stored_key
        except FileNotFoundError:
            print(f"File {file_path} has not been found.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No file selected.")


#function for the encryption using the key
def encrypt_data(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password


#function for the decryption using the key
def decrypt_data(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password


#function for the generation of a random password (20 chars)
def generate_psw():
    try:
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(20))
        return password
    except Exception as e:
        print(f"Error while generating the  password: {e}")

#function to add the password to an hashmap then load the data in a file
def add_psw(key, hashmap):
    service = input("Input the service name: ")
    username = input("Input the username: ")
    c = input("Do you want to genereate a password? (y/n): ")
    password = generate_psw() if c == "y" else input(
        "Input the password to store: ")

    encrypted_username = encrypt_data(username, key)
    encrypted_password = encrypt_data(password, key)

    if service not in hashmap:
        hashmap[service] = [encrypted_username, encrypted_password]
    else:
        print("YOU CAN LOAD ONE PASSWORD FOR SERVICE. WAIT FOR UPCOMING UPDATE")
    try:
        #THIS IS THE FILE WHERE YOUR PASSWORDS ARE STORED
        with open('data.pkl', 'wb') as file:
            pickle.dump(hashmap, file)
    except Exception as e:
        print(f"ERROR OCCURED: {e} ")


def show_psw(key):
    try:
        #OPEN THE FILE WHERE PASSWORDS ARE STORED
        with open("data.pkl", "rb") as file:
            hashmap = pickle.load(file)
            for i in hashmap:
                decrypted_username = decrypt_data(hashmap[i][0], key)
                decrypted_password = decrypt_data(hashmap[i][1], key)
                print(f"Username: {decrypted_username}")
                print(f"Password: {decrypted_password}")

    except Exception as e:
        print(f"Error as: {e}")


def main():
    passwords = {}
    choice = input("Do you have the master key? (y/n): ").lower().strip()
    if choice == "n":
        get_key()
        key = load_key()
    else:
        key = load_key()

    if not key:
        print("no key loaded. exit.")
        return

    while True:
        print("Menu:")
        print("----------------------------------------------")
        print("1. Add new password")
        print("2. Show all passwords")
        print("3. Exit")
        try:
            choice2 = int(input("Input your choice: "))
            if choice2 == 1:
                add_psw(key, passwords)
            elif choice2 == 2:
                show_psw(key)
            elif choice2 == 3:
                break
            else:
                print("Choice not valid.")
        except ValueError:
            print("Error: input a valid number.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
