# -*- coding: utf-8 -*-
"""
freebird music player -> main
Copyright 2023 freebird
"""

import os
import sys
import time
import dialog_box
try:
    import pygame
    from pygame.mixer import init as mixer_init
    import pygame.freetype as freetype
    from pygame.colordict import THECOLORS
    from pygame.draw import rect, aaline
except ModuleNotFoundError:
    dialog_box.error_msg("can't find pygame module!")
    exit()
from play_list import *
from freepygame import freetext, freebutton, freeicon, freetransformation
from io import text_encoding
import mutagen
try:
    import librosa
    import librosa.display
except ModuleNotFoundError:
    dialog_box.error_msg("can't find librosa module!")
    exit()

# 统一编码
text_encoding("utf-8")

argv = sys.argv

# 导入设置文件
try:
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
except:
    dialog_box.waring_msg("setting.txt file read error!\nplease check you setting film")
    sys.exit()

# 初始化
mixer_init(frequency = 44100)
pygame.init()
freetype.init()
frame_number = 80
pygame.display.set_caption("freebird music player")
pygame.display.set_icon(pygame.image.load("assets\\freebird_music.ico"))
pg_wind_music_index = 3
screen = pygame.display.set_mode(display_size, pygame.DOUBLEBUF | pygame.HWSURFACE)
buffer = pygame.Surface(display_size)
dirty_rects = []
# 文件检查
# _all_assets = os.listdir(path = "assets")
# _all_icon = os.listdir(path = "assets\\icon")
# _all_image = os.listdir(path = "assets\\image")
# _all_other = os.listdir(path = "assets\\other")
# _all_particle = os.listdir(path = "assets\\particle")
try:
    lrc_font = pygame.font.Font("assets\\simhei.ttf", 20)
    pg_wind_music1 = pygame.image.load("assets\\wind_music.JPG").convert(24)
    pg_wind_music2 = pygame.image.load("assets\\wind_music2.JPG").convert(24)
    pg_wind_music3 = pygame.image.load("assets\\wind_music3.jpg").convert(24)
    pg_wind_music1_r = pygame.image.load("assets\\wind_music_r.JPG").convert(24)
    pg_wind_music2_r = pygame.image.load("assets\\wind_music2_r.JPG").convert(24)
    pg_wind_music3_r = pygame.image.load("assets\\wind_music3_r.jpg").convert(24)
    pg_wind_music = [pg_wind_music1, pg_wind_music2, pg_wind_music3]
    pg_wind_music_r = [pg_wind_music1_r, pg_wind_music2_r, pg_wind_music3_r]
    pg_wind_color = [(0, 105, 70), (0, 20, 105), (137, 30, 0), (137, 30, 0)]
    icon_play = freeicon.FreeIcon(screen, (330, 415), pygame.image.load("assets\\icon\\play_1.png"),
                 pygame.image.load("assets\\icon\\play_2.png"))
    icon_stop = freeicon.FreeIcon(screen, (330, 415), pygame.image.load("assets\\icon\\stop_1.png"),
                 pygame.image.load("assets\\icon\\stop_2.png"))
    icon_last = freeicon.FreeIcon(screen, (270, 425), pygame.image.load("assets\\icon\\last_1.png"),
                 pygame.image.load("assets\\icon\\last_2.png"))
    icon_next = freeicon.FreeIcon(screen, (410, 425), pygame.image.load("assets\\icon\\next_1.png"),
                 pygame.image.load("assets\\icon\\next_2.png"))
    icon_vol_open = freeicon.FreeIcon(screen, (660, 175), pygame.image.load("assets\\icon\\vol_open_1.png"),
                     pygame.image.load("assets\\icon\\vol_open_2.png"))
    icon_vol_close = freeicon.FreeIcon(screen, (660, 235), pygame.image.load("assets\\icon\\vol_close_1.png"),
                      pygame.image.load("assets\\icon\\vol_close_2.png"))
    icon_setting = freeicon.FreeIcon(screen, (-100, -100), pygame.image.load("assets\\icon\\setting_1.png"),
                    pygame.image.load("assets\\icon\\setting_2.png"))
    icon_trash = freeicon.FreeIcon(screen, (-100, -100), pygame.image.load("assets\\icon\\trash_1.png"),
                  pygame.image.load("assets\\icon\\trash_2.png"))
    icon_random = freeicon.FreeIcon(screen, (660, 325), pygame.image.load("assets\\icon\\random_1.png"),
                   pygame.image.load("assets\\icon\\random_2.png"))
    icon_paper_plane = freeicon.FreeIcon(screen, (475, 425), pygame.image.load("assets\\icon\\paper_plane_1.png"),
                        pygame.image.load("assets\\icon\\paper_plane_2.png"))
    icon_home = freeicon.FreeIcon(screen, (660, 370), pygame.image.load("assets\\icon\\home_1.png"),
                 pygame.image.load("assets\\icon\\home_2.png"))
    icon_frequency = freeicon.FreeIcon(screen, (-100, -100), pygame.image.load("assets\\icon\\frequency_1.png"),
                      pygame.image.load("assets\\icon\\frequency_2.png"))
    icon_film = freeicon.FreeIcon(screen, (206, 426), pygame.image.load("assets\\icon\\film_1.png"),
                 pygame.image.load("assets\\icon\\film_2.png"))
    icon_cycle = freeicon.FreeIcon(screen, (660, 325), pygame.image.load("assets\\icon\\cycle_1.png"),
                  pygame.image.load("assets\\icon\\cycle_2.png"))
    icon_bird = freeicon.FreeIcon(screen, (-100, -100), pygame.image.load("assets\\icon\\bird_1.png"),
                 pygame.image.load("assets\\icon\\bird_2.png"))
    icon = [icon_play, icon_stop, icon_last, icon_next, icon_vol_open, icon_vol_close, icon_setting, icon_trash,
            icon_random, icon_paper_plane, icon_home, icon_frequency, icon_film, icon_cycle, icon_bird]
    icon_random.display_button = False
    icon_cycle.display_button = False
    particle = [pygame.image.load("assets\\particle\\0.PNG"),
                pygame.image.load("assets\\particle\\1.PNG"),
                pygame.image.load("assets\\particle\\2.PNG"),
                pygame.image.load("assets\\particle\\3.PNG"),
                pygame.image.load("assets\\particle\\4.PNG"),
                pygame.image.load("assets\\particle\\5.PNG"),
                pygame.image.load("assets\\particle\\6.PNG"),
                pygame.image.load("assets\\particle\\7.PNG"),
                pygame.image.load("assets\\particle\\8.PNG"),
                pygame.image.load("assets\\particle\\9.PNG")]
    event_text = freetext.SuperText(screen, [3, 5], "", "assets\\simhei.ttf", size=10,
                                    color=THECOLORS.get("grey70"), dsm=dsm)
    music_name_text = freetext.SuperText(screen, [3, 20], "文件名称 -> ", "assets\\simhei.ttf",
                                         size=15, color=THECOLORS.get("grey80"), dsm=dsm)
    vol_text = freetext.SuperText(screen, (display_size[0] - 73, 50), "音量", "assets\\simhei.ttf",
                                  size=20, color=THECOLORS.get("grey80"), dsm=dsm)
    vol_num = freetext.SuperText(screen, (display_size[0] - 73, 70), "", "assets\\simhei.ttf",
                                 color=THECOLORS.get("grey80"), dsm=dsm)
    time_text = freetext.SuperText(screen, (display_size[0] - 73, 100), "时间", "assets\\simhei.ttf",
                                   size=20, color=THECOLORS.get("grey80"), dsm=dsm)
    time_num = freetext.SuperText(screen, (display_size[0] - 73, 120), "", "assets\\simhei.ttf",
                                  color=THECOLORS.get("grey80"), dsm=dsm)
    freebird_text = freetext.SuperText(screen, (display_size[0] - 145, display_size[1] - 30), "freebird", size=20,
                                       font="assets\\FeiXiangDeNiaoErBeiChongChi1-2.ttf",
                                       color=THECOLORS.get("grey100"), dsm=dsm)
    pleiades_text = freetext.SuperText(screen, (10, display_size[1] - 50), "Paper ship", "assets\\segoepr.ttf",
                                       size=16, color=THECOLORS.get("grey100"), dsm=dsm)
    version_text = freetext.SuperText(screen, (10, display_size[1] - 20), "v 1.3.4", "assets\\simhei.ttf",
                                      size=15, color=THECOLORS.get("grey95"), dsm=dsm)
    music_name = freetext.SuperText(screen, (5, 42), "《》", "assets\\simhei.ttf", size=19,
                                    color=THECOLORS.get("grey100"), dsm=dsm)
    music_arties = freetext.SuperText(screen, (5, display_size[1] - 93), "音乐家：", "assets\\simhei.ttf",
                                      size=15, color=THECOLORS.get("grey95"), dsm=dsm)
    # button开头的都是按钮，需要在遍历信号时设置对应的功能
    button_exit = freebutton.FreeButton(screen, [display_size[0] - 80, 0], [80, 40], "EXIT", "assets\\simhei.ttf",
                                        border_color=THECOLORS.get("grey50"), draw_border=True, msg_tran=True, dsm=dsm)
    button_loop = freebutton.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 + 75)), 20, "L",
                                          "assets\\simhei.ttf", border_width = 2,
                                          width=2, msg_tran=True, draw_border=True,
                                          border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_set_highlight = freebutton.CircleButton(screen, (130, 130), 20, "H", "assets\\simhei.ttf",
                                                   width=2, msg_tran=True, draw_border=True,
                                                   border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_set_branch = freebutton.CircleButton(screen, (250, 130), 20, "B", "assets\\simhei.ttf",
                                                width=2, msg_tran=True, draw_border=True,
                                                border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_set_Keyboard = freebutton.CircleButton(screen, (370, 130), 20, "K", "assets\\simhei.ttf",
                                                  width=2, msg_tran=True, draw_border=True,
                                                  border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_set_image = freebutton.CircleButton(screen, (490, 130), 20, "I", "assets\\simhei.ttf",
                                               width=2, msg_tran=True, draw_border=True,
                                               border_color=THECOLORS.get("grey80"), dsm=dsm)
    # msg开头的是输入框，使用和按钮一样的坐标检测函数
    msg_music_path = freetext.FreeMsg(screen, (100, 100), (20, 200), "", "assets\\simhei.ttf", 20,
                                      THECOLORS.get("grey80"), THECOLORS.get("grey0"), 1)
    lyrics = [freebutton.FreeButton(screen, [5, display_size[1] - 113 - 20 * index], [display_size[0] - 90, 15], "",
                                    "assets\\simhei.ttf", size=16, button_color=THECOLORS.get("grey25"),
                                    text_color=THECOLORS.get("grey95"), draw_border=False, msg_tran = True, dsm = dsm)
              for index in range(0, int((display_size[1] - 75 - 40) / 20) - 2)]  # 歌词显示列表
    other_lyrics = [freetext.SuperText(screen, [5, (display_size[1] - 133 - 20 * index)], "", "assets\\simhei.ttf",
                                 size=16, color=THECOLORS.get("grey80"), dsm=dsm)
              for index in range(0, int((display_size[1] - 75 - 40) / 20) - 4)]  # 信息显示列表
    new_lyrics = []  # 歌词显示列表（新）
    # 以下两个列表可以通过for循环对列表中的对象批量操作，注意，text中的都是文本，对象的操作与按钮不同！
    button = [button_exit, button_loop]
    text = [vol_text, vol_num, event_text, music_name_text, time_text, time_num, freebird_text, version_text,
            pleiades_text]
    set_button = [button_set_highlight, button_set_branch, button_set_Keyboard, button_set_image]
except FileNotFoundError:
    # film check
    dialog_box.waring_msg("Missing resource file!")
    if dialog_box.ask_msg("Want to check the resources file?") is True:
        _all_assets = os.listdir(path = "assets")
        _all_icon = os.listdir(path = "assets\\icon")
        _all_image = os.listdir(path = "assets\\image")
        _all_other = os.listdir(path = "assets\\other")
        _all_particle = os.listdir(path = "assets\\particle")
        _all = [].append(_all_assets).append(_all_icon).append(_all_image).append(_all_other).append(_all_particle)
        _lose_assets = []
        for _unit in _all:
            for _assets in []:
                if _assets == _unit:
                    continue
                else:
                    _lose_assets.append(_assets)
        if not _lose_assets:
            dialog_box.info_msg("There is no resource file deletion")
        else:
            dialog_box.info_msg("...")
    pygame.quit()
    exit()

screen.blit(pg_wind_music[2], (0, 0))
clock = pygame.time.Clock()
MUSICOVER = pygame.USEREVENT  # 当音乐播放完成时的信号
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, MUSICOVER, pygame.WINDOWEXPOSED, pygame.MOUSEWHEEL,
                          pygame.MOUSEBUTTONDOWN, pygame.WINDOWLEAVE])

from pygame.mixer import music
music.set_endevent(MUSICOVER)

for unit in button:
    unit.display_button = False
icon_stop.display_button = False

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
sea_setting_film = False       # 是否显示设置界面
sea_home_page = False          # 是否显示主页
sea_list_page = False          # 是否显示播放列表界面
sea_music_spectrum = False     # 是否显示频谱图
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
music_key_is_read = False      # 标签信息是否设置
music_key_name = ""            # 歌曲名标签
music_key_arties = ""          # 艺术家名标签
music_key_albums = ""          # 专辑名标签
music_key_image = None         # 专辑封面标签
music_key_lrc = ""             # 歌词标签
music_key_introduction = ""    # 歌曲简介标签
music_key_sample_rate = 0      # 采样速率
music_key_channels = 0         # 声道信息
music_kry_length = 0           # 音乐长度
use_music_key_lrc = False      # 是否使用标签中的歌词
music_is_pure_music = False    # 音乐是纯音乐或没有歌词
branch_lrc_text = True         # 是否进行歌词分行
write_msg = False              # 是否写入输入框
use_keyboard_to_set = True     # 是否使用键盘设置
blur_image = None              # 模糊背景图像
use_blur_image = False         # 是否使用模糊背景图像
need_to_save = False           # 是否需要保存信息
need_to_change_home = True     # 是否需要刷新主页
now_play_list = None           # 当前播放列表
r_per_second_film = []         # 每秒频谱图
now_music_spectrum = []        # 当前频谱的柱状显示
cal_music_spectrum = False     # 是否计算频谱图
last_play_second = 0           # 上一个播放的秒数


# 获取音乐(歌词)文件夹中的文件列表
if music_path_set == "":
    music_list = os.listdir(path = 'music')
    music_path = "music\\"
else:
    music_list = os.listdir(path = music_path_set)
    music_path = music_path_set + "\\"
if music_lrc_path_set == "":
    music_lrc_list = os.listdir(path = 'music_lrc')
    music_lrc_path = "music_lrc\\"
else:
    music_lrc_list = os.listdir(music_lrc_path_set)
    music_lrc_path = music_lrc_path_set + "\\"
if use_setting_film is True:
    try:
        for music_list_index in range(0, len(music_list) - 1):
            suffix = music_list[music_list_index][len(music_list[music_list_index]) - 4:]  # 后缀名
            if suffix != ".mp3" and suffix != ".wav" and suffix != ".ogg":
                music_list.pop(music_list_index)
    except IndexError:
        print("error with music list")
    try:
        for music_lrc_list_index in range(0, len(music_lrc_list) - 1):
            suffix = music_lrc_list[music_lrc_list_index][len(music_lrc_list[music_lrc_list_index]) - 4:]
            if music_lrc_list[music_lrc_list_index][len(music_lrc_list[music_lrc_list_index]) - 4:] != ".lrc":
                music_lrc_list.pop(music_lrc_list_index)
    except IndexError:
        print("error with music lrc list")
try:
    music_list.insert(0, argv[1])
except IndexError:
    pass

# 专辑和播放列表相关参数
other_music_list = []
reduction_music_list = []
sea_other_music_list = False

# 播放列表初始化
parameter = Parameter([music_path, music_lrc_path, music_list, music_lrc_list])
playlist = PlayList()
print("infor title : " + str(parameter.get_title()))
print("playlist title : " + str(playlist.get_title()))
music_last = parameter.get_music_last()
music_last_not_load = True
if music_last == "":
    music_last_not_load = False
if playlist.get_what_you_play_now()[0] != "":
    # 如果有非默认播放列表在播放，使用该列表替换当前的默认播放列表
    other_music_list = playlist.get(str(playlist.get_what_you_play_now()[0]))
    reduction_music_list = music_list
    music_list_index = playlist.get_what_you_play_now()[1]
    sea_other_music_list = True
else:
    sea_other_music_list = False

# 音乐播放的准备
if music_list_index < len(music_list):
    # 载入第一个音乐
    music.load(music_path + music_list[music_list_index])
    music.set_volume(1)
    vol_num.set_msg(str(music.get_volume() * 100))  # 音量设置
    music_player = False    # 不播放
    music_is_load = True
    cal_music_spectrum = True
    move_text = True
else:
    dialog_box.waring_msg("Please join the music folder first!")
    pygame.quit()
    exit()

def init_music_argument():
    """
    Initializes the music-related global variables.

    This function sets the initial values for the music-related global variables.
    It is called when the program starts or when the music settings need to be reset.
    """
    global music_lrc_is_load, music_lrc_is_read, music_key_is_load, music_lrc_is_roll, \
        music_key_is_read, music_is_pure_music, need_to_change_home, need_to_save, move_text, cal_music_spectrum

    # Set the initial values for the music-related global variables
    music_lrc_is_load = False  # Indicates whether the music lyrics have been loaded
    music_lrc_is_read = False  # Indicates whether the music lyrics have been read
    music_key_is_load = False  # Indicates whether the music tag information has been loaded
    music_lrc_is_roll = False  # Indicates whether the music lyrics are currently rolling
    music_key_is_read = False  # Indicates whether the music tag information has been read
    music_is_pure_music = False  # Indicates whether the music is pure (without lyrics)
    need_to_change_home = True  # Indicates whether the home page needs to be changed
    need_to_save = False  # Indicates whether the information needs to be saved
    cal_music_spectrum = True
    move_text = True  # Indicates whether the text (lyrics) should move

def load_music(_music_list_index):
    """
    Load the music file at the specified index from the music list.

    This function attempts to load the music file from the music list at the given index.
    If the file is not found or there is an error loading the file, it tries to load the next file in the list.

    Parameters:
    _music_list_index (int): The index of the music file to load from the music list.

    Returns:
    int: The updated index of the music file to load from the music list. If the file at the given index is not found or
     there is an error loading it, it returns the next index.
    """
    try:
        music.load(music_path + music_list[_music_list_index])
    except (FileNotFoundError, pygame.error):
        try:
            music.load(music_list[_music_list_index])
        except pygame.error:
            _music_list_index += 1
    return _music_list_index

def get_the_tag_information():
    """
    Retrieves and stores information about the music from the tag.

    This function extracts the music's name, artists, albums, sample rate,
    channels, and length from the tag. It also loads the music's image from
    the tag and blurs it if required.

    Parameters:
    None. The function uses the global variables music_list_index, music_path,
    and the mutagen library to extract the tag information.

    Returns:
    None. The function modifies the global variables music_key_name, music_key_arties,
    music_key_albums, music_key_image, music_key_lrc, use_music_key_lrc, and blur_image.
    """
    global music_key_introduction, music_key_image, music_lrc_line, music_key_lrc, use_music_key_lrc, blur_image

    music_key_introduction = ""
    use_music_key_lrc = False
    try:
        music_key = mutagen.File(music_path + music_list[music_list_index])
    except mutagen.MutagenError:
        music_key = mutagen.File(music_list[music_list_index])

    get_information_from_tag(music_key)

    _bit_film, music_key_lrc = get_image_and_lrc_from_tag(music_key)

    music_image_film = open("music_image_film.music_image", "wb+")
    music_image_film.write(_bit_film)
    music_image_film.close()
    # img = cv2.imread('music_image_film.music_image')
    # blur_image = cv2.GaussianBlur(img, (5, 5), 3)
    try:
        music_key_image = pygame.image.load(os.path.join('music_image_film.music_image')).convert()
    except pygame.error:
        music_key_image = pygame.image.load(os.path.join('assets/anto_music_image.jpg')).convert()
    finally:
        try:
            music_key_image = pygame.transform.smoothscale(music_key_image, (260, 260))
        except ValueError:
            music_key_image = pygame.image.load(os.path.join('assets/anto_music_image.jpg')).convert()
            music_key_image = pygame.transform.smoothscale(music_key_image, (260, 260))
    if use_blur_image is True:
        blur_image = freetransformation.image_blur_processing(pygame.Surface.copy(music_key_image), 2)
        blur_image = pygame.transform.smoothscale(blur_image, (800, 800))
    # create the original pygame surface
    # c_size, c_image_mode, c_raw = (260, 260), 'RGBA', _film
    # surf = pygame.image.fromstring(c_raw, c_size, c_image_mode)
    # pil_blured = Image.fromstring("RGBA", c_size, c_raw).filter(ImageFilter.GaussianBlur(radius=6))
    # finally_image = pygame.image.fromstring(pil_blured.tostring("raw", c_image_mode), c_size, c_image_mode)

def get_information_from_tag(music_key):
    """
    Extracts and stores information about the music from the tag.

    Parameters:
    music_key (mutagen.File): The music file from which to extract the tag information.

    Returns:
    None. The function modifies the global variables music_key_name, music_key_arties,
    music_key_albums, music_key_sample_rate, music_key_channels, and music_kry_length.
    """
    global music_key_name, music_key_arties, music_key_albums, music_key_sample_rate, \
        music_key_channels, music_kry_length
    music_key_name = music_key.get("TIT2")  # 歌曲名
    music_key_arties = music_key.get("TPE1")  # 艺术家名
    music_key_albums = music_key.get("TALB")  # 专辑名
    music_key_sample_rate = music_key.info.sample_rate
    music_key_channels = music_key.info.channels
    music_kry_length = music_key.info.length

def get_image_and_lrc_from_tag(music_key):
    """
    Retrieves the image and lyrics from the tag of the music file.

    This function extracts the image and lyrics from the tag of the music file.
    It searches for the image data and lyrics text in the tag values.
    If the lyrics text is found, it is stored in the global variable `music_key_lrc`
    and the `use_music_key_lrc` flag is set to True.

    Parameters:
    music_key (mutagen.File): The music file from which to extract the tag information.

    Returns:
    tuple: A tuple containing the image data (as bytes) and the lyrics text (as a string).
        """
    global music_key_lrc, use_music_key_lrc, music_lrc_line
    _bit_film = b"0"
    music_key_lrc = ""
    for index in range(0, len(music_key.values())):
        try:
            _bit_film = music_key.values()[index].data
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
    return _bit_film, music_key_lrc

def get_lrc_from_lrc_film(_lyrics_len):
    """
    Load lyrics from a lrc file based on the current music file.

    Parameters:
    _lyrics_len (int): The length of the lyrics area in the GUI.
    """
    global music_lrc_text, music_lrc_is_load, music_lrc_line, music_lrc_draw, lrc_line_index

    # If the lyrics are not extracted from the tag, search for a lrc file
    if use_music_key_lrc is False:
        for lrc_unit in music_lrc_list:
            try:
                # Check if the lrc file name matches the current music file name
                if lrc_unit[:len(lrc_unit) - 4] == music_list[music_list_index][:len(music_list[music_list_index]) - 4]:
                    try:
                        try:
                            # Try to open the lrc file from the specified path
                            music_lrc_text = open(music_lrc_path + lrc_unit, "r+", encoding="utf-8")
                        except OSError:
                            # If the file is not found in the specified path, try to open it from the current directory
                            music_lrc_text = open(lrc_unit, "r+", encoding="utf-8")
                        music_lrc_is_load = True
                    except SystemError:
                        # If there is an error while opening the file, set the loading status to False
                        music_lrc_is_load = False
                        lyrics[int(_lyrics_len / 2)].set_msg("找到歌词文件但载入失败！")
                        music_lrc_line = []
                else:
                    music_lrc_line = []
            except (UnicodeEncodeError, PermissionError):
                print(str(format(time.time(), ".5f")) + "   ERROR : UnicodeEncodeError or PermissionError\n")
    else:
        music_lrc_is_load = True

    music_lrc_draw = []
    lrc_line_index = 0

def use_tag_information_as_a_song_message():
    """
    Use the tag information (name, artist, album) to set the song message.

    This function retrieves the music name and artist/album information from
    the tag and sets the corresponding GUI elements.
    It also sets the music_key_is_read and music_lrc_is_load flags to True
    to indicate that the tag information has been used.
    """
    global music_key_is_read, music_lrc_is_load
    if music_key_name is not None:
        music_name.set_msg(str(music_key_name))
    if music_key_arties is not None and music_key_albums is not None:
        music_arties.set_msg("音乐家：" + str(music_key_arties) + "  专辑：" + str(music_key_albums))
    else:
        music_arties.set_msg("音乐家：未知  专辑：未知")
    music_key_is_read = True
    music_lrc_is_load = True

def use_filename_as_a_song_message():
    """
    Use the filename to set the song message.

    This function extracts the song name and artist from the filename and sets the corresponding GUI elements.
    The artist is assumed to be the part before the first hyphen, and the song name is the part after the first hyphen.
    If the filename does not contain a hyphen, it sets both the song name and artist to "未知".
    Finally, it sets the music_key_is_read flag to True to indicate that the tag information has been used.
    """
    global music_key_is_read
    try:
        music_name_arties = music_list[music_list_index][:len(music_list[music_list_index]) - 4].split('-', 1)
        music_name.set_msg(music_name_arties[1][1:])
        music_arties.set_msg("音乐家：" + music_name_arties[0][:-1] + "  专辑：未知")
    except IndexError:
        music_name.set_msg("未知曲名")
        music_arties.set_msg("音乐家：未知  专辑：未知")
    music_key_is_read = True

def read_the_lyrics():
    """
    This function reads the lyrics from the music file and prepares them for display.

    Effects:
    - Sets the lyrics text in the lyrics list.
    - Initializes necessary variables for lyrics handling.
    - Determines the type of lyrics (branch or ordinary) and sets the appropriate variables.
    """
    global lyrics, music_lrc_line, music_lrc_draw, music_lrc_is_read, music_is_pure_music, \
        music_lrc_line_len, lrc_time, new_lyrics

    for _unit in lyrics:
        _unit.set_msg("")

    init_music_lrc_line()
    music_lrc_is_read = True

    add_music_text_information()

    _each_line_index = lyrics_len - 1
    _music_lrc_line_len_index = 0
    lrc_time = []  # Each line of lyrics' time
    new_lyrics = []  # Each line of lyrics rendered as an image

    if branch_lrc_text is True:
        set_branch_lrc_text(_each_line_index, _music_lrc_line_len_index)
    else:
        set_ordinary_lrc_text(_each_line_index, _music_lrc_line_len_index)
    music_lrc_line_len = len(music_lrc_line)

def init_music_lrc_line():
    """
    Initialize the music lyrics line.

    This function reads the lyrics from the music file and prepares them for display.
    If the 'use_music_key_lrc' flag is False, it reads the lyrics from the 'music_lrc_text' file.
    The lyrics are stored in the 'music_lrc_line' list, and a corresponding flag is added to the 'music_lrc_draw' list.
    If the 'use_music_key_lrc' flag is True, it initializes the 'music_lrc_draw' list with False flags.
    Finally, if the 'music_lrc_text' is not a string, it closes the file.
    """
    global music_lrc_line, music_lrc_text
    if use_music_key_lrc is False:
        music_lrc_line = []  # 用于存放歌词的每一行
        try:
            for each_line in music_lrc_text:
                music_lrc_draw.append(False)
                music_lrc_line.append(each_line)
        except ValueError:
            pass
    else:
        for _ in music_lrc_line:
            music_lrc_draw.append(False)
    if type(music_lrc_text) is not str:
        # noinspection PyUnresolvedReferences
        music_lrc_text.close()

def add_music_text_information():
    """
    This function adds music information from the lyrics line to the music name and artist labels.
    If the lyrics line does not contain the required tags, it tries to extract the information from the music file name.
    If the information is not available, it sets the music name and artist labels to "未知".

    Raises:
    IndexError: If the lyrics line does not contain the required tags or if the music file name
    is not in the expected format.
    """
    global music_is_pure_music, music_lrc_line_len
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

def set_branch_lrc_text(each_line_index, music_lrc_line_len_index):
    """
    This function processes branch lyrics text. It splits each line into time and content,
    and inserts the time into the time list. If the line contains both time and content,
    it inserts the content into the next line.

    Parameters:
    each_line_index (int): The index of the current line in the lyrics text.
    music_lrc_line_len_index (int): The current index in the processed lyrics text.

    Returns:
    int: The updated index in the processed lyrics text.
    """
    index_offset_quantity = 0
    for each_index in range(0, len(music_lrc_line)):
        _this_line_time = 0
        new_line = music_lrc_line[each_index + index_offset_quantity].split(" / ")
        if each_line_index == 0 or each_line_index <= lyrics_len - len(music_lrc_line):
            break
        try:
            _this_line_time = int(new_line[0][1:3]) * 60 + int(new_line[0][4:6]) + int(new_line[0][7:9]) / 100
        except (TypeError, ValueError):
            _this_line_time = 0
        if len(new_line) == 2:
            try:
                lrc_time.append(_this_line_time)
                music_lrc_line[each_index + index_offset_quantity] = new_line[0] + " / "
                lrc_time.append(_this_line_time)
                music_lrc_line.insert(each_index + index_offset_quantity + 1, "[00:00:00]" + new_line[1])
                music_lrc_line_len_index += 2
            except (IndexError, TypeError, ValueError):
                music_lrc_line_len_index += 1
        else:
            try:
                # 将时间附加到时间列表
                lrc_time.append(_this_line_time)
                music_lrc_line_len_index += 1
            except (IndexError, TypeError, ValueError):
                music_lrc_line_len_index += 1
        index_offset_quantity += len(new_line) - 1
    for index in range(0, len(lrc_time)):
        try:
            if lrc_time[index] == 0:
                lrc_time.pop(index)
        except IndexError:
            break
    return music_lrc_line_len_index

def set_ordinary_lrc_text(each_line_index, music_lrc_line_len_index):
    """
    This function processes and renders each line of the lyrics in the ordinary format.

    Parameters:
    each_line_index (int): The current index of the line being processed.
    music_lrc_line_len_index (int): The current index of the processed line in the lyrics list.

    Returns:
    int: The updated index of the processed line in the lyrics list.

    The function iterates through each line of the lyrics, extracts the time information,
    and renders the lyrics text. It also handles any potential errors that may occur during the process.
    """
    for each_line in music_lrc_line:
        # If the current line index is out of range, break the loop.
        if each_line_index == 0 or each_line_index <= lyrics_len - len(music_lrc_line):
            break
        try:
            # Extract the time information from the current line and append it to the time list.
            lrc_time.append(int(each_line[1:3]) * 60 + int(each_line[4:6]) + int(each_line[7:9]) / 100)
            music_lrc_line_len_index += 1
        except (IndexError, TypeError, ValueError):
            # If any error occurs during the extraction process, increment the line index and continue.
            music_lrc_line_len_index += 1
        # Render the lyrics text using the lrc_font and append it to the new_lyrics list.
        img_text = lrc_font.render(each_line[10:-1], True, THECOLORS.get("grey80"))
        # if img_text.get_width() > 630:
        # 	pass
        new_lyrics.append(img_text)
    # Return the updated index of the processed line in the lyrics list.
    return music_lrc_line_len_index

def flip_the_lyrics(_roll_two_lrc_line, _now_lyc_time):
    """
    This function handles the rolling of lyrics based on the current time.

    Parameters:
    _roll_two_lrc_line (bool): A flag indicating whether to roll two lines of lyrics.
    _now_lyc_time (float): The current time of the music.

    Returns:
    bool: A flag indicating whether to roll two lines of lyrics.

    The function iterates through the time list of lyrics. If the current time is within a certain range of a time unit,
    it sets the highlight index, checks if the lyrics should roll, and updates the necessary variables.
    """
    global music_lrc_is_roll, highlight_lrc_index, highlight_lrc_last, lrc_line_index, move_text
    for time_unit in lrc_time:
        # 遍历时间列表，判断是否到了下一行歌词的时间
        if _now_lyc_time - 0.1 <= time_unit <= _now_lyc_time + 0.1:
            highlight_lrc_index = lrc_time.index(time_unit) - 1
            if branch_lrc_text is False:
                highlight_lrc_index += 1
            if lrc_time[lrc_time.index(time_unit)] == time_unit:
                _roll_two_lrc_line = True
            if highlight_lrc_index < 0:
                highlight_lrc_index = 0
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
    return _roll_two_lrc_line

def manipulate_the_music_object():
    """
    Manipulates the music object based on the current state and user interactions.

    This function handles the music playback, including single-track looping,
    normal track transition, transition to the end of the list, list looping,
    and pausing the music when the user presses the 'Push' button.
    """
    global music_is_load, music_list_index, music_player

    if music_is_load is False and loop_music is True and button_loop.display_button is True:  # 单曲循环
        music_list_index -= 1
        music_list_index = load_music(music_list_index)
        music_player = True
        music_is_load = True
        init_music_argument()
        music.play()
        parameter.change_music_last(music_list[music_list_index])
    elif music_is_load is False and 0 <= music_list_index < len(music_list):  # 正常一曲终了后播放下一曲
        music_list_index = load_music(music_list_index)
        music_player = True
        music_is_load = True
        init_music_argument()
        music.play()
        parameter.change_music_last(music_list[music_list_index])
    elif music_is_load is False and 0 > music_list_index:  # 在列表开头按下上一曲按钮，播放列表结尾的曲子
        music_list_index = len(music_list) - 1
        music_list_index = load_music(music_list_index)
        music_player = True
        music_is_load = True
        init_music_argument()
        music.play()
        parameter.change_music_last(music_list[music_list_index])
    elif music_is_load is False and loop_music is True and button_loop.display_button is False:  # 列表循环
        music_player = False
        music_is_load = False
        init_music_argument()
        music_list_index = 0
    elif music_is_load is False and loop_music is False:  # 顺序播放播完时，啥都不干
        music_player = False
        music_is_load = False
        init_music_argument()
    if music_push_load is True:
        music.pause()

def if_cannot_use_lyrics():
    """
    This function checks if the lyrics can be used or not.

    Raises:
    IndexError: If the index is out of range.

    The function checks if the length of the lyrics is less than 4 or if the last line
    of the lyrics contains "[99:00.00]".
    If either of these conditions is true, it sets the message of the middle lyric
    to "未找到歌词！" or "纯音乐 请欣赏" respectively.
    If an IndexError is raised, it sets the message of the middle lyric to "歌词文件未找到！".
    """
    global music_is_pure_music, lrc_line_index
    try:
        if music_lrc_line_len < 4:
            lyrics[int(lyrics_len / 2)].set_msg("未找到歌词！")
            music_is_pure_music = True
        elif music_lrc_line_len >= 4 and music_lrc_line[music_lrc_line_len - 1].find("[99:00.00]") != -1:
            lyrics[int(lyrics_len / 2)].set_msg("纯音乐 请欣赏")
            music_is_pure_music = True
    except IndexError:
        lyrics[int(lyrics_len / 2)].set_msg("歌词文件未找到！")
        music_is_pure_music = True

def get_music_spectrum():
    """
    This function calculates and stores the music spectrum for each second.

    Parameters:
    music_list_index (int): The index of the current music file in the music list.
    music_kry_length (float): The length of the music file in seconds.
    r_per_second_film (list): A list to store the music spectrum for each second.

    Returns:
    None. The function modifies the global variable `r_per_second_film`.

    The function uses the `librosa.load()` function to load the music file specified by
    `music_path + music_list[music_list_index]`. It then calculates the number of samples
    per second by dividing the total number of samples by the music length in seconds.
    It initializes variables `_start`, `_end`, and `_i` to iterate over the music file.
    For each second in the music file, the function appends the spectrum of that second to
    `r_per_second_film`. The iteration stops when the number of seconds reaches the music length.
    """
    global music_list_index, music_kry_length, r_per_second_film
    r_per_second_film = []
    _r_music_film, sr = librosa.load(music_path + music_list[music_list_index])
    _r_per_second = int(len(_r_music_film) / int(music_kry_length))
    _start, _end, _i = 0, _r_per_second, 0
    for _second in _r_music_film:
        try:
            r_per_second_film.append(_r_music_film[_start:_end])
        except IndexError:
            break
        _start += _r_per_second
        _end += _r_per_second
        _i += 1
        if _i >= int(music_kry_length):
            break

def cal_second_music_spectrum():
    """
    Calculates and stores the music spectrum for each second.

    Parameters:
    r_per_second_film (list): A list containing the music spectrum for each second.
    music (pygame.mixer.music): The music object used to play the audio file.

    Returns:
    bool: True if the music spectrum for the current second is successfully calculated and stored.
        False if an IndexError occurs while accessing the music spectrum for the current second.

    The function calculates the music spectrum for each second by accessing the corresponding
    spectrum from the `r_per_second_film` list. It then stores the calculated spectrum in the
    `now_music_spectrum` list. The function returns True if the music spectrum for the current
    second is successfully calculated and stored. If an IndexError occurs while accessing the
    music spectrum for the current second, the function returns False.
    """
    global r_per_second_film, now_music_spectrum
    now_music_spectrum = []
    _now_r_list = []
    _music_spectrum_number = 400
    try:
        _now_r_list = r_per_second_film[int(music.get_pos() / 1000)]
    except IndexError:
        return False
    _one_object_number = int(len(_now_r_list) / _music_spectrum_number)
    _start, _end, _i = 0, _one_object_number, 0
    for _second in _now_r_list:
        try:
            now_music_spectrum.append(int(_now_r_list[_start:_end][int(_one_object_number / 2)] * 1000))
        except IndexError:
            break
        _start += _one_object_number
        _end += _one_object_number
        _i += 1
        if _i >= _music_spectrum_number:
            break
    return True

def set_the_lyrics():
    """
    This function sets the lyrics on the display.

    The function checks if the lyrics can be used or not using the `if_cannot_use_lyrics()` function.
    If the lyrics can be used, it checks the length of the lyrics and the index to write the lyrics.
    If the length of the lyrics is less than or equal to the number of lines available on the display,
    it writes the lyrics from the fourth line to the end of the display.
    If the length of the lyrics is greater than the number of lines available on the display,
    it writes the lyrics from the fourth line to the number of lines available on the display,
    and updates the index to write the lyrics.
    If an IndexError is raised, it decrements the index to write the lyrics.
    """
    global music_is_pure_music, lrc_line_index
    if_cannot_use_lyrics()
    if music_lrc_line_len >= 4 and music_is_pure_music is False:
        if music_lrc_line_len - 4 <= lyrics_len:
            for write_index in range(0, music_lrc_line_len - 4):
                lyrics[lyrics_len - write_index - 1].set_msg(str(music_lrc_line[write_index + 4][10:-1]))
        else:
            try:
                for write_index in range(0, lyrics_len):
                    lyrics[lyrics_len - write_index - 1].set_msg(
                        str(music_lrc_line[write_index + lrc_line_index + 4][10:-1]))
            except IndexError:
                lrc_line_index -= 1

def continuous_rolling_lyrics():
    """
    This function handles the continuous rolling of lyrics on the display.

    The function first checks if the lyrics can be used or not using the `if_cannot_use_lyrics()` function.
    If the lyrics can be used, it checks the length of the lyrics and the index to write the lyrics.
    If the length of the lyrics is less than or equal to the number of lines available on the display,
    it writes the lyrics from the fourth line to the end of the display.
    If the length of the lyrics is greater than the number of lines available on the display,
    it does not write any lyrics, as continuous rolling is not applicable in this case.
    """
    if_cannot_use_lyrics()
    if music_lrc_line_len >= 4 and music_is_pure_music is False:
        if music_lrc_line_len - 4 <= lyrics_len:
            for write_index in range(0, music_lrc_line_len - 4):
                lyrics[lyrics_len - write_index - 1].set_msg(str(music_lrc_line[write_index + 4][10:-1]))
        else:
            pass

def set_the_film_list():
    """
    This function sets the names of the music files in the list on the display.

    The function uses the global variable 'music_list' and 'lyrics_len' to get the list of music files and
    the number of lines in the display, respectively.
    It then iterates over the list of music files and sets the names of the files on the display.
    If the number of music files is greater than the number of lines in the display, it uses a scrolling
    mechanism to display all the files.
    """
    global lrc_line_index
    if len(music_list) <= lyrics_len:
        for write_index in range(0, len(music_list)):
            _film_name = str(music_list[write_index]).split("/")[-1]
            lyrics[lyrics_len - write_index - 1].set_msg(_film_name)
    else:
        try:
            for write_index in range(0, lyrics_len):
                _film_name = str(music_list[write_index + lrc_line_index]).split("/")[-1]
                lyrics[lyrics_len - write_index - 1].set_msg(_film_name)
        except IndexError:
            lrc_line_index -= 1

def set_the_information():
    """
    This function sets the music information on the display.

    The function sets the names of the music file, artist, album, sample rate, number of channels,
    music length, and the ID3v2 version on the display.
    """
    prefix = "                                    "
    lyrics[lyrics_len - 2].set_msg(prefix + "歌曲名")
    lyrics[lyrics_len - 3].set_msg(prefix + "->  " + str(music_key_name))
    lyrics[lyrics_len - 4].set_msg(prefix + "艺术家名")
    lyrics[lyrics_len - 5].set_msg(prefix + "->  " + str(music_key_arties))
    lyrics[lyrics_len - 6].set_msg(prefix + "专辑名")
    lyrics[lyrics_len - 7].set_msg(prefix + "->  " + str(music_key_albums))
    lyrics[lyrics_len - 9].set_msg(prefix + "sr: " + str(music_key_sample_rate) + "Hz  ca: " +
                                   str(music_key_channels) + "  len: " + str(int(music_kry_length)) + "s")
    lyrics[lyrics_len - 10].set_msg(prefix + "use ID3v2")
    lyrics[lyrics_len - 13].set_msg(prefix + "freebird fly in the sky!")

def set_the_settings():
    lyrics[int(lyrics_len / 2)].set_msg("")
    lyrics[lyrics_len - 1].set_msg("滚动歌词       歌词分行       键盘快捷键     背景切换")

def set_the_home_page():
    """
    This function sets the home page display with the last played music,
    the top 3 most frequently played songs, and other relevant information.
    """
    music_last_name = parameter.get_music_last().split("/")[-1][:-4]
    music_time = parameter.get_music_time().items()
    music_time_name, music_time_num = [], []
    for unit in music_time:
        music_time_name.append([str(unit[0]), unit[1]])
        music_time_num.append(unit[1])
    music_time_num = sorted(music_time_num)[-4:]
    music_time_top_1, music_time_top_2, music_time_top_3 = "None", "None", "None"
    music_time_top_index = 0
    try:
        for unit in music_time_name:
            if unit[1] == music_time_num[2] and music_time_top_index == 0:
                music_time_top_1 = unit[0].split("/")[-1][:-4]
                music_time_top_index += 1
                continue
            elif unit[1] == music_time_num[1] and music_time_top_index == 1:
                music_time_top_2 = unit[0].split("/")[-1][:-4]
                music_time_top_index += 2
                continue
            elif unit[1] == music_time_num[0] and music_time_top_index == 2:
                music_time_top_3 = unit[0].split("/")[-1][:-4]
                music_time_top_index += 3
                break
    except IndexError:
        music_time_top_1, music_time_top_2, music_time_top_3 = "None", "None", "None"
    # music_other = music_list[random.randint(0, len(music_list) - 1)].split("/")[-1][:-4]
    lyrics[lyrics_len - 1].set_msg("主页面")
    lyrics[lyrics_len - 3].set_msg("上次播放歌曲 -> " + str(music_last_name))
    lyrics[lyrics_len - 5].set_msg("播放频率top3")
    lyrics[lyrics_len - 7].set_msg("top1 -> " + music_time_top_1)
    lyrics[lyrics_len - 8].set_msg("top2 -> " + music_time_top_2)
    lyrics[lyrics_len - 9].set_msg("top3 -> " + music_time_top_3)
    
def set_the_list_page():
    global now_play_list
    lyrics[lyrics_len - 1].set_msg("请忽略此页，再翻一页到频谱")
    # lyrics[lyrics_len - 3].set_msg("-<选择列表>-")
    # lyrics[lyrics_len - 5].set_msg("加入列表或移出列表")
    # lyrics[lyrics_len - 6].set_msg("创建列表或删除列表")
    # lyrics[lyrics_len - 8].set_msg("当前播放列表")
    # lyrics[lyrics_len - 9].set_msg("->  " + str(now_play_list))
    lyrics[lyrics_len - 11].set_msg("还未完工")

def set_the_music_spectrum():
    lyrics[lyrics_len - 1].set_msg("频谱图页面/每秒")


# 主循环
while True:
    # 设置状态栏
    event_text.set_msg("现在时间：" + str(time.localtime().tm_year) + "年 " + str(time.localtime().tm_mon) + "月 " +
                       str(time.localtime().tm_mday) + "日 " + str(time.localtime().tm_hour) + "时 " +
                       str(time.localtime().tm_min) + "分 " + str(time.localtime().tm_sec) + "秒   " +
                       "当前帧速率 " + str(int(clock.get_fps())) + "     Copyright (c) 2023 freebird")
    # 事件和信号遍历
    for event in pygame.event.get():
        _user_use_MOUSEWHEEL = False
        if event.type == MUSICOVER:
            music_list_index += 1   # 一曲播放完，更新文件列表索引
            music_is_load = False
            music_player = False
        if event.type == pygame.QUIT:
            parameter.change_music_last(music_list[music_list_index])
            parameter.update_parameter()
            parameter.save_parameter()
            try:
                os.remove("music_image_film.music_image")
            except FileNotFoundError:
                pass
            freetype.quit()
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
        # elif event.type == pygame.MOUSEMOTION and 5 < pygame.mouse.get_pos()[0] < display_size[0] - 85 and \
        # 		42 < pygame.mouse.get_pos()[1] < display_size[1] - 93 and _user_use_MOUSEWHEEL is False:
        # 	if event.dict.get("touch") is True:
        # 		if event.dict.get("y") >= 0:
        # 			lrc_line_index -= 1
        # 		elif event.dict.get("y") <= 0:
        # 			lrc_line_index += 1
        # 		move_text = True
        elif 5 < pygame.mouse.get_pos()[0] < display_size[0] - 85 and \
                5 < pygame.mouse.get_pos()[1] < 40 and event.type == pygame.MOUSEBUTTONDOWN:
            # 判断用户是否点击了歌曲文件名
            if (sea_music_list is False and sea_music_film is False and
                    sea_setting_film is False and sea_home_page is False
                    and sea_list_page is False and sea_music_spectrum is False):
                sea_music_list = True
                sea_music_film = False
                sea_setting_film = False
                sea_home_page = False
                sea_list_page = False
                sea_music_spectrum = False
            elif (sea_music_list is True and sea_music_film is False and
                  sea_setting_film is False and sea_home_page is False
                  and sea_list_page is False and sea_music_spectrum is False):
                sea_music_list = False
                sea_music_film = True
                sea_setting_film = False
                sea_home_page = False
                sea_list_page = False
                sea_music_spectrum = False
            elif (sea_music_list is False and sea_music_film is True and
                  sea_setting_film is False and sea_home_page is False
                  and sea_list_page is False and sea_music_spectrum is False):
                sea_music_list = False
                sea_music_film = False
                sea_setting_film = True
                sea_home_page = False
                sea_list_page = False
                sea_music_spectrum = False
            elif (sea_music_list is False and sea_music_film is False and
                  sea_setting_film is True and sea_home_page is False
                  and sea_list_page is False and sea_music_spectrum is False):
                sea_music_list = False
                sea_music_film = False
                sea_setting_film = False
                sea_home_page = True
                sea_list_page = False
                sea_music_spectrum = False
            elif (sea_music_list is False and sea_music_film is False and
                  sea_setting_film is False and sea_home_page is True
                  and sea_list_page is False and sea_music_spectrum is False):
                sea_music_list = False
                sea_music_film = False
                sea_setting_film = False
                sea_home_page = False
                sea_list_page = True
                sea_music_spectrum = False
            elif (sea_music_list is False and sea_music_film is False and
                  sea_setting_film is False and sea_home_page is False
                  and sea_list_page is True and sea_music_spectrum is False):
                sea_music_list = False
                sea_music_film = False
                sea_setting_film = False
                sea_home_page = False
                sea_list_page = False
                sea_music_spectrum = True
            else:
                sea_music_list = False
                sea_music_film = False
                sea_setting_film = False
                sea_home_page = False
                sea_list_page = False
                sea_music_spectrum = False
            move_text = True
        elif event.type == pygame.KEYDOWN and use_keyboard_to_set is True:   # 键盘事件
            if event.key == pygame.K_b:
                pg_wind_music_index -= 1     # 切换背景
            elif event.key == pygame.K_x:
                if use_blur_image is True:
                    use_blur_image = False
                else:
                    use_blur_image = True
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
            elif event.key == pygame.K_f:
                if branch_lrc_text is True:
                    branch_lrc_text = False
                else:
                    branch_lrc_text = True
                music_player = True
                music_is_load = True
                init_music_argument()
            elif event.key == pygame.K_s:
                if sea_setting_film is False:
                    sea_setting_film = True
                else:
                    sea_setting_film = False
                move_text = True
            elif event.key == pygame.K_SPACE:
                if icon_play.display_button is False:  # 播放和暂停时的按钮样式
                    icon_play.display_button = True
                    icon_stop.display_button = False
                    music_push_load = True
                    music.pause()
                else:
                    icon_play.display_button = False
                    icon_stop.display_button = True
                    if music_player is True:
                        music.unpause()
                        music_push_load = False
                    else:
                        music.play()
                        music_player = True
                        music_push_load = False

        # 以下调用了freebutton.position_button()的都是按钮
        # 注意，所有以下代码中按钮的操作都只是改变样貌或控制音乐的暂停和再次播放！
        # 对于音乐对象本身的操作（如切换音乐等）在事件遍历的下面，这里只是再次发出信号
        elif freebutton.position_button_class(button_exit, pygame.mouse.get_pos()) is True:
            button_exit.set_msg_color(THECOLORS.get("grey95"))
            button_exit.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                parameter.change_music_last(music_list[music_list_index])
                parameter.update_parameter()
                parameter.save_parameter()
                try:
                    os.remove("music_image_film.music_image")
                except FileNotFoundError:
                    pass
                freetype.quit()
                music.stop()
                pygame.quit()
                sys.exit()
        elif freebutton.position_button([330, 390, 415, 475], pygame.mouse.get_pos()) is True:
            icon_play.set_index(1)
            icon_play.check_button = True
            icon_stop.set_index(1)
            icon_stop.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if icon_play.display_button is False:  # 播放和暂停时的按钮样式
                    icon_play.display_button = True
                    icon_stop.display_button = False
                    music_push_load = True
                    music.pause()
                else:
                    icon_play.display_button = False
                    icon_stop.display_button = True
                    if music_player is True:
                        music.unpause()
                        music_push_load = False
                    else:
                        music.play()
                        music_player = True
                        music_push_load = False
        elif freebutton.position_button([410, 450, 425, 465], pygame.mouse.get_pos()) is True:
            icon_next.set_index(1)
            icon_next.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                music.pause()
                music_player = False
                music_is_load = False
                music_list_index += 1
                move_text = True
        elif freebutton.position_button([270, 310, 425, 465], pygame.mouse.get_pos()) is True:
            icon_last.set_index(1)
            icon_last.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                music.pause()
                music_player = False
                music_is_load = False
                music_list_index -= 1
                move_text = True
        elif freebutton.position_button([475, 515, 425, 465], pygame.mouse.get_pos()) is True:
            icon_paper_plane.set_index(1)
            icon_paper_plane.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    _music_film = dialog_box.save_msg()
                    for unit in music_lrc_line:
                        _music_film.write(unit)
                    _music_film.close()
                except (IndexError, AttributeError):
                    pass
        elif freebutton.position_button([205, 245, 425, 465], pygame.mouse.get_pos()) is True:
            icon_film.set_index(1)
            icon_film.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                _music_film = dialog_box.film_msg()
                for unit in _music_film:
                    suffix = unit[len(unit) - 4:]
                    if suffix != ".mp3" and suffix != ".wav" and suffix != ".ogg":
                        if suffix == ".lrc":
                            music_lrc_list.append(unit)
                        continue
                    music_list.append(unit)
        elif freebutton.position_button([660, 700, 175, 215], pygame.mouse.get_pos()) is True:
            icon_vol_open.set_index(1)
            icon_vol_open.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                music.set_volume(music.get_volume() + 0.05)   # 音量加
        elif freebutton.position_button([660, 700, 235, 275], pygame.mouse.get_pos()) is True:
            icon_vol_close.set_index(1)
            icon_vol_close.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                music.set_volume(music.get_volume() - 0.05)   # 音量减
        elif freebutton.position_button_class(button_loop, pygame.mouse.get_pos()) is True:
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
        elif freebutton.position_button([660, 700, 370, 410], pygame.mouse.get_pos()) is True:
            icon_home.set_index(1)
            icon_home.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sea_home_page is False:
                    sea_music_list = False
                    sea_music_film = False
                    sea_setting_film = False
                    sea_home_page = True
                else:
                    sea_music_list = False
                    sea_music_film = False
                    sea_setting_film = False
                    sea_home_page = False
                move_text = True
        elif freebutton.position_button_class(button_set_branch, pygame.mouse.get_pos()) is True:
            button_set_branch.set_msg_color(THECOLORS.get("grey95"))
            button_set_branch.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN and sea_setting_film is True:
                if branch_lrc_text is True:
                    branch_lrc_text = False
                else:
                    branch_lrc_text = True
                music_player = True
                music_is_load = True
                init_music_argument()
        elif freebutton.position_button_class(button_set_highlight, pygame.mouse.get_pos()) is True:
            button_set_highlight.set_msg_color(THECOLORS.get("grey95"))
            button_set_highlight.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN and sea_setting_film is True:
                if show_highlight is True:
                    show_highlight = False
                else:
                    show_highlight = True
        elif freebutton.position_button_class(button_set_Keyboard, pygame.mouse.get_pos()) is True:
            button_set_Keyboard.set_msg_color(THECOLORS.get("grey95"))
            button_set_Keyboard.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN and sea_setting_film is True:
                if use_keyboard_to_set is True:
                    use_keyboard_to_set = False
                else:
                    use_keyboard_to_set = True
        elif freebutton.position_button_class(button_set_image, pygame.mouse.get_pos()) is True:
            button_set_image.set_msg_color(THECOLORS.get("grey95"))
            button_set_image.check_button = True
            if event.type == pygame.MOUSEBUTTONDOWN and sea_setting_film is True:
                pg_wind_music_index -= 1
        elif sea_home_page is True:
            if freebutton.position_button_class(lyrics[lyrics_len - 3], pygame.mouse.get_pos()) is True:
                lyrics[lyrics_len - 3].set_msg_color(THECOLORS.get("grey100"))
                lyrics[lyrics_len - 3].check_button = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sea_music_list = False
                    sea_music_film = False
                    sea_setting_film = False
                    sea_home_page = False
                    move_text = True
                    try:
                        _index = music_list.index(music_last)
                    except ValueError:
                        music_list.append(music_last)
                        _index = len(music_list) - 1
                    finally:
                        music_list_index = load_music(_index)
                        music_player = True
                        music_is_load = True
                        init_music_argument()
                        music.play()
        elif sea_list_page is True:
            if freebutton.position_button_class(lyrics[lyrics_len - 3], pygame.mouse.get_pos()) is True:
                lyrics[lyrics_len - 3].set_msg_color(THECOLORS.get("grey100"))
                lyrics[lyrics_len - 3].check_button = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("x")
            elif freebutton.position_button_class(lyrics[lyrics_len - 5], pygame.mouse.get_pos()) is True:
                lyrics[lyrics_len - 5].set_msg_color(THECOLORS.get("grey100"))
                lyrics[lyrics_len - 5].check_button = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("x2")
            elif freebutton.position_button_class(lyrics[lyrics_len - 6], pygame.mouse.get_pos()) is True:
                lyrics[lyrics_len - 6].set_msg_color(THECOLORS.get("grey100"))
                lyrics[lyrics_len - 6].check_button = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("X3")
        else:
            for unit in button:
                unit.check_button = False  # 这里的check_button是用于控制按钮是否被按下的，上面的代码中也有
            for unit in set_button:
                unit.check_button = False
            for unit in icon:
                unit.check_button = False
            for unit in lyrics:
                unit.check_button = False
        if event.type == pygame.WINDOWLEAVE:  # 当光标离开窗口后，坐标依然停留在离开前的位置，可能造成按钮一直被按下的假象
            for unit in button:               # 所以这里在设置一次
                unit.check_button = False
            for unit in set_button:
                unit.check_button = False
            for unit in icon:
                unit.check_button = False
            for unit in lyrics:
                unit.check_button = False

    # 以下代码接受从事件遍历中发出的信号，对音乐对象进行操作，注意，有先后顺序！
    try:
        manipulate_the_music_object()
    except pygame.error:
        music_list_index += 1

    # 获取标签信息
    if music_is_load is True and music_key_is_load is False:
        try:
            get_the_tag_information()
            music_key_is_load = True
        except IndexError:
            music_key_is_load = False

    # 以下代码用于检测歌词，排版与打印歌词
    lyrics_len = len(lyrics)   # 歌词显示列表的长度
    if music_is_load is True and music_lrc_is_load is False and music_lrc_is_read is False:  # 载入歌词
        get_lrc_from_lrc_film(lyrics_len)

    # 读取标签信息后，使用标签信息作为歌曲信息
    if music_lrc_is_load is False and music_key_is_load is True and music_key_is_read is False:
        use_tag_information_as_a_song_message()

    # 如果没有读取标签，使用文件名作为歌曲信息
    if music_lrc_is_load is False and music_key_is_load is False and music_key_is_read is False:
        use_filename_as_a_song_message()

    if music_lrc_is_load is True and music_lrc_is_read is False:  # 读取歌词
        read_the_lyrics()

    # 计算频谱图
    now_music_time = int(music.get_pos() / 1000)
    if cal_music_spectrum is True:
        get_music_spectrum()
        cal_music_spectrum = False
    if last_play_second != now_music_time:
        last_play_second = now_music_time
        if cal_second_music_spectrum() is False:
            now_music_spectrum = []

    if sea_music_list is False:
        if lrc_line_index < 0:
            lrc_line_index = 0
        elif lrc_line_index > music_lrc_line_len - lyrics_len:
            lrc_line_index = music_lrc_line_len - lyrics_len
    else:
        if lrc_line_index < 0:
            lrc_line_index = 0
        elif lrc_line_index > len(music_list) - lyrics_len:
            lrc_line_index = len(music_list) - lyrics_len
    if move_text is True:
        for unit in lyrics:
            unit.set_msg("")

    if (sea_music_list is False and sea_music_film is False and sea_setting_film is False and sea_home_page is False and
            sea_list_page is False and sea_music_spectrum is False and move_text is True):
        set_the_lyrics()

    elif sea_music_list is True and move_text is True:
        set_the_film_list()

    elif sea_music_film is True and move_text is True:
        set_the_information()

    elif sea_setting_film is True and move_text is True:
        set_the_settings()

    elif sea_home_page is True and move_text is True:
        set_the_home_page()

    elif sea_list_page is True and move_text is True:
        set_the_list_page()

    elif sea_music_spectrum is True and move_text is True:
        set_the_music_spectrum()

    move_text = False

    # 自动翻动歌词
    now_time = time.time()
    now_lyc_time = float(music.get_pos() / 1000)
    roll_two_lrc_line = False
    if sea_music_list is False and music_lrc_is_read is True and show_highlight is True:
        roll_two_lrc_line = flip_the_lyrics(roll_two_lrc_line, now_lyc_time)
    if roll_two_lrc_line is True or highlight_lrc_last == highlight_lrc_index:
        music_lrc_is_roll = False

    dirty_rects.append(pygame.Rect(0, 0, 720, 480))  # 全屏需要更新

    # 打印歌词
    # if sea_music_list is False and sea_music_film is False and move_text is True:
    # 	if music_lrc_line_len - 4 <= lyrics_len:
    # 		for write_index in range(0, music_lrc_line_len - 4):
    # 			screen.blit(new_lyrics[lyrics_len - write_index - 1], (5, 220))
    # 	else:
    # 		try:
    # 			for write_index in range(0, lyrics_len):
    # 				screen.blit(new_lyrics[lyrics_len - write_index - 1], (5, 220))
    # 		except IndexError:
    # 			lrc_line_index -= 1
    # elif sea_music_list is True and move_text is True:
    # 	lyrics[int(lyrics_len / 2)].set_msg("")
    # 	if len(music_list) <= lyrics_len:
    # 		for write_index in range(0, len(music_list)):
    # 			lyrics[lyrics_len - write_index - 1].set_msg(str(music_list[write_index]))
    # 	else:
    # 		try:
    # 			for write_index in range(0, lyrics_len):
    # 				lyrics[lyrics_len - write_index - 1].set_msg(str(music_list[write_index + lrc_line_index]))
    # 		except IndexError:
    # 			lrc_line_index -= 1
    if (sea_setting_film is False and sea_home_page is False and sea_list_page is False and
            sea_music_spectrum is False and show_highlight is True):
        if sea_music_list is False and sea_music_film is False and music_is_pure_music is False:
            if len(music_lrc_line) <= 14:
                line_index = 14 - highlight_lrc_index
            else:
                line_index = 14 - (highlight_lrc_index - lrc_line_index)
                if line_index < 0 or line_index > 13:
                    line_index = 100
            pygame.draw.rect(screen, pg_wind_color[pg_wind_music_index - 1],
                             (0, display_size[1] - 133 - 20 * line_index, 636, 19), 0)
        elif sea_music_list is True and sea_music_film is False:
            if len(music_list) <= 14:
                line_index = 14 - music_list_index
            else:
                line_index = 14 - (music_list_index - lrc_line_index)
                if line_index < 0 or line_index > 13:
                    line_index = 100
            pygame.draw.rect(screen, pg_wind_color[pg_wind_music_index - 1],
                             (0, display_size[1] - 133 - 20 * line_index, 636, 19), 0)
    for unit in lyrics:
        unit.draw()
    if len(music_arties.get_attribute().get("msg")) > 70:
        music_arties.set_msg(str(music_arties.get_attribute().get("msg"))[:70] + "...")
    music_arties.draw()
    music_name.draw()

    # 以下代码打印窗口上的元素，包括按钮，文本之类的对象
    if sea_music_film is True and music_key_image is not None and sea_setting_film is False:
        screen.blit(music_key_image, (10, 90))
    if pg_wind_music_index < 1:
        pg_wind_music_index = 4
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
    for unit in icon:
        if unit.display_button is False:
            continue
        if unit.check_button is False:
            unit.set_index(0)
        unit.draw()
    for unit in lyrics:
        if unit.check_button is False:
            unit.set_msg_color(THECOLORS.get("grey95"))
    if sea_setting_film is True:
        for unit in set_button:
            if unit.check_button is False:
                unit.set_msg_color(THECOLORS.get("grey75"))
            unit.draw()
    # if pygame.mouse.get_pressed()[0]:
    # 	for unit in particle:
    # 		screen.blit(unit, pygame.mouse.get_pos())
    if 0 <= music_list_index < len(music_list):  # 显示音乐的名称
        if len(str(music_list[music_list_index])) <= 65:
            music_name_text.set_msg("文件名称 -> " + str(music_list[music_list_index]))
        else:
            music_name_text.set_msg("文件名称 -> " + str(music_list[music_list_index])[:65] + "...")
    time_num.set_msg(str(now_music_time) + "s")
    if now_music_time == 60:
        need_to_save = True
        _new_time_dict = parameter.get_music_time()
        if _new_time_dict.get(str(music_list[music_list_index])) is None:
            _new_time_dict[str(music_list[music_list_index])] = 1
        else:
            _new_time_dict[str(music_list[music_list_index])] += 1
        parameter.change_music_time(_new_time_dict)
    vol_num.set_msg(str(int(music.get_volume() * 100)))
    for unit in text:
        unit.draw()
    if music_kry_length > 0 and now_music_time > 0:
        playback_schedule = 720 * (now_music_time / music_kry_length)
        pygame.draw.aaline(screen, THECOLORS.get("grey50"), (0, 479), (playback_schedule, 479))
        pygame.draw.aaline(screen, THECOLORS.get("grey50"), (0, 478), (playback_schedule, 478))
    if sea_music_spectrum is True:
        height_down = display_size[1] - 110
        height_top = 100
        height = height_down - height_top
        weight_left = 10
        weight_right = 625
        weight = weight_right - weight_left
        pygame.draw.rect(screen, THECOLORS.get("grey50"), (weight_left, height_top, weight, height), 1)
        each_width = weight / 400
        each_i = 0
        for _each in now_music_spectrum:
            if _each >= (height_down - height_top):
                _each = height_down - height_top
            pygame.draw.rect(screen, THECOLORS.get("grey80"), (weight_left + (each_width * each_i),
                                                               (height_down - _each),
                                                               each_width, _each))
            each_i += 1

    # 窗口刷新，准备再次遍历事件
    # pygame.display.update(dirty_rects)
    pygame.display.flip()
    if pg_wind_music_index < 1:
        pg_wind_music_index = 4
    if pg_wind_music_index == 1:
        screen.blit(pg_wind_music[0], (0, 0))
    elif pg_wind_music_index == 2:
        screen.blit(pg_wind_music[1], (0, 0))
    elif pg_wind_music_index == 3:
        screen.blit(pg_wind_music[2], (0, 0))
    elif pg_wind_music_index == 4:
        if use_blur_image is True:
            screen.blit(blur_image, (-40, -160))
        else:
            screen.blit(pg_wind_music[0], (0, 0))
    clock.tick(frame_number)  # 控制帧数
    dirty_rects.clear()
