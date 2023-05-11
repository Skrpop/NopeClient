import requests
import socketio

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

@sio.on("list:tournaments")
def listtournamenst(data):
    print(data)


def create_tournament(num_best_of_matches):
    sio.emit('tournament:create', num_best_of_matches, callback=on_tournament_created)


def join_tournament(tournament_id):
    sio.emit('tournament:join',  tournament_id, callback=on_tournament_joined)


def leave_tournament():
    sio.emit('tournament:leave', callback=on_tournament_left)


def start_tournament():
    sio.emit('tournament:start', callback=on_tournament_started)


def on_tournament_created(data):
    if data['success']:
        print("Tournament created. Tournament ID:", data['data']['tournamentId'])
    else:
        print("Tournament creation failed. Error:", data['error']['message'])


def on_tournament_joined(data):
    if data['success']:
        print("Joined tournament. Tournament ID:")
    else:
        print("Failed to join tournament. Error:", data['error']['message'])


def on_tournament_left(data):
    if data['success']:
        print("Left tournament.")
    else:
        print("Failed to leave tournament. Error:", data['error']['message'])


def on_tournament_started(data):
    if data['success']:
        print("Tournament started.")
    else:
        print("Failed to start tournament. Error:", data['error']['message'])


def login(username, password):
    data = {"username": username, "password": password}
    url = 'https://nope-server.azurewebsites.net/api/auth/login'
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()['accessToken']
    else:
        return None


def register(username, password, firstname, lastname):
    data = {"username": username, "password": password, "firstname": firstname, "lastname": lastname}
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

                sio.connect('https://nope-server.azurewebsites.net', auth={'token': accessToken})

                while True:
                    print("\nPlease choose an option:")
                    print("1. List Tournaments")
                    print("2. Create Tournament")
                    print("3. Join Tournament")
                    print("4. Leave Tournament")
                    print("5. Start Tournament")
                    print("6. Quit")
                    choice = input("Enter the number (1 to 6): ")

                    if choice == '1':

                        pass
                    elif choice == '2':
                        num_best_of_matches = int(
                            input("Enter the number of best of matches (odd number, n > 2 and n < 8): "))
                        create_tournament(num_best_of_matches)
                    elif choice == '3':
                        tournament_id = input("Enter the tournament ID: ")
                        join_tournament(tournament_id)
                    elif choice == '4':
                        leave_tournament()
                    elif choice == '5':
                        start_tournament()
                    elif choice == '6':
                        sio.disconnect()
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 6.")
                else:
                    print("Login failed! Please try again.")
        elif choice == '2':
            firstname = input("Enter your first name: ")
            lastname = input("Enter your last name: ")
            if register(username, password, firstname, lastname):
                print("Registration successful! You can now log in.")
            else:
                print("Registration failed! Please try again.")
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
