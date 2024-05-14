import pickle

class Parameter():

    def __init__(self, other):
        self.infor_dict = self.load_parameter(other)
        self.infor_title = self.infor_dict.get("title")
        self.infor_music_path = self.infor_dict.get("music_path")
        self.infor_music_lrc_path = self.infor_dict.get("music_lrc_path")
        self.infor_music_list = self.infor_dict.get("music_list")
        self.infor_music_lrc_list = self.infor_dict.get("music_lrc_list")
        self.infor_music_last = self.infor_dict.get("music_last")
        self.infor_music_add = self.infor_dict.get("music_add")
        self.infor_music_time = self.infor_dict.get("music_time")

    def load_parameter(self, other):
        save_film = open("assets\\information.save", "rb+")
        try:
            _infor_dict = pickle.load(save_film)
        except EOFError:
            save_film.close()
            self.init_parameter(other)
            save_film = open("assets\\information.save", "rb+")
            _infor_dict = pickle.load(save_film)
        save_film.close()
        return _infor_dict

    def change_parameter(self, new_dict : dict):
        self.infor_dict = new_dict

    def change_title(self, new_title : str):
        self.infor_title = new_title

    def change_music_path(self, new_music_path : str):
        self.infor_music_path = new_music_path

    def change_music_lrc_path(self, new_music_lrc_path : str):
        self.infor_music_lrc_path = new_music_lrc_path

    def change_music_list(self, new_music_list : list):
        self.infor_music_list = new_music_list

    def change_music_lrc_list(self, new_music_lrc_list : list):
        self.infor_music_lrc_list = new_music_lrc_list

    def change_music_last(self, new_music_last : str):
        self.infor_music_last = new_music_last

    def change_music_add(self, new_music_add : list):
        self.infor_music_add = new_music_add

    def change_music_time(self, new_music_time : dict):
        self.infor_music_time = new_music_time

    def get_title(self):
        return self.infor_title

    def get_music_path(self):
        return self.infor_music_path

    def get_music_lrc_path(self):
        return self.infor_music_lrc_path

    def get_music_list(self):
        return self.infor_music_list

    def get_music_lrc_list(self):
        return self.infor_music_lrc_list

    def get_music_last(self):
        return self.infor_music_last

    def get_music_add(self):
        return self.infor_music_add

    def get_music_time(self):
        return self.infor_music_time

    def save_parameter(self):
        pickle_film = open("assets\\information.save", "wb")
        pickle.dump(self.infor_dict, pickle_film)
        pickle_film.close()

    def update_parameter(self):
        self.infor_dict.update(title = self.infor_title)
        self.infor_dict.update(music_path = self.infor_music_path)
        self.infor_dict.update(music_lrc_path = self.infor_music_lrc_path)
        self.infor_dict.update(music_list = self.infor_music_list)
        self.infor_dict.update(music_lrc_list = self.infor_music_lrc_list)
        self.infor_dict.update(music_last = self.infor_music_last)
        self.infor_dict.update(music_add = self.infor_music_add)
        self.infor_dict.update(music_time = self.infor_music_time)

    def get_parameter(self):
        return self.infor_dict

    def init_parameter(self, other):
        _information = open("assets\\information.save", "wb+")
        pickle.dump({"title": "freebird_music_player ;-)",
                     "music_path": other[0],
                     "music_lrc_path": other[1],
                     "music_list": other[2],
                     "music_lrc_list": other[3],
                     "music_last" : "",
                     "music_add": [],
                     "music_time": {}}, _information)
        _information.close()

