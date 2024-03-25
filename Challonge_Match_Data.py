import challonge
import csv

# Function to read API keys and usernames from a file
def read_usernames_and_api_keys(file_path):
    usernames_api_keys = []
    with open(file_path, 'r') as file:
        for line in file:
            username, api_key = line.strip().split(',')
            usernames_api_keys.append((username.strip(), api_key.strip()))
    return usernames_api_keys

# Function to display usernames in a numbered list
def display_usernames(usernames_api_keys):
    print("User Names:")
    for i, (username, _) in enumerate(usernames_api_keys, start=1):
        print(f"{i}. {username}")
    print()

# Function to retrieve tournament IDs and names associated with a username
def get_tournament_info(username, api_key):
    try:
        tournaments = challonge.tournaments.index(created_by=username, api_key=api_key)
        return [(tournament['id'], tournament['name']) for tournament in tournaments]
    except challonge.ChallongeException as e:
        print(f"Error: {e}")
        return []

# Function to display tournament IDs and names
def display_tournament_info(tournament_info):
    print("Tournament IDs:")
    for i, (tournament_id, tournament_name) in enumerate(tournament_info, start=1):
        print(f"{i}. {tournament_id}: {tournament_name}")
    print()
    
# Function to export match information to a CSV file
def export_match_info(matches, file_path, tournament_id, api_key):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Match Winner', 'Match Loser', 'Winner Score', 'Loser Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for match in matches:
            winner_id = match['winner_id']
            loser_id = match['loser_id']
            winner_score = ''
            loser_score = ''
            if 'scores_csv' in match:
                scores = match['scores_csv'].split('-')
                if len(scores) >= 2:
                    if scores[0] > scores[1]:
                        winner_score = scores[0]
                        loser_score = scores[1]
                    else:
                        winner_score = scores[1]
                        loser_score = scores[0]
            try:
                winner_info = challonge.participants.show(tournament_id, winner_id, api_key=api_key) if winner_id is not None else {'name': str(winner_id)}
            except Exception as e:
                print(f"Error fetching winner information: {e}")
                winner_info = {'name': str(winner_id)}
            try:
                loser_info = challonge.participants.show(tournament_id, loser_id, api_key=api_key) if loser_id is not None else {'name': str(loser_id)}
            except Exception as e:
                print(f"Error fetching loser information: {e}")
                loser_info = {'name': str(loser_id)}
            writer.writerow({'Match Winner': winner_info['name'], 'Match Loser': loser_info['name'], 'Winner Score': winner_score, 'Loser Score': loser_score})



# Step 1: Read API keys and usernames from a file
usernames_api_keys = read_usernames_and_api_keys("api_keys.txt")

# Step 2: Display the usernames in a numbered list
display_usernames(usernames_api_keys)

# Step 3: Prompt the user to enter the number corresponding to the desired username
user_choice = int(input("Enter User Number: "))
selected_username, selected_api_key = usernames_api_keys[user_choice - 1]

# Step 4: Retrieve the tournament IDs and names associated with the selected username
tournament_info = get_tournament_info(selected_username, selected_api_key)

# Step 5: Display the tournament IDs and names for the selected username
display_tournament_info(tournament_info)

# Step 6: Prompt the user to enter the number corresponding to the desired tournament ID
tournament_choice = int(input("Enter Tournament Number: "))
selected_tournament_id, selected_tournament_name = tournament_info[tournament_choice - 1]

# Step 7: Retrieve matches for the selected tournament ID
try:
    matches = challonge.matches.index(selected_tournament_id, api_key=selected_api_key)
    # Step 8: Export match information to a CSV file
    export_match_info(matches, 'match_info.csv', selected_tournament_id, selected_api_key)
    print("Match information exported successfully.")
except challonge.ChallongeException as e:
    print(f"Error: {e}")
