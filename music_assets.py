import pygame
import dialog_box

def check_film():
    return True

def init_icon():
    try:
        text_font = pygame.font.Font("assets\\ZhiyongWrite-2.ttf", 22)
        lrc_font = pygame.font.Font("assets\\simhei.ttf", 20)
        pg_wind_music1 = pygame.image.load("assets\\wind_music.JPG").convert(24)
        pg_wind_music2 = pygame.image.load("assets\\wind_music2.JPG").convert(24)
        pg_wind_music3 = pygame.image.load("assets\\wind_music3.jpg").convert(24)
        pg_wind_music1_r = pygame.image.load("assets\\wind_music_r.JPG").convert(24)
        pg_wind_music2_r = pygame.image.load("assets\\wind_music2_r.JPG").convert(24)
        pg_wind_music3_r = pygame.image.load("assets\\wind_music3_r.jpg").convert(24)
        pg_wind_music = [pg_wind_music1, pg_wind_music2, pg_wind_music3]
        pg_wind_music_r = [pg_wind_music1_r, pg_wind_music2_r, pg_wind_music3_r]
        pg_wind_color = [(0, 105, 70), (0, 20, 105), (137, 30, 0)]
        icon_play = [pygame.image.load("assets\\icon\\play_1.png"),
                     pygame.image.load("assets\\icon\\play_2.png"), 0, (330, 415), 0]
        icon_stop = [pygame.image.load("assets\\icon\\stop_1.png"),
                     pygame.image.load("assets\\icon\\stop_2.png"), 0, (330, 415), 0]
        icon_last = [pygame.image.load("assets\\icon\\last_1.png"),
                     pygame.image.load("assets\\icon\\last_2.png"), 0, (270, 425), 0]
        icon_next = [pygame.image.load("assets\\icon\\next_1.png"),
                     pygame.image.load("assets\\icon\\next_2.png"), 0, (410, 425), 0]
        icon_vol_open = [pygame.image.load("assets\\icon\\vol_open_1.png"),
                         pygame.image.load("assets\\icon\\vol_open_2.png"), 0, (660, 185), 0]
        icon_vol_close = [pygame.image.load("assets\\icon\\vol_close_1.png"),
                          pygame.image.load("assets\\icon\\vol_close_2.png"), 0, (660, 255), 0]
        icon_setting = [pygame.image.load("assets\\icon\\setting_1.png"),
                        pygame.image.load("assets\\icon\\setting_2.png"), 0, (0, 0), 0]
        icon_trash = [pygame.image.load("assets\\icon\\trash_1.png"),
                      pygame.image.load("assets\\icon\\trash_2.png"), 0, (0, 0), 0]
        icon_random = [pygame.image.load("assets\\icon\\random_1.png"),
                       pygame.image.load("assets\\icon\\random_2.png"), 0, (660, 325), 0]
        icon_paper_plane = [pygame.image.load("assets\\icon\\paper_plane_1.png"),
                            pygame.image.load("assets\\icon\\paper_plane_2.png"), 0, (0, 0), 0]
        icon_home = [pygame.image.load("assets\\icon\\home_1.png"),
                     pygame.image.load("assets\\icon\\home_2.png"), 0, (0, 0), 0]
        icon_frequency = [pygame.image.load("assets\\icon\\frequency_1.png"),
                          pygame.image.load("assets\\icon\\frequency_2.png"), 0, (0, 0), 0]
        icon_film = [pygame.image.load("assets\\icon\\film_1.png"),
                     pygame.image.load("assets\\icon\\film_2.png"), 0, (0, 0), 0]
        icon_cycle = [pygame.image.load("assets\\icon\\cycle_1.png"),
                      pygame.image.load("assets\\icon\\cycle_2.png"), 0, (660, 325), 0]
        icon_bird = [pygame.image.load("assets\\icon\\bird_1.png"),
                     pygame.image.load("assets\\icon\\bird_2.png"), 0, (0, 0), 0]
    except FileNotFoundError:
        dialog_box.waring_msg("Missing resource file!")
        if dialog_box.ask_msg("Want to check the resources file?") is True:
            _film = check_film()
            if _film is None:
                dialog_box.info_msg("There is no resource file deletion")
            else:
                dialog_box.info_msg("...")
        pygame.quit()
        exit()
        
    icon = [icon_play, icon_stop, icon_last, icon_next, icon_vol_open, icon_vol_close, icon_setting, icon_trash,
            icon_random, icon_paper_plane, icon_home, icon_frequency, icon_film, icon_cycle, icon_bird]
    return icon, text_font, lrc_font, pg_wind_music, pg_wind_music_r, pg_wind_color

