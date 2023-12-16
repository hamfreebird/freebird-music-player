"""freebird music player -> main"""
"""
播放器原型版本

停止更新 - 23.08.28
可能与未来版本设置文件不兼容！
"""

import os
import pygame
import freepygame.freepygamelib as freepygame
from pygame.mixer import music
from pygame.mixer import init as mixer_init  # 用于初始化音乐模块
from pygame.gfxdraw import line as gfxdraw_line
from pygame.colordict import THECOLORS       # pygame的颜色列表
from sys import exit as sys_exit             # 控制退出
from time import sleep as time_sleep         # 控制延迟
from time import localtime as now_time
from time import time as time_time
global music_lrc_line_len

def list_to_str(_list_name):  # 用于将歌词列表转化为字符串
	list_str = repr(_list_name)
	list_str = list_str.replace("[", "")
	list_str = list_str.replace("]", "")
	return list_str

# 导入设置文件
setting_list = ["" for index in range(0, 3)]
setting_index = 0
setting = open("setting.txt", "r")
for set_num in setting:
	setting_list[setting_index] = set_num
	setting_index += 1
display_size_set = (720, 480)
music_path_set = str(setting_list[1][14:len(setting_list[1]) - 2])
music_lrc_path_set = str(setting_list[2][18:len(setting_list[2]) - 2])

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
screen = pygame.display.set_mode(display_size)
screen.fill(THECOLORS.get("grey100"))  # grey100是白色,带100的透明度
clock = pygame.time.Clock()
MUSICOVER = pygame.USEREVENT  # 当音乐播放完成时的信号
music.set_endevent(MUSICOVER)

# 需要显示的可交互的元素
event_text = freepygame.SuperText(screen, [3, 5], "", size = 10, color = THECOLORS.get("grey50"))
music_name_text = freepygame.SuperText(screen, [3, 20], "文件名称 -> ", size = 15, color = THECOLORS.get("grey30"))
vol_text = freepygame.SuperText(screen, (display_size[0] - 73, 50), "音量", size = 20)
vol_num = freepygame.SuperText(screen, (display_size[0] - 73, 70), "")
time_text = freepygame.SuperText(screen, (display_size[0] - 73, 100), "时间", size = 20)
time_num = freepygame.SuperText(screen, (display_size[0] - 73, 120), "")
freebird_text = freepygame.SuperText(screen, (display_size[0] - 90, display_size[1] - 30), "by freebird", "Freestyle Script")
pleiades_text = freepygame.SuperText(screen, (8, display_size[1] - 50), "Pleiades", "Freestyle Script")
version_text = freepygame.SuperText(screen, (10, display_size[1] - 20), "v 1.0.0", size = 15)
# button开头的都是按钮，需要在遍历信号时设置对应的功能
button_exit = freepygame.FreeButton(screen, [display_size[0] - 80, 0], [80, 40], "EXIT",
								draw_line = True, line_color = THECOLORS.get("grey100"), line_width = 5)
button_go = freepygame.CircleButton(screen, (int(display_size[0] / 2), display_size[1] - 35), 30, "||")
button_adva = freepygame.CircleButton(screen, (int(display_size[0] / 2 + 70), display_size[1] - 35), 20, ">>")
button_back = freepygame.CircleButton(screen, (int(display_size[0] / 2 - 70), display_size[1] - 35), 20, "<<")
button_next = freepygame.CircleButton(screen, (int(display_size[0] / 2 + 125), display_size[1] - 35), 20, "|>")
button_last = freepygame.CircleButton(screen, (int(display_size[0] / 2 - 125), display_size[1] - 35), 20, "<|")
button_vol_add = freepygame.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 - 35)), 20, "V+")
button_vol_min = freepygame.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 + 35)), 20, "V-")
button_loop = freepygame.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 + 105)), 20, "L")
music_name = freepygame.FreeButton(screen, (5, 42), (display_size[0] - 90, 20), "《》",
								size = 19, button_color = THECOLORS.get("grey100"), text_color = THECOLORS.get("grey0"), draw_border = False)
