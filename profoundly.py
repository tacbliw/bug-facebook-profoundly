#!/usr/bin/python
# -*- coding: utf-8 -*-

#################################################################################
#   For this code to work, you must have usernames and ID stored in 'user.txt'  #
#                                                                               #
#   To get the IDs, visite Profoundly through a debugging proxy and capture the #
# json data that contains friends' players names and ID.                        #
#                                                                               #
#   Players' names and IDs are stored in 'user.txt', one per line, with this    #
# format:     <playerID>:<fullName>                                             #
#                                                                               #
#   This code is tested with utf-8 Vietnamese characters, special characters in #
# others languages may cause tons of errors :)                                  #
#                                                                               #
#   Peace~                                                                      # 
#################################################################################

import requests
import json
import codecs

def get_messages(user_id):
    """Take user ID and return user json data"""
    url = "https://web.neargroup.me/ng/GetAllMessages?playerId=" + user_id
    response = requests.get(url)
    return response.json()

id_names = {}

with open("user.txt", 'r', encoding = 'utf-8') as f:
    lines = f.readlines()

    for line in lines:
        data = line.split(':')
        id_names[data[0]] = data[1].strip()

out_file = codecs.open("messages.txt", 'w+', encoding='utf-8')

count = 0
for playerID in id_names.keys():
    count += 1
    
    messages_json = get_messages(playerID)

    to_user = {}
    from_user = {}

    # Output to messages file
    out_file.write("\n[{}] {}\n".format(id_names[playerID], playerID))

    for mess in messages_json:
        text = codecs.unicode_escape_decode(mess["message"])[0].strip()

        if mess["from"] == playerID:  #  Player sending messages
            if mess["to"] in id_names.keys():
                if id_names[mess['to']] in to_user.keys():
                    to_user[id_names[mess['to']]].append(text)

                else:
                    to_user[id_names[mess['to']]] = [text]

            else:
                if mess['to'] in to_user.keys():
                    to_user[mess['to']].append(text)

                else:
                    to_user[mess['to']] = [text]

        elif mess["to"] == playerID:  #  Player receiving messages
            if mess["from"] in id_names.keys():
                if id_names[mess['from']] in from_user.keys():
                    from_user[id_names[mess['from']]].append(text)

                else:
                    from_user[id_names[mess['from']]] = [text]

            else:
                short_name = codecs.unicode_escape_decode(mess['name'].replace('\\\\', '\\'))[0]
                if short_name in from_user.keys():
                    from_user[short_name].append(text)

                else:
                    from_user[short_name] = [text]

    if len(to_user) != 0:
        out_file.write("    [Sends]\n")
        for name in to_user.keys():
            for message in to_user[name]:
                try:
                    out_file.write("        [" + name + "] " + message + '\n')
                except UnicodeEncodeError:
                    out_file.write("         <error>\n")
                    continue


    if len(from_user) != 0:
        out_file.write("\n    [Receives]\n")
        for name in from_user.keys():
            for message in from_user[name]:
                try:
                    out_file.write("        [" + name + "] " + message + '\n')
                except UnicodeEncodeError:
                    out_file.write("          <error>\n")
                    continue

    print("[{}/{}]Done: ".format(count, len(id_names)) + id_names[playerID])

out_file.close()
