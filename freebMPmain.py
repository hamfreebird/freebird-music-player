# -*- coding: utf-8 -*-
"""freebird music player -> main"""

import os
import sys
import time
import pygame
from pygame.mixer import music
from pygame.mixer import init as mixer_init  # 用于初始化音乐模块
from pygame.colordict import THECOLORS       # pygame的颜色列表
from pygame.font import Font
from freepygame import freetext, freebutton
from _io import text_encoding
import mutagen
global music_lrc_line_len

text_encoding("utf-8")

# 导入设置文件
setting_list = ["" for _ in range(0, 3)]
setting_index = 0
use_setting_film = True
setting = open("setting.txt", "r")
for set_num in setting:
	setting_list[setting_index] = set_num
	setting_index += 1
dsm = 1  # 界面放大倍数
display_size = (720 * dsm, 480 * dsm)
music_path_set = str(setting_list[1][14:len(setting_list[1]) - 2])
music_lrc_path_set = str(setting_list[2][18:len(setting_list[2]) - 2])
setting.close()

# 导入日志文件
freelog = open("freelog.txt", "a+")
freelog.write("\n" + str(time.localtime()))
freelog.write("\n" + str(format(time.time(), ".5f")) + "   Open log file\n")

# 初始化
pygame.init()
mixer_init(frequency = 44100)  # 音乐模块的初始化
frame_number = 60
pygame.display.set_caption("freebird music player")
pygame.display.set_icon(pygame.image.load("assets\\freebird_music.ico"))
text_font = Font("assets\\AiNiPoSui-ShengGuoWanMei-2.ttf", 20)
pg_wind_music1 = pygame.image.load("assets\\wind_music.JPG")
pg_wind_music2 = pygame.image.load("assets\\wind_music2.JPG")
pg_wind_music3 = pygame.image.load("assets\\wind_music3.jpg")
pg_wind_music1_r = pygame.image.load("assets\\wind_music_r.JPG")
pg_wind_music2_r = pygame.image.load("assets\\wind_music2_r.JPG")
pg_wind_music3_r = pygame.image.load("assets\\wind_music3_r.jpg")
pg_wind_music = [pg_wind_music1, pg_wind_music2, pg_wind_music3]
pg_wind_music_r = [pg_wind_music1_r, pg_wind_music2_r, pg_wind_music3_r]
pg_wind_color = [(0, 105, 70), (0, 20, 105), (137, 30, 0)]
pg_wind_music_index = 3
screen = pygame.display.set_mode(display_size)
screen.blit(pg_wind_music[2], (0, 0))
clock = pygame.time.Clock()
MUSICOVER = pygame.USEREVENT  # 当音乐播放完成时的信号
music.set_endevent(MUSICOVER)
freelog.write(str(format(time.time(), ".5f")) + "   pygame : And the initialization\n")

# 需要显示的可交互的元素
event_text = freetext.SuperText(screen, [3, 5], "", size = 10, color = THECOLORS.get("grey70"), dsm = dsm)
music_name_text = freetext.SuperText(screen, [3, 20], "文件名称 -> ", size = 15, color = THECOLORS.get("grey80"), dsm = dsm)
vol_text = freetext.SuperText(screen, (display_size[0] - 73, 50), "音量", size = 20, color = THECOLORS.get("grey80"), dsm = dsm)
vol_num = freetext.SuperText(screen, (display_size[0] - 73, 70), "", color = THECOLORS.get("grey80"), dsm = dsm)
time_text = freetext.SuperText(screen, (display_size[0] - 73, 100), "时间", size = 20, color = THECOLORS.get("grey80"), dsm = dsm)
time_num = freetext.SuperText(screen, (display_size[0] - 73, 120), "", color = THECOLORS.get("grey80"), dsm = dsm)
freebird_text = freetext.SuperText(screen, (display_size[0] - 95, display_size[1] - 30), "by freebird",
                                   text_font, color = THECOLORS.get("grey100"), dsm = dsm)