music_arties = freepygame.FreeButton(screen, (5, display_size[1] - 93), (display_size[0] - 90, 15), "音乐家：",
								size = 15, button_color = THECOLORS.get("grey100"), text_color = THECOLORS.get("grey0"), draw_border = False)
lyrics = [freepygame.FreeButton(screen, (5, display_size[1] - 113 - 20 * index), (display_size[0] - 90, 15), "",
								size = 16, button_color = THECOLORS.get("grey100"), text_color = THECOLORS.get("grey0"), draw_border = False)
		  for index in range(0, int((display_size[1] - 75 - 40) / 20) - 2)]  # 歌词显示列表
# 以下两个列表可以通过for循环对列表中的对象批量操作，注意，text中的都是文本，对象的操作与按钮不同！
button = [button_exit, button_go, button_adva, button_back, button_next, button_last, button_vol_add, button_vol_min, button_loop]
text = [vol_text, vol_num, event_text, music_name_text, time_text, time_num, freebird_text, version_text, pleiades_text]
for unit in button:
	unit.display_button = False

# 获取音乐(歌词)文件夹中的文件列表
if music_path_set == "": music_list = os.listdir(path = 'music'); music_path = "music\\"
else: music_list = os.listdir(path = music_path_set); music_path = music_path_set + "\\"
if music_lrc_path_set == "": music_lrc_list = os.listdir(path = 'music_lrc'); music_lrc_path = "music_lrc\\"
else: music_lrc_list = os.listdir(music_lrc_path_set); music_lrc_path = music_lrc_path_set + "\\"
# try:
# 	for music_list_index in range(0, len(music_list)):
# 		if music_list[music_list_index][:len(music_list[music_list_index]) - 4] != ".mp3" or \
# 				music_list[music_list_index][:len(music_list[music_list_index]) - 4] != ".wav" or\
# 				music_list[music_list_index][:len(music_list[music_list_index]) - 4] != ".ogg":
# 			music_list.remove(music_list[music_list_index])
# except:
# 	print(music_list)
# try:
# 	for music_list_index in range(0, len(music_lrc_list)):
# 		if music_lrc_list[music_list_index][:len(music_lrc_list[music_list_index]) - 4] != ".lrc":
# 			music_lrc_list.remove(music_lrc_list[music_list_index])
# except:
# 	print(music_lrc_list)
music_lrc_is_load = False
music_lrc_is_read = False
music_lrc_line_len = 9999999
lrc_line_index = 0
music_lrc_text = """"""
music_lrc_line = ["" for index in range(0, 512)]
music_lrc_draw = [[False, False] for index in range(0, 512)]
music_list_index = 0
music_push_load = True
music_is_load = False
loop_music = True

# 音乐播放的准备
if music_list_index < len(music_list):
	# 载入第一个音乐
	music.load(music_path + music_list[music_list_index])
	music.set_volume(1)
	vol_num.set_msg(str(music.get_volume() * 100))
	music_player = False
	music_is_load = True
else:
	music.set_volume(1)
	vol_num.set_msg(str(music.get_volume() * 100))
	music_player = False
time_sleep(0.05)
frame_number_list = [float(time_time()), 0.0]

