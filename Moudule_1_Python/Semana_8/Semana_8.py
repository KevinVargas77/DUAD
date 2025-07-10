import os


def load_lyrics(file_list):
    lyrics = []
    lyrics_names = []
    for file_name in file_list:
        with open(file_name, "r") as file:
            content = file.read()
            lyrics.append(content)
        
        base_name = os.path.basename(file_name)    
        clean_name = base_name.split("_", 1)[1].replace(".txt", "")
        lyrics_names.append(clean_name)
    return lyrics, lyrics_names


def show_lyrics(lyrics, song_number):
    if 0 <= song_number < len(lyrics): 
        print(f'\nSong lyric of the song #{song_number +1}:\n')
        print(lyrics[song_number])


def all_songs(lyrics_names, output_file): 
    sorted_list = sorted(lyrics_names)
    
    with open(output_file, "w", encoding="utf-8") as file:
        for lyric in sorted_list:
            file.write(lyric + "\n")
    
    with open(output_file, "r", encoding="utf-8") as file:
        content = file.read()
    
    return content


def lyrics_menu(lyrics_names):
    for i, name in enumerate(lyrics_names):
        print(f"{i+1}. {name}")


def main():
    folder = "Pearl_Jam_Ten"
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".txt")]

    lyrics, lyrics_names = load_lyrics(file_list)

    sorted_content = all_songs(lyrics_names, "all_songs_sorted.txt")

    print("This is the sorted list of all the songs:\n")
    print(sorted_content)

    print("Which song's lyrics do you want to read?")
    lyrics_menu(lyrics_names)
    choice = int(input("\nEnter the song number: ")) - 1

    show_lyrics(lyrics, choice)


main()