class PlayList():

    def __init__(self, _film_name = " "):
        self.information = self.load(_film_name)
        self.title = self.information.get("title")
        self.list_number = self.information.get("list_umber")
        self.list = self.information.get("list")

    def add(self, name, type, list, infor):
        if type == "music":
            self.list[list][name] = infor
        elif type == "list":
            self.list[list] = {}
        else:
            return False
        return True
    
    def delete(self, name, type, list):
        if type == "music":
            return self.list[list].pop(name)
        elif type == "list":
            return self.list.pop(list)
        else:
            return False
    
    def change(self, name, type, list, new, infor):
        if type == "music":
            self.list[list].pop(name)
            self.list[list][new] = infor
            return self.list.get(list).get(new)
        elif type == "list":
            self.list.pop[list]
            self.list[new] = {}
            return self.list.get(new)
        else:
            return None
    
    def in_list(self, name, type, list):
        if type == "music":
            if self.list.get(list).get(name) is not None:
                return True
            return False
        elif type == "list":
            if self.list.get(list) is not None:
                return True
            return False
        else:
            return None
    
    def get(self, list, mode = 'list'):
        if mode == 'list':
            return self.list.get(list)
        return self.list
    
    def all(self):
        return self.information
    
    def update(self):
        self.information.update(title = self.title)
        self.information.update(list_number = self.list_number)
        self.information.update(list = self.list)
    
    def save(self, _film_name = " "):
        if _film_name != " ":
            pickle_film = open(str("assets\\" + _film_name), "wb")
        else:
            pickle_film = open("assets\\play_list.save", "wb")
        pickle.dump(self.information, pickle_film)
        pickle_film.close()

    def init_save(self, _film_name = " "):
        if _film_name != " ":
            _information = open(str("assets\\" + _film_name), "wb+")
        else:
            _information = open("assets\\play_list.save", "wb+")
        pickle.dump({"title": "freebird_music_player   (*≧︶≦))(￣▽￣* )ゞ",
                     "list_number": 0,
                     "list": {}}, _information)
        _information.close()

    def load(self, _film_name = " "):
        if _film_name != " ":
            self.init_save(_film_name)
            save_film = open(str("assets\\" + _film_name), "rb+")
            _information = pickle.load(save_film)
        else:
            save_film = open("assets\\play_list.save", "rb+")
            try:
                _information = pickle.load(save_film)
            except EOFError:
                save_film.close()
                self.init_save()
                save_film = open("assets\\play_list.save", "rb+")
                _information = pickle.load(save_film)
        save_film.close()
        return _information
    
def get_music_from_music_list(name, music_list, music_path):
    if name in music_list:
        return str(music_path + name)
    return None

if __name__ == "__main__":
    name_in = "d"
    name_not_in = "h"
    music_list = ["a", "b", "c", "d", "e", "f", "g"]
    music_path = "music\\"
    print("on")
    print("--------------------------------")
    
    # music\d and None
    print(get_music_from_music_list(name_in, music_list, music_path))
    print(get_music_from_music_list(name_not_in, music_list, music_path))
    print("--------------------------------")
    playlist = PlayList("text.save")
    
    # {'title': 'freebird_music_player   (*≧︶≦))(￣▽￣* )ゞ', 'list_number': 0, 
    # 'list': {}}
    print(playlist.all())
    list_name = "my"
    
    # all True
    print(playlist.add("", "list", list_name, "my_list"))
    print(playlist.add(music_list[1], "music", "my", get_music_from_music_list(music_list[1], music_list, music_path)))
    print(playlist.add(music_list[3], "music", "my", get_music_from_music_list(music_list[3], music_list, music_path)))
    playlist.update()
    
    # {'title': 'freebird_music_player   (*≧︶≦))(￣▽￣* )ゞ', 'list_number': None, 
    # 'list': {'my': {'b': 'music\\b', 'd': 'music\\d'}}}
    print(playlist.all())
    
    # music\b and freebird
    print(playlist.delete(music_list[1], "music", "my"))
    print(playlist.change(music_list[3], "music", "my", "x", "freebird"))
    playlist.update()
    
    # {'title': 'freebird_music_player   (*≧︶≦))(￣▽￣* )ゞ', 'list_number': None, 
    # 'list': {'my': {'x': 'freebird'}}}
    print(playlist.all())
    playlist.save()
    print("--------------------------------")
    print("off")