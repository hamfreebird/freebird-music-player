"""freebird music player -> main"""

import os
import pygame
from pygame.mixer import music
from pygame.mixer import init as mixer_init  # 用于初始化音乐模块
from pygame.colordict import THECOLORS       # pygame的颜色列表
from sys import exit as sys_exit
from time import localtime as now_time
# import freepygame
import freepygamelib as freepygame
# from mutagen.id3 import ID3, APIC
global music_lrc_line_len

def list_to_str(_list_name):  # 用于将歌词列表转化为字符串
	list_str = repr(_list_name)
	list_str = list_str.replace("[", "")
	list_str = list_str.replace("]", "")
	return list_str

# def embed_album_art(filename, image):
# 	  audio = ID3(filename)
# 	  with open(image, 'rb') as f:
# 		  audio['APIC'] = APIC(
# 			  encoding = 3,         # 3表示UTF-8编码
# 			  mime = 'image/jpeg',  # 图片格式
# 			  type = 3,             # 3表示专辑封面
# 			  desc = u'Cover',      # 描述信息
# 			  data = f.read()       # 读取图片数据
# 		  )
# 	  audio.save()

# 导入设置文件
setting_list = ["" for _ in range(0, 3)]
setting_index = 0
use_setting_film = True
setting = open("setting.txt", "r")
for set_num in setting:
	setting_list[setting_index] = set_num
	setting_index += 1
display_size_set = (720, 480)
music_path_set = str(setting_list[1][14:len(setting_list[1]) - 2])
music_lrc_path_set = str(setting_list[2][18:len(setting_list[2]) - 2])
setting.close()

# 初始化
pygame.init()
mixer_init(frequency = 44100)  # 音乐模块的初始化
if display_size_set == (720, 480):
	display_size = (720, 480)
else:
	display_size = display_size_set
frame_number = 60
pygame.display.set_caption("freebird music player")
pygame.display.set_icon(pygame.image.load("assets\\freebird_music.ico"))
pg_wind_music1 = pygame.image.load("assets\\wind_music.JPG")
pg_wind_music2 = pygame.image.load("assets\\wind_music2.JPG")
pg_wind_music3 = pygame.image.load("assets\\wind_music3.jpg")
pg_wind_music = [pg_wind_music1, pg_wind_music2, pg_wind_music3]
pg_wind_music_index = 3
screen = pygame.display.set_mode(display_size)
screen.blit(pg_wind_music[2], (0, 0))
clock = pygame.time.Clock()
MUSICOVER = pygame.USEREVENT  # 当音乐播放完成时的信号
music.set_endevent(MUSICOVER)

# 需要显示的可交互的元素
event_text = freepygame.SuperText(screen, [3, 5], "", size = 10, color = THECOLORS.get("grey70"))
music_name_text = freepygame.SuperText(screen, [3, 20], "文件名称 -> ", size = 15, color = THECOLORS.get("grey80"))
vol_text = freepygame.SuperText(screen, (display_size[0] - 73, 50), "音量", size = 20, color = THECOLORS.get("grey80"))
vol_num = freepygame.SuperText(screen, (display_size[0] - 73, 70), "", color = THECOLORS.get("grey80"))
time_text = freepygame.SuperText(screen, (display_size[0] - 73, 100), "时间", size = 20, color = THECOLORS.get("grey80"))
time_num = freepygame.SuperText(screen, (display_size[0] - 73, 120), "", color = THECOLORS.get("grey80"))
freebird_text = freepygame.SuperText(screen, (display_size[0] - 90, display_size[1] - 30), "by freebird",
									 "Freestyle Script", color = THECOLORS.get("grey100"))
