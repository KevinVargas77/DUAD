import csv

def export_csv(video_games):
    with open('video_games.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "genre", "developer", "ESRB_rating"])
        writer.writeheader()
        writer.writerows(video_games)


def export_csv_tabs(video_games):
    with open('video_games_tabs.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "genre", "developer", "ESRB_rating"], delimiter='\t')
        writer.writeheader()
        writer.writerows(video_games)


def create_video_game():
    game = {
        "name": vg_name(),
        "genre": vg_genre(),
        "developer": vg_developer(),
        "ESRB_rating": vg_ESRB_rating()
    }
    return game


def vg_name():
    try:
        name = input('Please enter the video game name: ')
        if name == "":
            raise ValueError("Field cannot be empty.")
        return name
    except ValueError as e:
        print(f"Error: {e}")
        return vg_name()


def vg_genre():
    try:
        genre = input('Please enter the genre: ')
        if genre == "":
            raise ValueError("Field cannot be empty.")
        return genre
    except ValueError as e:
        print(f"Error: {e}")
        return vg_genre()


def vg_developer():
    try:
        developer = input('Please enter the video game developer: ')
        if developer == "":
            raise ValueError("Field cannot be empty.")
        return developer
    except ValueError as e:
        print(f"Error: {e}")
        return vg_developer()


def vg_ESRB_rating():
    valid_ratings = ["E", "T", "M", "AO", "RP"]
    while True:
        rating = input('Please enter the ESRB rating:\n'
                       'E - Everyone\n'
                       'T - Teen\n'
                       'M - Mature\n'
                       'AO - Adults Only\n'
                       'RP - Rating Pending\n'
                       'Your choice: ').upper()

        if rating in valid_ratings:
            return rating
        else:
            print("Invalid rating, please choose from the list.")


def enter_vg(video_games):
    while True:
        try:
            count = int(input("Enter the number of video games to add: "))
            if count <= 0:
                print("Please enter a positive number greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid positive number.")

    for i in range(count):
        print(f"\nEntering details for video game {i + 1}:")
        video_game = create_video_game()
        video_games.append(video_game)

    print("\nVideo games registered:")
    for game in video_games:
        print(game)


def saving_csv(video_games):
    while True:
        save = input("Do you want to save your video games to a CSV file now? (yes/no): ").lower()
        if save == "yes":
            format_choice = input("Choose format: (1) Commas (2) Tabs: ")
            if format_choice == "1":
                export_csv(video_games)
                print("Video games saved with commas.")
            elif format_choice == "2":
                export_csv_tabs(video_games)
                print("Video games saved with tabs.")
            else:
                print("Invalid choice. Saving with commas by default.")
                export_csv(video_games)
            break
        elif save == "no":
            enter_vg(video_games)
        else:
            print("Please enter 'yes' or 'no'.")


def main():
    """=== Video Games Register ==="""
    video_games = []
    enter_vg(video_games)
    saving_csv(video_games)


if __name__ == "__main__":
    main()
