import pickle
import pandas as pd
from datetime import datetime

MODEL_FILE = "fixtures/rfc.p"

with open(MODEL_FILE, "rb") as f:
    RFC = pickle.load(f)


def predict(data):
    """:param data to predict by fitted classification model that was read from pickle file
           :returns model prediction"""
    return RFC.predict(data)


def refresh():
    """Upload new model file every time it is updated and trained on new data"""
    global RFC
    RFC = pickle.load(MODEL_FILE)


def get_forecast(timestamp, distance_from_shore, distance_from_port, speed, course, lat, lon):
    """receives inputs for a single prediction as parameters
       returns a single prediction as a string."""
    timestamp = datetime.timestamp(datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M"))
    x = pd.DataFrame([[timestamp, distance_from_shore, distance_from_port, speed, course, lat, lon]])
    return predict(x)


def main():
    """ starting function to call above functions and print prediction results"""
    result = get_forecast()
    print(result)


if __name__ == '__main__':
    main()