pleiades_text = freepygame.SuperText(screen, (10, display_size[1] - 50), "Pleiades", "Freestyle Script", color = THECOLORS.get("grey100"))
version_text = freepygame.SuperText(screen, (10, display_size[1] - 20), "v 1.0.0", size = 15, color = THECOLORS.get("grey95"))
music_name = freepygame.SuperText(screen, (5, 42), "《》", size = 19, color = THECOLORS.get("grey100"))
music_arties = freepygame.SuperText(screen, (5, display_size[1] - 93), "音乐家：", size = 15, color = THECOLORS.get("grey95"))
# button开头的都是按钮，需要在遍历信号时设置对应的功能
button_exit = freepygame.FreeButton(screen, [display_size[0] - 80, 0], [80, 40], "EXIT", border_color = THECOLORS.get("grey50"),
									draw_border = True, msg_tran = True)
button_go = freepygame.CircleButton(screen, (int(display_size[0] / 2), display_size[1] - 35), 30, "||",
									width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"))
button_adva = freepygame.CircleButton(screen, (int(display_size[0] / 2 + 70), display_size[1] - 35), 20, ">>",
									  width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"))
button_back = freepygame.CircleButton(screen, (int(display_size[0] / 2 - 70), display_size[1] - 35), 20, "<<",
									  width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"))
button_next = freepygame.CircleButton(screen, (int(display_size[0] / 2 + 125), display_size[1] - 35), 20, "|>",
									  width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"))
button_last = freepygame.CircleButton(screen, (int(display_size[0] / 2 - 125), display_size[1] - 35), 20, "<|",
									  width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"))
button_vol_add = freepygame.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 - 35)), 20, "V+",
										 width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"))
button_vol_min = freepygame.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 + 35)), 20, "V-",
										 width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"))
button_loop = freepygame.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 + 105)), 20, "L",
									  width = 1, msg_tran = True, draw_border = True, border_color = THECOLORS.get("grey80"))
lyrics = [freepygame.SuperText(screen, (5, display_size[1] - 133 - 20 * index), "", size = 16, color = THECOLORS.get("grey80"))
		  for index in range(0, int((display_size[1] - 75 - 40) / 20) - 4)]  # 歌词显示列表
# 以下两个列表可以通过for循环对列表中的对象批量操作，注意，text中的都是文本，对象的操作与按钮不同！
button = [button_exit, button_go, button_adva, button_back, button_next, button_last, button_vol_add, button_vol_min, button_loop]
text = [vol_text, vol_num, event_text, music_name_text, time_text, time_num, freebird_text, version_text, pleiades_text]
for unit in button:
	unit.display_button = False

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
music_lrc_line = ["" for _ in range(0, 512)]      # 每一行歌词的内容
music_lrc_draw = [False for _ in range(0, 512)]   # 每一行歌词绘制的状态
sea_music_list = False         # 是否显示文件列表
music_list_index = 0           # 文件列表索引，控制播放的音乐文件
music_push_load = True
music_is_load = False          # 音乐文件是否载入
loop_music = True              # 是否循环播放

# 音乐播放的准备
if music_list_index < len(music_list):
	# 载入第一个音乐
	music.load(music_path + music_list[music_list_index])
	music.set_volume(1)
	vol_num.set_msg(str(music.get_volume() * 100))  # 音量设置
	music_player = False    # 不播放
	music_is_load = True
else:
	music.set_volume(1)
	vol_num.set_msg(str(music.get_volume() * 100))
	music_player = False

