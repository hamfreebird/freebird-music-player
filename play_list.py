import pickle

class Parameter():
    """
    This class is responsible for managing and storing various parameters related to the music player.
    """

    def __init__(self, other):
        """
        Initialize a new instance of the Parameter class.

        Parameters:
        other (list): A list containing the initial values for the parameters.
        """
        self.infor_dict = self.load_parameter(other)
        self.infor_title = self.infor_dict.get("title")
        self.infor_music_path = self.infor_dict.get("music_path")
        self.infor_music_lrc_path = self.infor_dict.get("music_lrc_path")
        self.infor_music_list = self.infor_dict.get("music_list")
        self.infor_music_lrc_list = self.infor_dict.get("music_lrc_list")
        self.infor_music_last = self.infor_dict.get("music_last")
        self.infor_music_add = self.infor_dict.get("music_add")
        self.infor_music_time = self.infor_dict.get("music_time")

    # ... other methods ...

    def load_parameter(self, other):
        """
        Load the parameters from a file.

        Parameters:
        other (list): A list containing the initial values for the parameters.

        Returns:
        dict: A dictionary containing the loaded parameters.
        """
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

    # ... other methods ...

    def save_parameter(self):
        """
        Save the current parameters to a file.
        """
        pickle_film = open("assets\\information.save", "wb")
        pickle.dump(self.infor_dict, pickle_film)
        pickle_film.close()

    # ... other methods ...

    def update_parameter(self):
        """
        Update the current parameters with the values of the instance variables.
        """
        self.infor_dict.update(title = self.infor_title)
        self.infor_dict.update(music_path = self.infor_music_path)
        self.infor_dict.update(music_lrc_path = self.infor_music_lrc_path)
        self.infor_dict.update(music_list = self.infor_music_list)
        self.infor_dict.update(music_lrc_list = self.infor_music_lrc_list)
        self.infor_dict.update(music_last = self.infor_music_last)
        self.infor_dict.update(music_add = self.infor_music_add)
        self.infor_dict.update(music_time = self.infor_music_time)

    # ... other methods ...

    def init_parameter(self, other):
        """
        Initialize the parameters with the initial values.

        Parameters:
        other (list): A list containing the initial values for the parameters.
        """
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

