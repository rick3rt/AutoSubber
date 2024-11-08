from cryptography.fernet import Fernet
import getpass
import json
import os


class CredentialManager:
    """
    CredentialManager is a class that manages the storage and retrieval of credentials
    using encryption for security. It handles the creation of encryption keys, loading
    and saving of encrypted credentials, and provides methods to add, list, and retrieve
    credentials.
    Attributes:
        filename (str): The path to the file where credentials are stored.
        key_file (str): The path to the file where the encryption key is stored.
        key (bytes): The encryption key used for encrypting and decrypting credentials.
        cipher (Fernet): The Fernet cipher object used for encryption and decryption.
        credentials (dict): A dictionary storing the credentials.
    Methods:
        __init__(filename="data/credentials.json"):
            Initializes the CredentialManager with the specified filename.
        load_key():
            Loads the encryption key from the key file, generating a new key if it doesn't exist.
        load_credentials():
            Loads and decrypts the credentials from the credentials file.
        save_credentials():
            Encrypts and saves the credentials to the credentials file.
        add_credential(username, password):
            Adds a new credential (username and password) to the credentials dictionary and saves it.
        list_credentials():
            Returns a list of all stored usernames.
        get_password(username):
            Retrieves the password for the specified username, or None if the username does not exist.
    """

    def __init__(self, filename="data/credentials.json"):
        self.filename = filename
        self.key_file = "data/key.key"
        self.key = self.load_key()
        self.cipher = Fernet(self.key)
        self.credentials = self.load_credentials()

    def load_key(self):
        # Generate and save a key if it doesn't exist
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as keyfile:
                keyfile.write(key)
        else:
            with open(self.key_file, "rb") as keyfile:
                key = keyfile.read()
        return key

    def load_credentials(self):
        # Load credentials from file if it exists
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                encrypted_data = file.read()
                if encrypted_data:
                    decrypted_data = self.cipher.decrypt(
                        encrypted_data.encode()
                    ).decode()
                    return json.loads(decrypted_data)
        return {}

    def save_credentials(self):
        # Encrypt and save credentials to file
        encrypted_data = self.cipher.encrypt(json.dumps(self.credentials).encode())
        with open(self.filename, "w") as file:
            file.write(encrypted_data.decode())

    def add_credential(self, username, password):
        self.credentials[username] = password
        self.save_credentials()

    def list_credentials(self):
        return list(self.credentials.keys())

    def get_password(self, username):
        return self.credentials.get(username, None)


# Test Interface
def main():
    manager = CredentialManager()

    while True:
        print("\nCredential Manager")
        print("1. Add Credential")
        print("2. List Credentials")
        print("3. Get Password")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            manager.add_credential(username, password)
            print(f"Credential for {username} added successfuly.")

        elif choice == "2":
            print("Stored Credentials:")
            for username in manager.list_credentials():
                print(username)

        elif choice == "3":
            username = input("Enter username to retrieve password: ")
            password = manager.get_password(username)
            if password:
                print(f"Password for {username}: {password}")
            else:
                print("Username not found.")

        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option, please choose again.")


if __name__ == "__main__":
    main()