# 主循环
while True:
	# 设置状态栏
	event_text.set_msg("现在时间：" + str(now_time().tm_year) + "年 " + str(now_time().tm_mon) + "月 " + str(now_time().tm_mday) +
					   "日 " + str(now_time().tm_hour) + "时 " + str(now_time().tm_min) + "分 " + str(now_time().tm_sec) + "秒   " +
					   "当前帧速率 " + str(int(clock.get_fps())) + "     freebird fly in the sky!")
	# 事件和信号遍历
	for event in pygame.event.get():
		if event.type == MUSICOVER:
			music_list_index += 1   # 一曲播放完，更新文件列表索引
			music_is_load = False
			music_player = False
		if event.type == pygame.QUIT:
			music.stop()
			pygame.quit()           # 退出pygame引擎
			sys_exit()              # 退出程序
		elif event.type == pygame.WINDOWEXPOSED and music_player is False:
			music.pause()
		elif event.type == pygame.MOUSEWHEEL:
			if event.dict.get("y") >= 0:     # 当用户使用鼠标滚轮时
				lrc_line_index -= 1          # 歌词向上滚动
			elif event.dict.get("y") <= 0:
				lrc_line_index += 1          # 歌词向下滚动
		elif 5 < pygame.mouse.get_pos()[0] < display_size[0] - 85 and \
				5 < pygame.mouse.get_pos()[1] < 40 and event.type == pygame.MOUSEBUTTONDOWN:
			if sea_music_list is False:      # 判断用户是否点击了歌曲文件名
				sea_music_list = True        # True是显示歌词
			else:
				sea_music_list = False
		elif event.type == pygame.KEYDOWN:   # 键盘事件
			if event.key == pygame.K_b:
				pg_wind_music_index -= 1     # 切换背景
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

		# 以下调用了freepygame.position_button()的都是按钮
		# 注意，所有以下代码中按钮的操作都只是改变样貌或控制音乐的暂停和再次播放！
		# 对于音乐对象本身的操作（如切换音乐等）在时间遍历的下面，这里只是再次发出信号
		elif freepygame.position_button(button_exit, pygame.mouse.get_pos()) is True:
			button_exit.set_msg_color(THECOLORS.get("grey95"))
			button_exit.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.stop()
				pygame.quit()
				sys_exit()
		elif freepygame.position_button(button_go, pygame.mouse.get_pos()) is True:
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
		elif freepygame.position_button(button_adva, pygame.mouse.get_pos()) is True:
			button_adva.set_msg_color(THECOLORS.get("grey95"))
			button_adva.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:  # 按下快进键
				music.pause()
				music_pos = music.get_pos() + 5   # 将播放时间后移5秒
				music.play(start = music_pos)
		elif freepygame.position_button(button_back, pygame.mouse.get_pos()) is True:
			button_back.set_msg_color(THECOLORS.get("grey95"))
			button_back.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:  # 快退
				music.pause()
				music_pos = music.get_pos() - 5
				music.play(start = music_pos)
		elif freepygame.position_button(button_next, pygame.mouse.get_pos()) is True:
			button_next.set_msg_color(THECOLORS.get("grey95"))
			button_next.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.pause()
				music_player = False
				music_is_load = False
				music_list_index += 1
		elif freepygame.position_button(button_last, pygame.mouse.get_pos()) is True:
			button_last.set_msg_color(THECOLORS.get("grey95"))
			button_last.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.pause()
				music_player = False
				music_is_load = False
				music_list_index -= 1
		elif freepygame.position_button(button_vol_add, pygame.mouse.get_pos()) is True:
			button_vol_add.set_msg_color(THECOLORS.get("grey95"))
			button_vol_add.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.set_volume(music.get_volume() + 0.05)   # 音量加
		elif freepygame.position_button(button_vol_min, pygame.mouse.get_pos()) is True:
			button_vol_min.set_msg_color(THECOLORS.get("grey95"))
			button_vol_min.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.set_volume(music.get_volume() - 0.05)   # 音量减
		elif freepygame.position_button(button_loop, pygame.mouse.get_pos()) is True:
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
		music.play()
	elif music_is_load is False and 0 <= music_list_index < len(music_list):  # 正常一曲终了后播放下一曲
		music.load(music_path + music_list[music_list_index])
		music_player = True
		music_is_load = True
		music_lrc_is_load = False
		music_lrc_is_read = False
		music.play()
	elif music_is_load is False and 0 > music_list_index:  # 在列表开头按下上一曲按钮，播放列表结尾的曲子
		music_list_index = len(music_list) - 1
		music.load(music_path + music_list[music_list_index])
		music_player = True
		music_is_load = True
		music_lrc_is_load = False
		music_lrc_is_read = False
		music.play()
	elif music_is_load is False and loop_music is True and button_loop.display_button is False:  # 列表循环
		music_player = False
		music_is_load = False
		music_lrc_is_load = False
		music_lrc_is_read = False
		music_list_index = 0
	elif music_is_load is False and loop_music is False:  # 顺序播放播完时，啥都不干
		music_player = False
		music_is_load = False
		music_lrc_is_load = False
		music_lrc_is_read = False
	if music_push_load is True:
		music.pause()

	# 以下代码用于检测歌词，排版与打印歌词
	lyrics_len = len(lyrics)
	if music_is_load is True and music_lrc_is_load is False and music_lrc_is_read is False:  # 载入歌词
		for lrc_unit in music_lrc_list:
			if lrc_unit[:len(lrc_unit) - 4] == music_list[music_list_index][:len(music_list[music_list_index]) - 4]:
				try:
					music_lrc_text = open(music_lrc_path + lrc_unit, "r+", encoding = "utf-8")
					music_lrc_is_load = True
					print("< 10 > Now load the lyrics :", music_lrc_text)
				except SystemError:
					music_lrc_is_load = False
					lyrics[int(lyrics_len / 2)].set_msg("找到歌词文件但载入失败！")
					music_lrc_line = ["" for _ in range(0, 512)]
					print("< 11 > Find the lyrics but can't load it :", music_lrc_path, lrc_unit)
			else:
				lyrics[int(lyrics_len / 2)].set_msg("未找到歌词！")
				music_lrc_line = ["" for _ in range(0, 512)]
		music_lrc_draw = [False for _ in range(0, 512)]
		lrc_line_index = 0
	if music_lrc_is_load is False:
		try:
			music_name_arties = music_list[music_list_index][:len(music_list[music_list_index]) - 4].split('-', 1)
			music_name.set_msg(music_name_arties[1][1:])
			music_arties.set_msg("作曲家：" + music_name_arties[0][:-1] + "  专辑：未知")
		except IndexError:
			music_name.set_msg("未知曲名")
			music_arties.set_msg("音乐家：未知  专辑：未知")
		print("< 12 > Do not load the lyrics :", music_name.get_attribute().get("msg"))
	if music_lrc_is_load is True and music_lrc_is_read is False:  # 读取歌词
		for unit in lyrics: unit.set_msg("")
		music_lrc_line = ["" for _ in range(0, 512)]
		music_lrc_line_len = 0
		for each_line in music_lrc_text:
			music_lrc_draw[music_lrc_line_len] = False
			music_lrc_line[music_lrc_line_len] = each_line
			music_lrc_line_len += 1
		music_lrc_text.close()
		music_lrc_is_read = True
		if str(music_lrc_line[1][1:4]) == "ti:":
			music_name.set_msg(str(music_lrc_line[1][4:len(music_lrc_line[1]) - 2]))
		if str(music_lrc_line[2][1:4]) == "ar:" and str(music_lrc_line[3][1:4]) == "al:":
			str_len = 0
			for index in ("音乐家：" + str(music_lrc_line[2][4:len(music_lrc_line[2]) - 2]) + "  专辑：" +
						  str(music_lrc_line[3][4:len(music_lrc_line[3]) - 2])):
				str_len += len(str(ord(index)))
			if str_len <= 200:
				music_arties.set_msg("音乐家：" + str(music_lrc_line[2][4:len(music_lrc_line[2]) - 2]) +
									 "  专辑：" + str(music_lrc_line[3][4:len(music_lrc_line[3]) - 2]))
			else:
				music_arties.set_msg(("音乐家：" + str(music_lrc_line[2][4:len(music_lrc_line[2]) - 2]) +
									  "  专辑：" + str(music_lrc_line[3][4:len(music_lrc_line[3]) - 2]))[:42] + "...")
		if str(music_lrc_line[4][1:4]) == "by:":
			music_lrc_line.pop(4)
		print("< 13 > Set the lyrics :", music_name.get_attribute().get("msg"))
	if lrc_line_index < 0:
		lrc_line_index = 0
	for unit in lyrics: unit.set_msg("")
	if sea_music_list is False:
		try:
			if music_lrc_line_len < 4:
				lyrics[int(lyrics_len / 2)].set_msg("歌词文件异常！")
			elif music_lrc_line_len >= 4 and music_lrc_line[music_lrc_line_len - 1].find("[99:00.00]") != -1:
				lyrics[int(lyrics_len / 2)].set_msg("纯音乐 请欣赏")
		except IndexError:
			lyrics[int(lyrics_len / 2)].set_msg("歌词文件未找到！")
		if lrc_line_index > music_lrc_line_len - lyrics_len - 3:
			lrc_line_index = music_lrc_line_len - lyrics_len - 3
		elif music_lrc_line_len >= 4:
			if music_lrc_line_len - 4 <= lyrics_len:
				for write_index in range(0, music_lrc_line_len - 4):
					str_len = 0
					for index_str in str(music_lrc_line[write_index + 4][10:-1]):
						str_len += len(str(ord(index_str)))
					if str_len > 200:
						lyrics[lyrics_len - write_index - 1].set_msg(str(music_lrc_line[write_index + 4][10:60]) + "...")
					else:
						lyrics[lyrics_len - write_index - 1].set_msg(str(music_lrc_line[write_index + 4][10:-1]))
			else:
				try:
					for write_index in range(0, lyrics_len):
						str_len = 0
						for index_str in str(music_lrc_line[write_index + lrc_line_index + 4][10:-1]):
							str_len += len(str(ord(index_str)))
						if str_len > 200:
							lyrics[lyrics_len - write_index - 1].set_msg(str(music_lrc_line[write_index + lrc_line_index + 4][10:60]) + "...")
						else:
							lyrics[lyrics_len - write_index - 1].set_msg(str(music_lrc_line[write_index + lrc_line_index + 4][10:-1]))
				except IndexError:
					lrc_line_index -= 1
	else:
		if len(music_list) <= lyrics_len:
			for write_index in range(0, len(music_list)):
				str_len = 0
				for index_str in str(music_list[write_index]):
					str_len += len(str(ord(index_str)))
				if str_len > 200:
					lyrics[lyrics_len - write_index - 1].set_msg(str(music_list[write_index][10:60]) + "...")
				else:
					lyrics[lyrics_len - write_index - 1].set_msg(str(music_list[write_index]))
		else:
			try:
				for write_index in range(0, lyrics_len):
					str_len = 0
					for index_str in str(music_list[write_index + lrc_line_index]):
						str_len += len(str(ord(index_str)))
					if str_len > 200:
						lyrics[lyrics_len - write_index - 1].set_msg(str(music_list[write_index + lrc_line_index][10:60]) + "...")
					else:
						lyrics[lyrics_len - write_index - 1].set_msg(str(music_list[write_index + lrc_line_index]))
			except IndexError:
				lrc_line_index -= 1

	each_line_index = lyrics_len - 1
	music_lrc_line_index = 1
	music_lrc_line_len_index = 0
	# for each_line in music_lrc_line:
	# 	if each_line_index == 0 or each_line_index <= lyrics_len - len(music_lrc_line):
	# 		break
	# 	try:
	# 		if each_line[0] == "[" and each_line[9] == "]" and music_lrc_line_len_index >= 4:
	# 			if music.get_pos() / 10 < float(each_line[1:3] + each_line[4:6] + each_line[7:9]) <= music.get_pos() / 10 + 2:
	# 				music_lrc_draw[music_lrc_line_index] = True
	# 			each_line_index -= 1
	# 		music_lrc_line_index += 1
	# 	except IndexError:
	# 		break
	# 	music_lrc_line_len_index += 1
	# try:
	# 	for write_index in range(0, lyrics_len):
	# 		if music_lrc_draw[write_index - lrc_line_index + 4] is True:
	# 			lyrics[lyrics_len - write_index].set_color(THECOLORS.get("grey80"))
	# except IndexError:
	# 	print("out!")

	for unit in lyrics:  # 打印歌词
		unit.draw()
	if len(music_arties.get_attribute().get("msg")) > 70:
		music_arties.set_msg(str(music_arties.get_attribute().get("msg"))[:70] + "...")
	music_arties.draw()
	music_name.draw()

	# 以下代码打印窗口上的元素，包括按钮，文本之类的对象
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
