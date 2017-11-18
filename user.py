import random

class User():
    def __init__(self, table, event=None):
        self.user_id = random.choice(table.user_list)
        #self.user_id = 'User_1'
        self.device_id = table.randomly_get_device_id(self.user_id)
        self.event = event
        if event is None:
            self.appname = table.randomly_get_app_name(self.user_id)
        else:
            self.appname = table.randomly_get_file_item(self.user_id, event, 'apps')
        name = table.randomly_get_file_item(self.user_id, event, 'pattern_name')
        if name == 'all':
            self.pattern_name = random.choice(table.name_list)
        else:
            self.pattern_name = name
        if event is not None:
            self.subfile = table.users[self.user_id]['event'][event]['subfile']
        else:
            self.subfile = None