# 主事件循环
while True:
	event_text.set_msg("现在时间：" + str(now_time().tm_year) + "年 " + str(now_time().tm_mon) + "月 " + str(now_time().tm_mday) +
					   "日 " + str(now_time().tm_hour) + "时 " + str(now_time().tm_min) + "分 " + str(now_time().tm_sec) + "秒   " +
					   "当前帧速率 " + str(1 / float(frame_number_list[1] - frame_number_list[0])))
	frame_number_list[0] = float(time_time())
	# 事件和信号遍历
	for event in pygame.event.get():
		if event.type == MUSICOVER:
			music_list_index += 1
			music_is_load = False
			music_player = False
		if event.type == pygame.QUIT:
			music.stop()
			pygame.quit()
			sys_exit()
		elif event.type == pygame.WINDOWEXPOSED and music_player is False:
			music.pause()
		elif event.type == pygame.MOUSEWHEEL:
			if event.dict.get("y") >= 0:
				lrc_line_index -= 1
			elif event.dict.get("y") <= 0:
				lrc_line_index += 1
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
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
			button_exit.set_button_color(THECOLORS.get("grey25"))
			button_exit.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.stop()
				pygame.quit()
				sys_exit()
		elif freepygame.position_button(button_go, pygame.mouse.get_pos()) is True:
			button_go.set_button_color(THECOLORS.get("grey25"))
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
			button_adva.set_button_color(THECOLORS.get("grey25"))
			button_adva.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music_pos = music.get_pos() + 5
				music.pause()
				music.play(start = music_pos)
		elif freepygame.position_button(button_back, pygame.mouse.get_pos()) is True:
			button_back.set_button_color(THECOLORS.get("grey25"))
			button_back.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music_pos = music.get_pos() - 5
				music.pause()
				music.play(start = music_pos)
		elif freepygame.position_button(button_next, pygame.mouse.get_pos()) is True:
			button_next.set_button_color(THECOLORS.get("grey25"))
			button_next.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.pause()
				music_player = False
				music_is_load = False
				music_list_index += 1
		elif freepygame.position_button(button_last, pygame.mouse.get_pos()) is True:
			button_last.set_button_color(THECOLORS.get("grey25"))
			button_last.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.pause()
				music_player = False
				music_is_load = False
				music_list_index -= 1
		elif freepygame.position_button(button_vol_add, pygame.mouse.get_pos()) is True:
			button_vol_add.set_button_color(THECOLORS.get("grey25"))
			button_vol_add.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.set_volume(music.get_volume() + 0.05)
		elif freepygame.position_button(button_vol_min, pygame.mouse.get_pos()) is True:
			button_vol_min.set_button_color(THECOLORS.get("grey25"))
			button_vol_min.check_button = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				music.set_volume(music.get_volume() - 0.05)
		elif freepygame.position_button(button_loop, pygame.mouse.get_pos()) is True:
			button_loop.set_button_color(THECOLORS.get("grey25"))
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
	if music_is_load is True and music_lrc_is_load is False and music_lrc_is_read is False:  # 载入歌词
		for lrc_unit in music_lrc_list:
			if lrc_unit[:len(lrc_unit) - 4] == music_list[music_list_index][:len(music_list[music_list_index]) - 4]:
				try:
					music_lrc_text = open(music_lrc_path + lrc_unit, "r+", encoding = "utf-8")
					music_lrc_is_load = True
					print(music_lrc_text)
				except:
					music_lrc_is_load = False
					lyrics[int(len(lyrics) / 2)].set_msg("找到歌词文件但载入失败！")
					music_lrc_line = ["" for index in range(0, 512)]
			else:
				lyrics[int(len(lyrics) / 2)].set_msg("未找到歌词！")
				music_lrc_line = ["" for index in range(0, 512)]
		music_lrc_draw = [[False, False] for index in range(0, 512)]
		lrc_line_index = 0
	if music_lrc_is_load is False:
		music_name.set_msg(" ")
		music_arties.set_msg("音乐家：未知  专辑：未知")
	if music_lrc_is_load is True and music_lrc_is_read is False:  # 读取歌词
		for unit in lyrics: unit.set_msg("")
		music_lrc_line = ["" for index in range(0, 512)]
		music_lrc_line_len = 0
		for each_line in music_lrc_text:
			music_lrc_draw[music_lrc_line_len][0] = False
			music_lrc_draw[music_lrc_line_len][1] = False
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
	if music_lrc_line_len < 4:
		lyrics[int(len(lyrics) / 2)].set_msg("歌词文件异常！")
	elif music_lrc_line_len >= 4 and music_lrc_line[music_lrc_line_len - 1].find("[99:00.00]") != -1:
		lyrics[int(len(lyrics) / 2)].set_msg("纯音乐 请欣赏")
	if lrc_line_index < 0:
		lrc_line_index = 0
	if lrc_line_index > music_lrc_line_len - len(lyrics) - 3:
		lrc_line_index = music_lrc_line_len - len(lyrics) - 3
	elif music_lrc_line_len >= 4:
		if music_lrc_line_len - 4 <= len(lyrics):
			for write_index in range(0, music_lrc_line_len - 4):
				lyrics[len(lyrics) - write_index - 1].set_msg(str(music_lrc_line[write_index + 4][10:-1]))
		else:
			try:
				for write_index in range(0, len(lyrics)):
					str_len = 0
					for index_str in str(music_lrc_line[write_index + lrc_line_index + 4][10:-1]):
						str_len += len(str(ord(index_str)))
					if str_len > 200:
						lyrics[len(lyrics) - write_index - 1].set_msg(str(music_lrc_line[write_index + lrc_line_index + 4][10:60]) + "...")
					else:
						lyrics[len(lyrics) - write_index - 1].set_msg(str(music_lrc_line[write_index + lrc_line_index + 4][10:-1]))
			except IndexError:
				lrc_line_index -= 1
	each_line_index = len(lyrics) - 1
	music_lrc_line_index = 1
	music_lrc_line_len_index = 0
	for each_line in music_lrc_line:
		if each_line_index == 0 or each_line_index <= len(lyrics) - len(music_lrc_line):
			break
		try:
			if each_line[0] == "[" and each_line[9] == "]" and music_lrc_line_len_index >= 4:
				if music.get_pos() / 10 < float(each_line[1:3] + each_line[4:6] + each_line[7:9]) <= music.get_pos() / 10 + 2:
					music_lrc_draw[music_lrc_line_index][0] = True
					print("W1 ", music_lrc_draw[music_lrc_line_index][0], " ", music_lrc_line_index)
				elif music.get_pos() / 10 - 2 < float(each_line[1:3] + each_line[4:6] + each_line[7:9]) < music.get_pos() / 10:
					music_lrc_draw[music_lrc_line_index][1] = True
					print("W2 ", music_lrc_draw[music_lrc_line_index][1], " ", music_lrc_line_index)
				each_line_index -= 1
			music_lrc_line_index += 1
		except IndexError:
			break
		music_lrc_line_len_index += 1
	try:
		for write_index in range(0, len(lyrics)):
			if music_lrc_draw[write_index + lrc_line_index][0] is True and music_lrc_draw[write_index + lrc_line_index][1] is False:
				lyrics[len(lyrics) - write_index + 3].set_text_color(THECOLORS.get("grey0"))
				print("get ", write_index + lrc_line_index, " ", len(lyrics) - write_index + 3)
	except IndexError:
		print("out!")
	for unit in lyrics:  # 打印歌词
		unit.draw()
	if len(music_arties.get_attribute().get("msg")) > 70:
		music_arties.set_msg(str(music_arties.get_attribute().get("msg"))[:70] + "...")
	music_arties.draw()
	music_name.draw()

	# 以下代码打印窗口上的元素，包括按钮，文本之类的对象

	for unit in button:
		if unit.check_button is False:
			unit.set_button_color(THECOLORS.get("grey0"))
		unit.draw()
	if 0 <= music_list_index < len(music_list):  # 显示音乐的名称
		if len(str(music_list[music_list_index])) <= 65:
			music_name_text.set_msg("文件名称 -> " + str(music_list[music_list_index]))
		else:
			music_name_text.set_msg("文件名称 -> " + str(music_list[music_list_index])[:65] + "...")
	time_num.set_msg(str(int(music.get_pos() / 1000)) + "s")
	vol_num.set_msg(str(music.get_volume() * 100))
	gfxdraw_line(screen, 0, display_size[1] - 75, display_size[0],
				 display_size[1] - 75, THECOLORS.get("grey0"))
	gfxdraw_line(screen, display_size[0] - 80, 0, display_size[0] - 80,
				 display_size[1] - 75, THECOLORS.get("grey0"))
	gfxdraw_line(screen, 0, 39, display_size[0] - 80, 39, THECOLORS.get("grey0"))
	for index in range(0, int((display_size[1] - 75 - 40) / 20) - 1):  # 绘制歌词线
		gfxdraw_line(screen, 5, display_size[1] - 95 - 20 * index, display_size[0] - 85,
					 display_size[1] - 95 - 20 * index, THECOLORS.get("grey75"))
	for unit in text:
		unit.draw()

	# 窗口刷新，准备再次遍历事件
	pygame.display.flip()
	screen.fill(THECOLORS.get("grey100"))
	clock.tick(frame_number)  # 控制帧数
	frame_number_list[1] = float(time_time())
