import json
import sys
import math

def load_raw(): 
    with open("data.json") as fi:
        raw_data = json.load(fi)
    
    return raw_data

def store_raw(data):
    with open('data.json', 'w') as fo:
        json.dump(data, fo)

def update_ratings(data, keval, kfact, match):
    tmp_users = data["players"]

    avg_law_opponent = 0
    avg_out_opponent = 0
    avg_ren_opponent = 0

    for user in tmp_users:
        #get average score for law opponents
        if user["name"] in match["law"]:
            avg_out_opponent += int(user["rating"])
            avg_ren_opponent += int(user["rating"])
            user["side"] = "law"

        #get average score for out opponents
        if user["name"] in match["out"]:
            avg_law_opponent += int(user["rating"])
            avg_ren_opponent += int(user["rating"])
            user["side"] = "out"

        #get average score for ren opponents
        if user["name"] in match["ren"]:
            avg_law_opponent += int(user["rating"])
            avg_out_opponent += int(user["rating"])
            user["side"] = "ren"

    avg_law_opponent = round(avg_law_opponent/len(match["out"] + match["ren"]),2)    
    avg_out_opponent = round(avg_out_opponent/len(match["law"] + match["ren"]),2)    
    avg_ren_opponent = round(avg_ren_opponent/len(match["law"] + match["out"]),2)

    #now we have the average opponent for each player
    #we can elaborate the estimated result

    for user in tmp_users:
        #calulate the estimated outcome of the match
        if "side" in user:
            if user["side"] == "law":
                user["expected"] = 1/(1+math.pow(10,((avg_law_opponent-float(user["rating"]))/400)))
            if user["side"] == "out":
                user["expected"] = 1/(1+math.pow(10,((avg_out_opponent-float(user["rating"]))/400)))
            if user["side"] == "ren":
                user["expected"] = 1/(1+math.pow(10,((avg_ren_opponent-float(user["rating"]))/400)))

            #calculate the real outcome value
            user["actual"] = (keval[match["win"]][user["side"]] - (7*(user["name"] not in match["alive"])))/100
            #get the newer rating, updated accordingly
            user["rating"] = int(int(user["rating"]) + round(kfact * (user["actual"] - user["expected"]),0))

    for adjust in data["players"]:
        for correct in tmp_users:
            if adjust["name"] == correct["name"] and "side" in correct:
                adjust["rating"] = correct["rating"]
                adjust["matches"] += 1 

    return data