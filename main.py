import os
import random
import time
from textwrap import dedent

# For resolving the issue with missing dll file while importing the vlc module.
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import vlc

# CHANGE TO YOUR PATH HERE
os.chdir(r'E:\MUSIC\Something')

def print_menu() -> None:
    message = dedent("""
        Choices:
        1. Play clip again
        2. Play another clip and reveal the current music track name
        3. Quit
    """)
    print(message)

class MusicPlayer:
    def __init__(self, segment_length: int|float=5):
        self.segment_length = segment_length
    
    def construct_segment(self, file_path: str) -> None:
        """
        Constructs a `segment_length` second segment of the music file given by `file_path`.
        
        Arguments:
            file_path: The relative or absolute path of the music file.
        """
        # Create VLC media player instance
        self.player = vlc.MediaPlayer()

        # Load the mp3 file
        self.media = vlc.Media(file_path)
        self.player.set_media(self.media)

        # Get the file duration in milliseconds
        # Needs to played for a few milliseconds otherwise the duration becomes -1
        self.player.play()
        time.sleep(0.5)
        duration = self.player.get_length()
        self.player.stop()

        # Calculate the start time of the random segment
        start_time = random.randint(0, duration - self.segment_length * 1000)
        self.media.add_option(f":start-time={start_time // 1000}")
        self.media.add_option(f":stop-time={(start_time + self.segment_length * 1000) // 1000}")
        
    def play_file_segment(self) -> None:
        """
        Plays the constructed music segment.
        """
        self.player.set_media(self.media)
        self.player.play()
        time.sleep(self.segment_length)
        self.player.stop()
  
if __name__ == '__main__':
    # Find the name of all the files.
    media_files = []
    for root, folders, files in os.walk(os.getcwd()):
        for file in list(files):
            if not file.endswith('.mp3'):
                continue
            file_name = os.path.join(root, file)
            media_files.append(file_name)
            
    player = MusicPlayer(segment_length=1)
  
    while True:
        # Now get an random file name and format it to get the file name from the absolute path.
        media_file = random.choice(media_files)
        media_file_name = media_file.split('.')[0].split('\\')[-1]

        # Now play the random segment.
        player.construct_segment(file_path=media_file)
        player.play_file_segment()

        # Display the menu once per track.
        print_menu()
        
        choice = None
        while choice not in ['1', '2', '3']:
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                print('Ok, playing the clip again...')
                player.play_file_segment()
                choice = None
            elif choice == '3':
                break
            elif choice != '2':
                print('invalid entry.')
                
        print(f'The name of the track is \'{media_file_name}\'')
        if choice != '3':
            input('Press enter to move on! ')

        if choice == '3':
            print('Exiting...')
            break