pleiades_text = freetext.SuperText(screen, (10, display_size[1] - 50), "Wishing well", text_font, color = THECOLORS.get("grey100"), dsm = dsm)
version_text = freetext.SuperText(screen, (10, display_size[1] - 20), "v 1.2.0", size = 15, color = THECOLORS.get("grey95"), dsm = dsm)
music_name = freetext.SuperText(screen, (5, 42), "《》", size = 19, color = THECOLORS.get("grey100"), dsm = dsm)
music_arties = freetext.SuperText(screen, (5, display_size[1] - 93), "音乐家：", size = 15, color = THECOLORS.get("grey95"), dsm = dsm)
# button开头的都是按钮，需要在遍历信号时设置对应的功能
button_exit = freebutton.FreeButton(screen, [display_size[0] - 80, 0], [80, 40], "EXIT", border_color = THECOLORS.get("grey50"),
									draw_border = True, msg_tran = True, dsm = dsm)
button_go = freebutton.CircleButton(screen, (int(display_size[0] / 2), display_size[1] - 35), 30, "||",
									width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"), dsm = dsm)
button_adva = freebutton.CircleButton(screen, (int(display_size[0] / 2 + 70), display_size[1] - 35), 20, ">>",
									  width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"), dsm = dsm)
button_back = freebutton.CircleButton(screen, (int(display_size[0] / 2 - 70), display_size[1] - 35), 20, "<<",
									  width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"), dsm = dsm)
button_next = freebutton.CircleButton(screen, (int(display_size[0] / 2 + 125), display_size[1] - 35), 20, "|>",
									  width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"), dsm = dsm)
button_last = freebutton.CircleButton(screen, (int(display_size[0] / 2 - 125), display_size[1] - 35), 20, "<|",
									  width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"), dsm = dsm)
button_vol_add = freebutton.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 - 35)), 20, "V+",
										 width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"), dsm = dsm)
button_vol_min = freebutton.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 + 35)), 20, "V-",
										 width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"), dsm = dsm)
button_loop = freebutton.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 + 105)), 20, "L",
									  width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"), dsm = dsm)
lyrics = [freetext.SuperText(screen, (5, display_size[1] - 133 - 20 * index), "", size = 16, color = THECOLORS.get("grey80"), dsm = dsm)
		  for index in range(0, int((display_size[1] - 75 - 40) / 20) - 4)]  # 歌词显示列表
# 以下两个列表可以通过for循环对列表中的对象批量操作，注意，text中的都是文本，对象的操作与按钮不同！
button = [button_exit, button_go, button_adva, button_back, button_next, button_last, button_vol_add, button_vol_min, button_loop]
text = [vol_text, vol_num, event_text, music_name_text, time_text, time_num, freebird_text, version_text, pleiades_text]
for unit in button:
	unit.display_button = False
freelog.write(str(format(time.time(), ".5f")) + "   control : And the initialization\n")

# 获取音乐(歌词)文件夹中的文件列表
if music_path_set == "":
	music_list = os.listdir(path = 'music'); music_path = "music\\"
else:
	music_list = os.listdir(path = music_path_set); music_path = music_path_set + "\\"
if music_lrc_path_set == "":
	music_lrc_list = os.listdir(path = 'music_lrc'); music_lrc_path = "music_lrc\\"
else:
	music_lrc_list = os.listdir(music_lrc_path_set); music_lrc_path = music_lrc_path_set + "\\"
if use_setting_film is True:
	try:
		for music_list_index in range(0, len(music_list) - 1):
			suffix = music_list[music_list_index][len(music_list[music_list_index]) - 4:]  # 后缀名
			if suffix != ".mp3" and suffix != ".wav" and suffix != ".ogg":
				music_list.pop(music_list_index)
		for music_list_index in range(0, len(music_lrc_list)):
			if music_lrc_list[music_list_index][len(music_lrc_list[music_list_index]) - 4:] != ".lrc":
				music_lrc_list.pop(music_list_index)
	except IndexError:
		print(music_list, music_lrc_list)
		
