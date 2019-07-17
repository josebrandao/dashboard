import urllib
import shutil
import os
import json
import datetime

############################################
###          Configurations for API Request          ###
############################################
URL = "https://dax-rest.comscore.com/v1/reportitems.json"
PARAMS = {
        "site": "int",
        "client": "comscore",
        "user": "onecallapiuser1",
        "password": "onecallapiuser1"
}

def fetch_data(itemid, startdate, temp_str=""):
    """
    Makes request to API and writes to the data folder the results
    overwriting the existing file
    """
    PARAMS["itemid"] = str(itemid)
    PARAMS["startdate"] = startdate
    try:
        fname, msg = urllib.urlretrieve(URL + "?" + urllib.urlencode(PARAMS))
    finally:
        newf = os.path.dirname(os.path.realpath(__file__))
        newf += "/data/" + PARAMS["itemid"] + temp_str +".json"
        shutil.copyfile(fname, newf)
        urllib.urlcleanup()

def get_yesterday():
    today = datetime.datetime.today().replace(
                    hour=0, minute=0, second=0, microsecond=0)
    day = datetime.timedelta(days=1)
    yesterday = today - day
    return yesterday

def check_existing_data(itemid):
    """
    Reads existing json file, if the last date in the json file does not match
    yesterday's date then a request is made to the API for only yesterday's
    data.  The json file is then appended with the new days data and the
    oldest day in the dataset is deleted.
    """

    itemid = str(itemid)
    json_data = open('data/' + itemid + ".json", "r")
    data = json.load(json_data)
    json_data.close()
    count = int(data["reportitems"]["reportitem"][0]["rows"]["@count"])
    last_row = data["reportitems"]["reportitem"][0]["rows"]["r"][count-1]["c"]
    last_row_date = datetime.datetime.strptime(last_row[0], "%b-%d-%Y")
    yesterday = get_yesterday()
    if yesterday != last_row_date:
        data["reportitems"]["reportitem"][0]["rows"]["r"].pop(0)
        fetch_data(itemid, "yesterday", "-temp")
        single_json = open('data/' + itemid + "-temp.json")
        single_data = json.load(single_json)
        single_json.close()
        os.remove("data/" + itemid + "-temp.json")
        single_data_row  = single_data["reportitems"]["reportitem"][0]["rows"]["r"][0]
        data["reportitems"]["reportitem"][0]["rows"]["r"].append(single_data_row)
        json_data = open("data/" + itemid + ".json", "w+")
        json_data.write(json.dumps(data))
        json_data.close()

def update_line(filename, line_no, new_line):
    """
    Overwrites the file with exactly the same text with only a single line,
    determined by line number (0 indexed), replaced
    """
    with open(filename, "r") as f:
        newlines = []
        for i, line in enumerate(f):
            if i != line_no:
                newlines.append(line)
            else:
                newlines.append(new_line)
    with open(filename, "w") as f:
        for line in newlines:
            f.write(line)

y_var_string = 'var yesterday = "' + get_yesterday().strftime("%m/%d/%Y") + '"\n'
update_line("index.html", 13, y_var_string)
check_existing_data("46")
fetch_data("25", "yesterday")
fetch_data("52", "yesterday")
fetch_data("113", "yesterday")
fetch_data("609", "yesterday")
fetch_data("63", "yesterday")
