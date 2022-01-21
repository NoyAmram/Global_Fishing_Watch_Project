import pickle
import pandas as pd
from datetime import datetime

MODEL_FILE = "fixtures/rfc.p"

with open(MODEL_FILE, "rb") as f:
    RFC = pickle.load(f)


def predict(data):
    return RFC.predict(data)

def refresh():
    global RFC
    RFC = pickle.load(MODEL_FILE)

def get_forecast (timestamp, distance_from_shore, distance_from_port, speed, course, lat, lon):
    timestamp = datetime.timestamp(datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M"))
    x = pd.DataFrame([[timestamp, distance_from_shore, distance_from_port, speed, course, lat, lon]])
    return predict(x)


if __name__ == '__main__':
    result = get_forecast()
    print(result)