# 状态与参数
music_lrc_is_load = False      # 歌词已加载
music_lrc_is_read = False      # 歌词已读取
music_lrc_line_len = 0         # 歌词行数初始化
lrc_line_index = 0             # 歌词行数索引
music_lrc_text = """"""        # 歌词文件标识符
music_lrc_line = []            # 每一行歌词的内容
music_lrc_draw = []            # 每一行歌词绘制的状态
sea_music_list = False         # 是否显示文件列表
sea_music_film = False         # 是否显示歌曲信息
music_list_index = 0           # 文件列表索引，控制播放的音乐文件
music_push_load = True         # 是否按下暂停键
music_is_load = False          # 音乐文件是否载入
loop_music = True              # 是否循环播放
move_text = True               # 歌词是否滚动中
lrc_time = []                  # 每一行歌词的时间
highlight_lrc_index = 0        # 高亮显示的行的索引
highlight_lrc_last = 0         # 下一高亮行的索引
show_highlight = True          # 显示高亮行
show_lyrics_roll = True        # 是否自动滚动歌词
music_lrc_is_roll = False      # 歌词已自动翻页
music_key_is_load = False      # 标签信息是否读取
music_key_name = ""            # 歌曲名标签
music_key_arties = ""          # 艺术家名标签
music_key_albums = ""          # 专辑名标签
music_key_image = None         # 专辑封面标签
music_key_lrc = ""             # 歌词标签
music_key_introduction = ""    # 歌曲介绍标签
music_key_sample_rate = 0      # 采样速率
music_key_channels = 0         # 声道信息
music_kry_length = 0           # 音乐长度
use_music_key_lrc = False      # 是否使用标签中的歌词
music_is_pure_music = False    # 音乐是纯音乐或没有歌词

# 音乐播放的准备
if music_list_index < len(music_list):
	# 载入第一个音乐
	music.load(music_path + music_list[music_list_index])
	music.set_volume(1)
	vol_num.set_msg(str(music.get_volume() * 100))  # 音量设置
	music_player = False    # 不播放
	music_is_load = True
	move_text = True
else:
	music.set_volume(1)
	vol_num.set_msg(str(music.get_volume() * 100))
	music_player = False
freelog.write(str(format(time.time(), ".5f")) + "   The music is ready\n")

