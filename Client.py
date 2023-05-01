import requests
import socketio

def login(username, password):
    data = {"username": username, "password": password}
    url = 'https://nope-server.azurewebsites.net/api/auth/login'
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()['accessToken']
    else:
        return None

def register(username, password):
    data = {"username": username, "password": password}
    url = 'https://nope-server.azurewebsites.net/api/auth/register'
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return True
    else:
        return False

def main():
    print("Welcome to the Console Menu")

    while True:
        print("Please choose an option:")
        print("1. Login")
        print("2. Register")
        choice = input("Enter the number (1 or 2): ")

        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if choice == '1':
            accessToken = login(username, password)

            if accessToken:
                print("Login successful! Access token:", accessToken)

                sio = socketio.Client()

                @sio.event
                def connect():
                    print("Connected")

                @sio.event
                def list_tournaments(data):
                    print("List of tournaments: ", data)

                @sio.event
                def tournament_playerInfo(data):
                    print("Tournament player info: ", data)

                @sio.event
                def tournament_info(data):
                    print("Tournament info: ", data)

                @sio.event
                def disconnect():
                    print("Disconnected")

                sio.connect('https://nope-server.azurewebsites.net', auth={'token': accessToken})

                # Add your event emissions here
                # Example of emitting a tournament:create event
                sio.emit("tournament:create", {"numBestOfMatches": 3})

                # Example of emitting a tournament:join event
                sio.emit("tournament:join", {"tournamentId": "your_tournament_id"})

                # Example of emitting a tournament:leave event
                sio.emit("tournament:leave")

                # Example of emitting a tournament:start event
                sio.emit("tournament:start")

                sio.wait()

                break
            else:
                print("Login failed! Please try again.")
        elif choice == '2':
            if register(username, password):
                print("Registration successful! You can now log in.")
            else:
                print("Registration failed! Please try again.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
