import pygame
import os

# Initialize mixer
pygame.mixer.init()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
assets_dir = os.path.join(project_root, "assets")

music_files = [
    os.path.join(assets_dir, "AyraStar_Music.wav"),
    os.path.join(assets_dir, "Cr&AS_Ngozi_Music.wav"),
    os.path.join(assets_dir, "DarkooFtRema_Music.wav"),
    os.path.join(assets_dir, "MohBad_Music.wav"),
    os.path.join(assets_dir, "music.wav"),
    os.path.join(assets_dir, "Teni_Malaika_Music.wav")
]

current_track_index = 0

def play_music():
    global current_track_index
    try:
        pygame.mixer.music.load(music_files[current_track_index])
        pygame.mixer.music.play()
        print(f"Now playing: {os.path.basename(music_files[current_track_index])}")
    except Exception as e:
        print(f"Error playing music: {e}")

def stop_music():
    pygame.mixer.music.stop()
    print("Music stopped.")

def next_track():
    global current_track_index
    current_track_index = (current_track_index + 1) % len(music_files)
    play_music()

def previous_track():
    global current_track_index
    current_track_index = (current_track_index - 1) % len(music_files)
    play_music()

if __name__ == "__main__":
    #print("Testing music paths:")
    for track in music_files:
        print(track)

    while True:
        #print("\nCommands: [P]lay, [S]top, [N]ext, [B]ack, [Q]uit")
        command = input("Enter command: ").strip().lower()

        if command == "p":
            play_music()
        elif command == "s":
            stop_music()
        elif command == "n":
            next_track()
        elif command == "b":
            previous_track()
        elif command == "q":
            stop_music()
            break
        else:
            print("Invalid command.")
