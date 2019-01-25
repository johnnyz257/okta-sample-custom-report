import os
import datetime
import csv
import io

from flask import Flask, request, send_from_directory, Response
from flask_sslify import SSLify
from utils.rest import OktaUtil

"""
GLOBAL VARIABLES ########################################################################################################
"""
app = Flask(__name__)
app.debug = False
app.config.update({
    "SECRET_KEY": "6w_#w*~AVts3!*yd&C]jP0(x_1ssd]MVgzfAw8%fF+c@|ih0s1H&yZQC&-u~O[--"  # For the session
})
sslify = SSLify(app, permanent=True, subdomains=True)


"""
UTILS ###################################################################################################################
"""


def json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def safe_cast(val, to_type, default=None):
    print("safe_cast()")
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


"""
ROUTES ##################################################################################################################
"""


@app.route('/<path:filename>')
def serve_static_html(filename):
    """ serve_static_html() generic route function to serve files in the 'static' folder """
    root_dir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)


@app.route('/')
def index():
    """ handler for the root url path of the app """
    print("index()")

    okta_util = OktaUtil(request.headers)
    o365_groups = okta_util.get_o365_groups()
    report = {"data": []}

    print("Total Groups: {0}".format(len(o365_groups)))

    for group in o365_groups:
        group_id = group["id"]
        users = okta_util.get_users_by_group_id(group_id)
        print("Total Users for Group: {0}:{1}".format(group["profile"]["name"], len(users)))

        for user in users:
            record = {}

            record["GroupName"] = group["profile"]["name"]
            record["FirstName"] = user["profile"]["firstName"]
            record["LastName"] = user["profile"]["lastName"]

            report["data"].append(record)

    # prep csv conversion for output
    csv_data_io = io.StringIO()
    csv_columns = [
        "GroupName",
        "FirstName",
        "LastName"
    ]
    cw = csv.DictWriter(csv_data_io, fieldnames=csv_columns, dialect='excel')
    cw.writeheader()
    for item in report["data"]:
        cw.writerow(item)

    response = Response(
        csv_data_io.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=export.csv"})

    return response


"""
MAIN ##################################################################################################################
"""
if __name__ == "__main__":
    # This is to run on c9.io.. you may need to change or make your own runner
    # print( "config.app: {0}".format(json.dumps(config.app, indent=4, sort_keys=True, default=json_converter)) )
    app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)))
