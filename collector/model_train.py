import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x))

DATA_FILE = "fixtures/full_raw_data.csv"
MODEL_FILE = "fixtures/rfc.p"


def prep(file_name):
    """Receives concatenate csv file contain the data and perform required preprocessing.
     Returns df separated to X and y."""
    df = pd.read_csv(file_name, encoding="utf-8")
    df.drop(df[df['is_fishing'] == -1].index, inplace=True)
    df = df.dropna()
    df.loc[(df["is_fishing"] > 0), "is_fishing"] = 1
    df.drop(['source'], inplace=True, axis=1)
    df.drop(['mmsi'], inplace=True, axis=1)
    return df.drop("is_fishing", axis=1), df["is_fishing"]


def train(x, y):
    """Receives train data and create model object.
        :returns model fitted on train data"""
    rfc = RandomForestClassifier(n_estimators=100, min_samples_leaf=2)
    rfc.fit(x, y)
    return rfc


def save_model(rfc, output_file):
    """Receives fitted model and save it to a pickle file"""
    with open(output_file, "wb") as f:
        pickle.dump(rfc, f)


def main():
    """Starting function to call above functions of the program."""
    X_train, y_train = prep(DATA_FILE)
    RFC = train(X_train, y_train)
    save_model(RFC, MODEL_FILE)


if __name__ == '__main__':
    main()