class PlayList():
    """
    This class is responsible for managing and storing playlists.
    It uses pickle to save and load the playlist data.
    """

    def __init__(self, _film_name=" "):
        """
        Initialize a new instance of the PlayList class.

        Parameters:
        _film_name (str): The name of the file to save the playlist data. If not provided, it defaults to "play_list.save".
        """
        self.information = self.load(_film_name)
        self.title = self.information.get("title")
        self.list_number = self.information.get("list_number")
        self.list = self.information.get("list")
        self.last_play_list = self.information.get("last_play_list")
        self.last_play_index = self.information.get("last_play_index")

    def add(self, name, type, list, infor):
        """
        Add a new item (music or list) to the playlist.

        Parameters:
        name (str): The name of the item to add.
        type (str): The type of the item to add ("music" or "list").
        list (str): The name of the list to add the item to.
        infor (str): The information associated with the music item.

        Returns:
        bool: True if the item was added successfully, False otherwise.
        """
        if type == "music":
            self.list[list][name] = infor
        elif type == "list":
            self.list[list] = {}
        else:
            return False
        return True

    # ... other methods ...

    def delete(self, name, type, list):
        """
        Delete an item (music or list) from the playlist.

        Parameters:
        name (str): The name of the item to delete.
        type (str): The type of the item to delete ("music" or "list").
        list (str): The name of the list from which to delete the item.

        Returns:
        bool: True if the item was deleted successfully, False otherwise.
        """
        if type == "music":
            return self.list[list].pop(name)
        elif type == "list":
            return self.list.pop(list)
        else:
            return False

    # ... other methods ...

    def change(self, name, type, list, new, infor):
        """
        Change the name of a music item in the playlist.

        Parameters:
        name (str): The current name of the music item.
        type (str): The type of the item to change ("music").
        list (str): The name of the list containing the music item.
        new (str): The new name for the music item.
        infor (str): The new information associated with the music item.

        Returns:
        str: The new name of the music item if the change was successful, None otherwise.
        """
        if type == "music":
            self.list[list].pop(name)
            self.list[list][new] = infor
            return self.list.get(list).get(new)
        elif type == "list":
            self.list.pop(list)
            self.list[new] = {}
            return self.list.get(new)
        else:
            return None

    # ... other methods ...

    def in_list(self, name, type, list):
        """
        Check if a music item is in the playlist.

        Parameters:
        name (str): The name of the music item to check.
        type (str): The type of the item to check ("music").
        list (str): The name of the list containing the music item.

        Returns:
        bool: True if the music item is in the playlist, False otherwise.
        """
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

    # ... other methods ...

    def get(self, list, mode="list"):
        """
        Get the list of music items or the entire list from the playlist.

        Parameters:
        list (str): The name of the list to retrieve.
        mode (str): The mode of retrieval ("list" or "music").

        Returns:
        dict: The list of music items or the entire list if the retrieval was successful.
        """
        if mode == "list":
            return self.list.get(list)
        return self.list

    # ... other methods ...

    def get_title(self):
        """
        Get the title of the playlist.

        Returns:
        str: The title of the playlist.
        """
        return self.title

    # ... other methods ...

    def all(self):
        """
        Get all the information of the playlist.

        Returns:
        dict: The entire information of the playlist.
        """
        return self.information

    # ... other methods ...

    def update(self):
        """
        Update the current information with the values of the instance variables.
        """
        self.information.update(title=self.title)
        self.information.update(list_number=self.list_number)
        self.information.update(list=self.list)
        self.information.update(last_play_list=self.last_play_list)
        self.information.update(last_play_index=self.last_play_index)

    def what_you_play_now(self, list, index):
        self.last_play_list = list
        self.last_play_index = index

    def get_what_you_play_now(self):
        return [self.last_play_list,
                self.last_play_index]

    # ... other methods ...

    def save(self, _film_name=" "):
        """
        Save the current playlist to a file.

        Parameters:
        _film_name (str): The name of the file to save the playlist data. If not provided, it defaults to "play_list.save".
        """
        if _film_name != " ":
            pickle_film = open(str("assets\\" + _film_name), "wb")
        else:
            pickle_film = open("assets\\play_list.save", "wb")
        pickle.dump(self.information, pickle_film)
        pickle_film.close()

    # ... other methods ...

    def init_save(self, _film_name=" "):
        """
        Initialize the playlist data with the initial values.

        Parameters:
        _film_name (str): The name of the file to save the playlist data. If not provided, it defaults to "play_list.save".
        """
        if _film_name != " ":
            _information = open(str("assets\\" + _film_name), "wb+")
        else:
            _information = open("assets\\play_list.save", "wb+")
        pickle.dump(
            {"title": "freebird_music_player   (*≧︶≦))(￣▽￣* )ゞ",
             "list_number": 0,
             "list": {},
             "last_play_list": "",
             "last_play_index": -1}, _information)
        _information.close()

    # ... other methods ...

    def load(self, _film_name=" "):
        """
        Load the playlist data from a file.

        Parameters:
        _film_name (str): The name of the file to load the playlist data. If not provided, it defaults to "play_list.save".

        Returns:
        dict: The loaded playlist data.
        """
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
    """
    This function retrieves the full path of a music file from the music list.

    Parameters:
    name (str): The name of the music file to retrieve.
    music_list (list): A list of music file names.
    music_path (str): The path where the music files are located.

    Returns:
    str: The full path of the music file if it exists in the music list, otherwise None.
    """
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
    playlist = PlayList("play_list.save")
    
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