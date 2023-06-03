import os
import random
import time

# For resolving the issue with missing dll file while importing the vlc module.
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import vlc

# CHANGE TO YOUR PATH HERE
os.chdir(r'E:\MUSIC\Something')

GUESSING_TIME: int = 3

def play_random_segment(file_path: str, segment_length: int = 5) -> None:
  """
  Plays a random `segment_length` second clop of the music file `file_path`.
  
  file_path: The absolute or relative path of the music file to be played.
  semgnet_length: The number of seconds to play.
  """
  # Create VLC media player instance
  player = vlc.MediaPlayer()
  
  # Load the mp3 file
  media = vlc.Media(file_path)
  player.set_media(media)
  
  # Get the file duration in milliseconds
  # Needs to played for a few milliseconds otherwise the duration becomes -1
  player.play()
  time.sleep(0.5)
  duration = player.get_length()
  player.stop()
  
  # Calculate the start time of the random segment
  start_time = random.randint(0, duration - segment_length * 1000)
  media.add_option(f":start-time={start_time // 1000}")
  media.add_option(f":stop-time={(start_time + segment_length * 1000) // 1000}")
  
  # Now play the file.
  player.set_media(media)
  player.play()
  time.sleep(segment_length)
  player.stop()
  
if __name__ == '__main__':
  # Find the name of all the files.
  media_files = []
  for root, folders, files in os.walk(os.getcwd()):
    for file in list(files):
      if not file.endswith('.mp3'):
        continue
      file_name = os.path.join(root, file)
      media_files.append(file_name)
  
  while True:
    # Now get an random file name and format it to get the file name from the absolute path.
    media_file = random.choice(media_files)
    media_file_name = media_file.split('.')[0].split('\\')[-1]
    
    # Now play the random segment.
    play_random_segment(file_path=media_file, segment_length=2)
    
    print(f'You have {GUESSING_TIME} seconds to guess the name!')
    time.sleep(GUESSING_TIME)
    
    print(f'The name of the track is \'{media_file_name}\'')
    
    choice = None
    while choice not in ['Y', 'N']:
      choice = input("Play again? (Y/N): ").strip().upper()
      if choice == 'N':
        print('')
        break
      elif choice != 'Y':
        print("Invalid choice. Please enter Y or N.")
    
    if choice == 'N':
        break