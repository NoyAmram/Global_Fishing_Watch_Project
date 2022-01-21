import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x))

def prep(file_name):
    df = pd.read_csv(file_name, encoding="utf-8")
    df.drop(df[df['is_fishing']==-1].index, inplace=True)
    df = df.dropna()
    df.loc[(df["is_fishing"] > 0), "is_fishing"] = 1
    df.drop(['source'], inplace=True, axis =1)
    df.drop(['mmsi'], inplace=True, axis=1)
    return df.drop("is_fishing", axis=1), df["is_fishing"]

def train(x_train, y_train):
    rfc = RandomForestClassifier(n_estimators=100, min_samples_leaf=2)
    rfc.fit(x_train, y_train)
    return rfc

def save_model(rfc, output_file):
    with open(output_file, "wb") as f:
        pickle.dump(rfc, f)


if __name__ == '__main__':
    x_train, y_train = prep("fixtures/full_raw_data.csv")
    RFC = train(x_train, y_train)
    save_model(RFC, "fixtures/rfc.p")