# 主循环
while True:
	# 设置状态栏
	event_text.set_msg("现在时间：" + str(time.localtime().tm_year) + "年 " + str(time.localtime().tm_mon) + "月 " +
	                   str(time.localtime().tm_mday) + "日 " + str(time.localtime().tm_hour) + "时 " +
					   str(time.localtime().tm_min) + "分 " + str(time.localtime().tm_sec) + "秒   " +
					   "当前帧速率 " + str(int(clock.get_fps())) + "     freebird fly in the sky!")
	# 事件和信号遍历
	for event in pygame.event.get():
		_user_use_MOUSEWHEEL = False
		if event.type == MUSICOVER:
			music_list_index += 1   # 一曲播放完，更新文件列表索引
			music_is_load = False
			music_player = False
		if event.type == pygame.QUIT:
			freelog.write(str(format(time.time(), ".5f")) + "   Close the log file and close the program\n")
			freelog.close()
			os.remove("music_image_film.music_image")
			music.stop()
			pygame.quit()           # 退出pygame引擎
			sys.exit()              # 退出程序
		elif event.type == pygame.WINDOWEXPOSED and music_player is False:
			music.pause()
		elif event.type == pygame.MOUSEWHEEL:
			if event.dict.get("y") >= 0:     # 当用户使用鼠标滚轮时
				lrc_line_index -= 1          # 歌词向上滚动
			elif event.dict.get("y") <= 0:
				lrc_line_index += 1          # 歌词向下滚动
			move_text = True
			_user_use_MOUSEWHEEL = True
		elif event.type == pygame.MOUSEMOTION and 5 < pygame.mouse.get_pos()[0] < display_size[0] - 85 and \
				42 < pygame.mouse.get_pos()[1] < display_size[1] - 93 and _user_use_MOUSEWHEEL is False:
			if event.dict.get("touch") is True:
				if event.dict.get("y") >= 0:
					lrc_line_index -= 1
				elif event.dict.get("y") <= 0:
					lrc_line_index += 1
				move_text = True
		elif 5 < pygame.mouse.get_pos()[0] < display_size[0] - 85 and \
				5 < pygame.mouse.get_pos()[1] < 40 and event.type == pygame.MOUSEBUTTONDOWN:
			if sea_music_list is False and sea_music_film is False:      # 判断用户是否点击了歌曲文件名
				sea_music_list = True
				sea_music_film = False
			elif sea_music_list is True and sea_music_film is False:
				sea_music_list = False
				sea_music_film = True
			else:
				sea_music_list = False
				sea_music_film = False
			move_text = True
		elif event.type == pygame.KEYDOWN:   # 键盘事件
			if event.key == pygame.K_b:
				pg_wind_music_index -= 1     # 切换背景
			elif event.key == pygame.K_l:
				if show_highlight is True:
					show_highlight = False
				else:
					show_highlight = True
			elif event.key == pygame.K_r:
				if show_lyrics_roll is True:
					show_lyrics_roll = False
				else:
					show_lyrics_roll = True
			elif event.key == pygame.K_h:
				lrc_line_index -= 1
				move_text = True
			elif event.key == pygame.K_n:
				lrc_line_index += 1
				move_text = True
			elif event.key == pygame.K_SPACE:
				if button_go.display_button is False:  # 播放和暂停时的按钮样式
					button_go.set_msg("->")
					button_go.display_button = True
					if music_player is True:
						music.unpause()
						music_push_load = False
					else:
						music.play()
						music_player = True
						music_push_load = False
				else:
					button_go.set_msg("||")
					button_go.display_button = False
					music_push_load = True
					music.pause()

		# 以下调用了freebutton.position_button()的都是按钮
		# 注意，所有以下代码中按钮的操作都只是改变样貌或控制音乐的暂停和再次播放！
		# 对于音乐对象本身的操作（如切换音乐等）在时间遍历的下面，这里只是再次发出信号
		elif freebutton.position_button(button_exit, pygame.mouse.get_pos()) is True:
			button_exit.set_msg_color(THECOLORS.get("grey95"))
			button_exit.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				freelog.write(str(format(time.time(), ".5f")) + "   Close the log file and close the program\n")
				freelog.close()
				os.remove("music_image_film.music_image")
				music.stop()
				pygame.quit()
				sys.exit()
		elif freebutton.position_button(button_go, pygame.mouse.get_pos()) is True:
			button_go.set_msg_color(THECOLORS.get("grey95"))
			button_go.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button_go.display_button is False:  # 播放和暂停时的按钮样式
					button_go.set_msg("->")
					button_go.display_button = True
					if music_player is True:
						music.unpause()
						music_push_load = False
					else:
						music.play()
						music_player = True
						music_push_load = False
				else:
					button_go.set_msg("||")
					button_go.display_button = False
					music_push_load = True
					music.pause()
		elif freebutton.position_button(button_adva, pygame.mouse.get_pos()) is True:
			button_adva.set_msg_color(THECOLORS.get("grey95"))
			button_adva.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:  # 按下快进键
				music.pause()
				music_pos = music.get_pos() + 5   # 将播放时间后移5秒
				music.play(start = music_pos)
		elif freebutton.position_button(button_back, pygame.mouse.get_pos()) is True:
			button_back.set_msg_color(THECOLORS.get("grey95"))
			button_back.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:  # 快退
				music.pause()
				music_pos = music.get_pos() - 5
				music.play(start = music_pos)
		elif freebutton.position_button(button_next, pygame.mouse.get_pos()) is True:
			button_next.set_msg_color(THECOLORS.get("grey95"))
			button_next.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.pause()
				music_player = False
				music_is_load = False
				music_list_index += 1
				move_text = True
		elif freebutton.position_button(button_last, pygame.mouse.get_pos()) is True:
			button_last.set_msg_color(THECOLORS.get("grey95"))
			button_last.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.pause()
				music_player = False
				music_is_load = False
				music_list_index -= 1
				move_text = True
		elif freebutton.position_button(button_vol_add, pygame.mouse.get_pos()) is True:
			button_vol_add.set_msg_color(THECOLORS.get("grey95"))
			button_vol_add.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.set_volume(music.get_volume() + 0.05)   # 音量加
		elif freebutton.position_button(button_vol_min, pygame.mouse.get_pos()) is True:
			button_vol_min.set_msg_color(THECOLORS.get("grey95"))
			button_vol_min.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.set_volume(music.get_volume() - 0.05)   # 音量减
		elif freebutton.position_button(button_loop, pygame.mouse.get_pos()) is True:
			button_loop.set_msg_color(THECOLORS.get("grey95"))
			button_loop.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				if loop_music is True and button_loop.display_button is True:  # 循环切换循环按钮的样式
					button_loop.set_msg("N")
					loop_music = False
				elif loop_music is False and button_loop.display_button is True:
					button_loop.set_msg("L")
					loop_music = True
					button_loop.display_button = False
				elif loop_music is True and button_loop.display_button is False:
					button_loop.set_msg("OL")
					button_loop.display_button = True
		else:
			for unit in button:
				unit.check_button = False  # 这里的check_button是用于控制按钮是否被按下的，上面的代码中也有
		if event.type == pygame.WINDOWLEAVE:  # 当光标离开窗口后，坐标依然停留在离开前的位置，可能造成按钮一直被按下的假象
			for unit in button:               # 所以这里在设置一次
				unit.check_button = False

	# 以下代码接受从事件遍历中发出的信号，对音乐对象进行操作，注意，有先后顺序！
	if music_is_load is False and loop_music is True and button_loop.display_button is True:  # 单曲循环
		music_list_index -= 1
		music.load(music_path + music_list[music_list_index])
		music_player = True
		music_is_load = True
		move_text = True
		music.play()
	elif music_is_load is False and 0 <= music_list_index < len(music_list):  # 正常一曲终了后播放下一曲
		music.load(music_path + music_list[music_list_index])
		music_player = True
		music_is_load = True
		music_lrc_is_load = False
		music_lrc_is_read = False
		music_key_is_load = False
		music_lrc_is_roll = False
		music_is_pure_music = False
		move_text = True
		music.play()
	elif music_is_load is False and 0 > music_list_index:  # 在列表开头按下上一曲按钮，播放列表结尾的曲子
		music_list_index = len(music_list) - 1
		music.load(music_path + music_list[music_list_index])
		music_player = True
		music_is_load = True
		music_lrc_is_load = False
		music_lrc_is_read = False
		music_key_is_load = False
		music_lrc_is_roll = False
		music_is_pure_music = False
		move_text = True
		music.play()
	elif music_is_load is False and loop_music is True and button_loop.display_button is False:  # 列表循环
		music_player = False
		music_is_load = False
		music_lrc_is_load = False
		music_lrc_is_read = False
		music_key_is_load = False
		music_lrc_is_roll = False
		music_is_pure_music = False
		move_text = True
		music_list_index = 0
	elif music_is_load is False and loop_music is False:  # 顺序播放播完时，啥都不干
		music_player = False
		music_is_load = False
		music_lrc_is_load = False
		music_lrc_is_read = False
		music_key_is_load = False
		music_lrc_is_roll = False
		music_is_pure_music = False
		move_text = True
	if music_push_load is True:
		music.pause()
		
	# 获取标签信息
	if music_is_load is True and music_key_is_load is False:
		_film = b"0"
		music_key_lrc = ""
		music_key_introduction = ""
		use_music_key_lrc = False
		music_key = mutagen.File(music_path + music_list[music_list_index])
		music_key_name = music_key.get("TIT2")     # 歌曲名
		music_key_arties = music_key.get("TPE1")   # 艺术家名
		music_key_albums = music_key.get("TALB")   # 专辑名
		music_key_sample_rate = music_key.info.sample_rate
		music_key_channels = music_key.info.channels
		music_kry_length = music_key.info.length
		for index in range(0, len(music_key.values())):
			try:
				_film = music_key.values()[index].data
			except AttributeError:
				try:
					_lrc = music_key.values()[index].text
					if _lrc[0] == "[" and _lrc[3] == ":":
						music_key_lrc = music_key.values()[index].text
						use_music_key_lrc = True
				except (AttributeError, IndexError, TypeError):
					continue
		if use_music_key_lrc is True:
			line_str = ""
			music_lrc_line = []
			for index in range(0, len(music_key_lrc)):
				if music_key_lrc[index] != "\r" and music_key_lrc[index] != "\n":
					line_str += music_key_lrc[index]
				elif music_key_lrc[index] == "\r":
					line_str += "\n"
					music_lrc_line.append(line_str)
					line_str = ""
		music_image_film = open("music_image_film.music_image", "wb+")
		music_image_film.write(_film)
		music_image_film.close()
		try:
			music_key_image = pygame.image.load(os.path.join('music_image_film.music_image'))
		except pygame.error:
			music_key_image = pygame.image.load(os.path.join('assets/anto_music_image.jpg'))
		finally:
			music_key_image = pygame.transform.smoothscale(music_key_image, (260, 260))
		introduction = open("introduction.txt", "r+")
		introduction.seek(0, 0)
		for line in introduction:
			for index in range(0, len(line)):
				if line[index] == "$" and line[index + 1] == "$":
					if line[:index - 1] == music_list[music_list_index]:
						music_key_introduction = line[index + 3:-1]
		introduction.close()
		if music_key_introduction == "":
			music_key_introduction = music_key_name
		music_key_is_load = True
		freelog.write(str(format(time.time(), ".5f")) + "   Now load the key:" + "\n")

	# 以下代码用于检测歌词，排版与打印歌词
	lyrics_len = len(lyrics)   # 歌词显示列表的长度
	if music_is_load is True and music_lrc_is_load is False and music_lrc_is_read is False:  # 载入歌词
		if use_music_key_lrc is False:
			for lrc_unit in music_lrc_list:
				if lrc_unit[:len(lrc_unit) - 4] == music_list[music_list_index][:len(music_list[music_list_index]) - 4]:
					try:
						music_lrc_text = open(music_lrc_path + lrc_unit, "r+", encoding = "utf-8")
						music_lrc_is_load = True
						freelog.write(str(format(time.time(), ".5f")) + "   Now load the lyrics:" + str(music_lrc_text) + "\n")
					except SystemError:
						music_lrc_is_load = False
						lyrics[int(lyrics_len / 2)].set_msg("找到歌词文件但载入失败！")
						music_lrc_line = []
						freelog.write(str(format(time.time(), ".5f")) + "   ERROR : Find the lyrics but can't load it:" +
						              str(music_lrc_path) + str(lrc_unit) + "\n")
				else:
					lyrics[int(lyrics_len / 2)].set_msg("未找到歌词！")
					music_lrc_line = []
					freelog.write(str(format(time.time(), ".5f")) + "   ERROR : No lyrics:" + str(lrc_unit) + "\n")
		else:
			music_lrc_is_load = True
		music_lrc_draw = []
		lrc_line_index = 0
	# 读取标签信息后，使用标签信息作为歌曲信息
	if music_lrc_is_load is False and music_key_is_load is True:
		if music_key_name is not None:
			music_name.set_msg(str(music_key_name))
		if music_key_arties is not None and music_key_albums is not None:
			music_name.set_msg("音乐家：" + str(music_key_arties) + "  专辑：" + str(music_key_albums))
		else:
			music_arties.set_msg("音乐家：未知  专辑：未知")
	# 如果没有读取标签，使用文件名作为歌曲信息
	if music_lrc_is_load is False and music_key_is_load is False:
		try:
			music_name_arties = music_list[music_list_index][:len(music_list[music_list_index]) - 4].split('-', 1)
			music_name.set_msg(music_name_arties[1][1:])
			music_arties.set_msg("音乐家：" + music_name_arties[0][:-1] + "  专辑：未知")
		except IndexError:
			music_name.set_msg("未知曲名")
			music_arties.set_msg("音乐家：未知  专辑：未知")
		freelog.write(str(format(time.time(), ".5f")) + "   ERROR : Do not load the lyrics:" +
		              music_name.get_attribute().get("msg") + "\n")
	if music_lrc_is_load is True and music_lrc_is_read is False:  # 读取歌词
		for unit in lyrics:
			unit.set_msg("")
		if use_music_key_lrc is False:
			music_lrc_line = []  # 用于存放歌词的每一行
			for each_line in music_lrc_text:
				music_lrc_draw.append(False)
				music_lrc_line.append(each_line)
		else:
			for _ in music_lrc_line:
				music_lrc_draw.append(False)
		if type(music_lrc_text) is not str:
			music_lrc_text.close()
		music_lrc_is_read = True
		try:
			if str(music_lrc_line[1][1:4]) == "ti:":
				music_name.set_msg(str(music_lrc_line[1][4:len(music_lrc_line[1]) - 2]))
			if str(music_lrc_line[2][1:4]) == "ar:" and str(music_lrc_line[3][1:4]) == "al:":
				music_arties.set_msg("音乐家：" + str(music_lrc_line[2][4:len(music_lrc_line[2]) - 2]) +
									 "  专辑：" + str(music_lrc_line[3][4:len(music_lrc_line[3]) - 2]))
			if str(music_lrc_line[4][1:4]) == "by:":
				music_lrc_line.pop(4)
		except IndexError:
			try:
				music_name_arties = music_list[music_list_index][:len(music_list[music_list_index]) - 4].split('-', 1)
				music_name.set_msg(music_name_arties[1][1:])
				music_arties.set_msg("音乐家：" + music_name_arties[0][:-1] + "  专辑：未知")
			except IndexError:
				music_name.set_msg("未知曲名")
				music_arties.set_msg("音乐家：未知  专辑：未知")
			music_is_pure_music = True
		finally:
			music_lrc_line_len = len(music_lrc_line)
		each_line_index = lyrics_len - 1
		music_lrc_line_len_index = 0
		lrc_time = []    # 每行歌词的时间
		for each_line in music_lrc_line:
			if each_line_index == 0 or each_line_index <= lyrics_len - len(music_lrc_line):
				break
			try:
				# 将每行歌词的时间导入时间列表
				lrc_time.append(int(each_line[1:3]) * 60 + int(each_line[4:6]) + int(each_line[7:9]) / 100)
				music_lrc_line_len_index += 1
			except (IndexError, TypeError, ValueError):
				music_lrc_line_len_index += 1
		freelog.write(str(format(time.time(), ".5f")) + "   Set the lyrics:" + music_name.get_attribute().get("msg") + "\n")
	if lrc_line_index < 0:
		lrc_line_index = 0
	elif lrc_line_index > music_lrc_line_len - lyrics_len:
		lrc_line_index = music_lrc_line_len - lyrics_len
	if move_text is True:
		for unit in lyrics:
			unit.set_msg("")
	if sea_music_list is False and sea_music_film is False and move_text is True:
		try:
			if music_lrc_line_len < 4:
				lyrics[int(lyrics_len / 2)].set_msg("歌词文件异常！")
			elif music_lrc_line_len >= 4 and music_lrc_line[music_lrc_line_len - 1].find("[99:00.00]") != -1:
				lyrics[int(lyrics_len / 2)].set_msg("纯音乐 请欣赏")
				music_is_pure_music = True
		except IndexError:
			lyrics[int(lyrics_len / 2)].set_msg("歌词文件未找到！")
		if music_lrc_line_len >= 4:
			if music_lrc_line_len - 4 <= lyrics_len:
				for write_index in range(0, music_lrc_line_len - 4):
					lyrics[lyrics_len - write_index - 1].set_msg(str(music_lrc_line[write_index + 4][10:-1]))
			else:
				try:
					for write_index in range(0, lyrics_len):
						lyrics[lyrics_len - write_index - 1].set_msg(str(music_lrc_line[write_index + lrc_line_index + 4][10:-1]))
				except IndexError:
					lrc_line_index -= 1
	elif sea_music_list is True and move_text is True:
		lyrics[int(lyrics_len / 2)].set_msg("")
		if len(music_list) <= lyrics_len:
			for write_index in range(0, len(music_list)):
				lyrics[lyrics_len - write_index - 1].set_msg(str(music_list[write_index]))
		else:
			try:
				for write_index in range(0, lyrics_len):
					lyrics[lyrics_len - write_index - 1].set_msg(str(music_list[write_index + lrc_line_index]))
			except IndexError:
				lrc_line_index -= 1
	# 显示歌曲信息
	elif sea_music_film is True and move_text is True:
		prefix = "                                    "
		lyrics[lyrics_len - 1].set_msg(prefix + "歌曲名")
		lyrics[lyrics_len - 2].set_msg(prefix + "->  " + str(music_key_name))
		lyrics[lyrics_len - 3].set_msg(prefix + "艺术家名")
		lyrics[lyrics_len - 4].set_msg(prefix + "->  " + str(music_key_arties))
		lyrics[lyrics_len - 5].set_msg(prefix + "专辑名")
		lyrics[lyrics_len - 6].set_msg(prefix + "->  " + str(music_key_albums))
		lyrics[lyrics_len - 8].set_msg(prefix + "简介")
		lyrics[lyrics_len - 9].set_msg(prefix + "->  " + str(music_key_introduction))
		lyrics[lyrics_len - 12].set_msg(prefix + "sr: " + str(music_key_sample_rate) + "Hz  ca: " +
		                  str(music_key_channels) + "  len: " + str(int(music_kry_length)) + "s")
		lyrics[lyrics_len - 13].set_msg(prefix + "use ID3v2")
	move_text = False
	
	# 自动翻动歌词
	now_time = time.time()
	now_lyc_time = float(music.get_pos() / 1000)
	if sea_music_list is False and music_lrc_is_read is True:
		need_set_highlight = False
		each_line_index = lyrics_len - 1
		music_lrc_line_index = 1
		music_lrc_line_len_index = 0
		for time_unit in lrc_time:
			# 遍历时间列表，判断是否到了下一行歌词的时间
			if now_lyc_time - 0.1 <= time_unit <= now_lyc_time + 0.1:
				highlight_lrc_index = lrc_time.index(time_unit)
				if show_lyrics_roll is True and music_lrc_is_roll is False:
					highlight_lrc_last = highlight_lrc_index + 1
					music_lrc_is_roll = True
					if lrc_line_index != highlight_lrc_index - int(lyrics_len / 2):
						lrc_line_index = highlight_lrc_index - int(lyrics_len / 2)
					if highlight_lrc_index < int(lyrics_len / 2):
						lrc_line_index = 0
					else:
						lrc_line_index += 1
					move_text = True
	if highlight_lrc_last == highlight_lrc_index:
		music_lrc_is_roll = False
	
	# 打印歌词
	if sea_music_list is False and sea_music_film is False and music_is_pure_music is False:
		line_index = 13 - (highlight_lrc_index - lrc_line_index)
		if line_index < 0 or line_index > 13:
			line_index = 100
		pygame.draw.rect(screen, pg_wind_color[pg_wind_music_index - 1], (0, display_size[1] - 133 - 20 * line_index, 636, 19), 0)
	for unit in lyrics:
		unit.draw()
	if len(music_arties.get_attribute().get("msg")) > 70:
		music_arties.set_msg(str(music_arties.get_attribute().get("msg"))[:70] + "...")
	music_arties.draw()
	music_name.draw()

	# 以下代码打印窗口上的元素，包括按钮，文本之类的对象
	if sea_music_film is True and music_key_image is not None:
		screen.blit(music_key_image, (10, 90))
	if pg_wind_music_index < 1:
		pg_wind_music_index = 3
	if pg_wind_music_index == 1:
		screen.blit(pg_wind_music_r[0], (635, 0))
	elif pg_wind_music_index == 2:
		screen.blit(pg_wind_music_r[1], (635, 0))
	elif pg_wind_music_index == 3:
		screen.blit(pg_wind_music_r[2], (635, 0))
	for unit in button:
		if unit.check_button is False:
			unit.set_msg_color(THECOLORS.get("grey75"))
		unit.draw()
	if 0 <= music_list_index < len(music_list):  # 显示音乐的名称
		if len(str(music_list[music_list_index])) <= 65:
			music_name_text.set_msg("文件名称 -> " + str(music_list[music_list_index]))
		else:
			music_name_text.set_msg("文件名称 -> " + str(music_list[music_list_index])[:65] + "...")
	time_num.set_msg(str(int(music.get_pos() / 1000)) + "s")
	vol_num.set_msg(str(music.get_volume() * 100))
	for unit in text:
		unit.draw()

	# 窗口刷新，准备再次遍历事件
	pygame.display.flip()
	if pg_wind_music_index < 1:
		pg_wind_music_index = 3
	if pg_wind_music_index == 1:
		screen.blit(pg_wind_music[0], (0, 0))
	elif pg_wind_music_index == 2:
		screen.blit(pg_wind_music[1], (0, 0))
	elif pg_wind_music_index == 3:
		screen.blit(pg_wind_music[2], (0, 0))
	clock.tick(frame_number)  # 控制帧数