def init_button(screen, display_size, THECOLORS, dsm):
    import freepygame.freebutton as freebutton
    button_exit = freebutton.FreeButton(screen, [display_size[0] - 80, 0], [80, 40], "EXIT", "assets\\simhei.ttf",
                                        border_color=THECOLORS.get("grey50"), draw_border=True, msg_tran=True, dsm=dsm)
    button_go = freebutton.CircleButton(screen, (int(display_size[0] / 2), display_size[1] - 35), 30, "||",
                                        "assets\\simhei.ttf",
                                        width=1, msg_tran=True, draw_border=True, border_color=THECOLORS.get("grey80"),
                                        dsm=dsm)
    button_adva = freebutton.CircleButton(screen, (int(display_size[0] / 2 + 70), display_size[1] - 35), 20, ">>",
                                          "assets\\simhei.ttf",
                                          width=1, msg_tran=True, draw_border=True,
                                          border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_back = freebutton.CircleButton(screen, (int(display_size[0] / 2 - 70), display_size[1] - 35), 20, "<<",
                                          "assets\\simhei.ttf",
                                          width=1, msg_tran=True, draw_border=True,
                                          border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_next = freebutton.CircleButton(screen, (int(display_size[0] / 2 + 125), display_size[1] - 35), 20, "|>",
                                          "assets\\simhei.ttf",
                                          width=1, msg_tran=True, draw_border=True,
                                          border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_last = freebutton.CircleButton(screen, (int(display_size[0] / 2 - 125), display_size[1] - 35), 20, "<|",
                                          "assets\\simhei.ttf",
                                          width=1, msg_tran=True, draw_border=True,
                                          border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_vol_add = freebutton.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 - 35)), 20, "V+",
                                             "assets\\simhei.ttf",
                                             width=1, msg_tran=True, draw_border=True,
                                             border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_vol_min = freebutton.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 + 35)), 20, "V-",
                                             "assets\\simhei.ttf",
                                             width=1, msg_tran=True, draw_border=True,
                                             border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_loop = freebutton.CircleButton(screen, (display_size[0] - 40, int(display_size[1] / 2 + 105)), 20, "L",
                                          "assets\\simhei.ttf",
                                          width=1, msg_tran=True, draw_border=True,
                                          border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_set_highlight = freebutton.CircleButton(screen, (30, 130), 20, "H", "assets\\simhei.ttf",
                                                   width=1, msg_tran=True, draw_border=True,
                                                   border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_set_branch = freebutton.CircleButton(screen, (150, 130), 20, "B", "assets\\simhei.ttf",
                                                width=1, msg_tran=True, draw_border=True,
                                                border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_set_Keyboard = freebutton.CircleButton(screen, (270, 130), 20, "K", "assets\\simhei.ttf",
                                                  width=1, msg_tran=True, draw_border=True,
                                                  border_color=THECOLORS.get("grey80"), dsm=dsm)
    button_set_image = freebutton.CircleButton(screen, (390, 130), 20, "I", "assets\\simhei.ttf",
                                               width=1, msg_tran=True, draw_border=True,
                                               border_color=THECOLORS.get("grey80"), dsm=dsm)
    
    button = [button_exit, button_go, button_adva, button_back, button_next, button_last, button_vol_add,
              button_vol_min, button_loop]
    set_button = [button_set_highlight, button_set_branch, button_set_Keyboard, button_set_image]
    return button, set_button

def init_text(screen, display_size, THECOLORS, dsm):
    import freepygame.freetext as freetext
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
    pleiades_text = freetext.SuperText(screen, (10, display_size[1] - 50), "Wishing well", "assets\\ZhiyongWrite-2.ttf",
                                       color=THECOLORS.get("grey100"), dsm=dsm)
    version_text = freetext.SuperText(screen, (10, display_size[1] - 20), "v 1.2.5", "assets\\simhei.ttf",
                                      size=15, color=THECOLORS.get("grey95"), dsm=dsm)
    music_name = freetext.SuperText(screen, (5, 42), "《》", "assets\\simhei.ttf", size=19,
                                    color=THECOLORS.get("grey100"), dsm=dsm)
    music_arties = freetext.SuperText(screen, (5, display_size[1] - 93), "音乐家：", "assets\\simhei.ttf",
                                      size=15, color=THECOLORS.get("grey95"), dsm=dsm)
    
    text = [vol_text, vol_num, event_text, music_name_text, time_text, time_num, freebird_text, version_text,
            pleiades_text]
    return text, music_name, music_arties

def init_lrc(screen, display_size, THECOLORS, dsm):
    import freepygame.freetext as freetext
    lyrics = [freetext.SuperText(screen, [5, (display_size[1] - 133 - 20 * index)], "", "assets\\simhei.ttf",
                                 size=16, color=THECOLORS.get("grey80"), dsm=dsm)
              for index in range(0, int((display_size[1] - 75 - 40) / 20) - 4)]  # 歌词显示列表
    return lyrics
