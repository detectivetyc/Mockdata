from table import Table
import sys
from random import choice
from read_sql import ReadSQL
import random, string

def context_dict_process(context_dict, context, user, table, session_id, sigid):
    key_ret = context_dict[context]
    key_ret = key_ret[1:len(key_ret) - 1]
    if key_ret == 'user_agent' :
        val_ret = table.devices[user.device_id]['ua']
    elif key_ret == 'login_name' or key_ret == 'user_name@b64':
        val_ret = choice(table.users[user.user_id]['alias'])
    elif key_ret == 'method' :
        val_ret = choice(['GET', 'POST'])
    elif key_ret == 'rsp_latency' :
        val_ret = str(random.randint(1, 100))
    elif key_ret == 'file_name' :
        if table.users[user.user_id]['event'][user.event]['filename'] == "":
            val_ret = generate_random_name(8)
        else:
            val_ret = table.users[user.user_id]['event'][user.event]['filename']
    elif key_ret == 'file_hash' :
        val_ret = generate_random_hash()
    elif key_ret == 'file_size' :
        val_ret = random.randint(1000, 99999)
    elif key_ret == 'session_id' :
        val_ret = session_id
    elif key_ret == 'status_code' :
        val_ret = table.get_item(user.event, user.appname, 'rsp_code')
        if val_ret is None:
            sys.exit("rsp_code is None")
    elif key_ret == 'user_id':
        val_ret = random.randint(1,1000)
    elif key_ret == 'user_token' :
        #user_token
        val_ret = 'ABCDEFGHIJKLMNOPQ'
    else :
        val_ret = table.get_item(user.event, user.appname, key_ret)
        if val_ret is None:
            sys.exit("There is no info about context %s" % key_ret)
    ret = {}
    ret[key_ret] = val_ret
    return ret

def handle_context(context_dict, user, table, session_id, sigid):
    part_dict = {}
    for key in context_dict:
        temp_dict = context_dict_process(context_dict, key, user, table, session_id, sigid)
        part_dict[temp_dict.keys()[0]] = temp_dict.values()[0]
    if len(part_dict) < 1:
        sys.exit("some thing wrong with context")
        #special case for 0x4050000 and 0x4060000
    if sigid == "'0x4050000'" or sigid == "'0x4060000'":
        hash = generate_random_hash()
        part_dict['file_hash'] = hash
    return part_dict

def generate_body_part(element_list, sigid, user, table, session_id):
    context_dict = ReadSQL.get_element_by_sigid(sigid, table.element_sql.list)
    if user.event == 'download' or user.event == 'upload':
        if user.appname == 'Dropbox':
            context_dict['http_req_method'] = 'method'
            context_dict['http_req_host'] = 'host'
            context_dict['http_req_url'] = 'url'
    part_dict = handle_context(context_dict, user, table, session_id, sigid)
    return part_dict

def generate_random_name(size = 8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def generate_random_hash(size = 32):
    return ''.join(random.choice(string.ascii_lowercase[0:6] + string.digits) for _ in range(size))

