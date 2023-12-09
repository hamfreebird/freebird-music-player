"""by freebird"""

import os

setting_list = ["" for _ in range(0, 3)]
setting_index = 0
use_setting_film = True
setting = open("setting.txt", "r")
for set_num in setting:
	setting_list[setting_index] = set_num
	setting_index += 1
music_path_set = str(setting_list[1][14:len(setting_list[1]) - 2])
setting.close()

if music_path_set == "":
	music_list = os.listdir(path = 'music')
else:
	music_list = os.listdir(path = music_path_set)
	
introduction = open("introduction.txt", "w")
for line in music_list:
	introduction.write(line + "\n")
introduction.close()