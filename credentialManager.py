from cryptography.fernet import Fernet
import json
import os


class CredentialManager:
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
            password = input("Enter password: ")
            manager.add_credential(username, password)
            print(f"Credential for {username} added successfully.")

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
