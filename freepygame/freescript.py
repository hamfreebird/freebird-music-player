marking_list = {
    "symbol" : {
        'all' : ['+', '-', '*', '/', '{', '}', '[', ']', '$', '#', '@', '!', '?', '^', '<', '>', '='],
        '+' : 100,
        '-' : 101,
        '*' : 102,
        '/' : 103,
        '{' : 104,
        '}' : 105,
        '[' : 106,
        ']' : 107,
        '$' : 108,
        '#' : 109,
        '@' : 110,
        '!' : 111,
        '?' : 112,
        '^' : 113,
        '<' : 114,
        '>' : 115,
        '=' : 116
    },
    "type" : {
        'all' : ['int', 'float', 'string', 'boolean', 'variable', 'commentate'],
        'int' : 200,
        'float' : 201,
        'string' : 202,
        'boolean' : 203,
        'variable' : 204,
        'commentate' : 205
    }
}

class Script():
    # 自由飞鸟脚本解释器
    
    def __init__(self, script : str):
        self.script = script
        self.script = self.marking()
        
    def marking(self):
        mark_list = self.script.split(';')
        return mark_list
