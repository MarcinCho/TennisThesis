import pandas as pd
from sklearn.model_selection import train_test_split


def data_loader(path, normalize_flag=False, std_scaler=False):

    df = pd.read_csv(path)

    df, x_latest, y_latest = validation_set(df)

    non_numeric_columns = df.select_dtypes(["object"]).columns

    df_numeric_only = df.drop(non_numeric_columns, axis=1)

    df = df_numeric_only

    df = df.drop(["match_id"], axis=1)

    if normalize_flag:
        df = (df - df.min()) / (df.max() - df.min())

    df = df.fillna(df.median())

    df = df.fillna(df.median())

    Y = pd.DataFrame(df["y"])
    df = df.drop(["y"], axis=1)
    X = df
    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.1, random_state=45, stratify=Y
    )

    if std_scaler:
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    return x_latest, y_latest, X_train, X_test, y_train, y_test


def normalize(dff):
    result = dff.copy()
    for feature_name in dff.columns:
        max_value = dff[feature_name].max()
        min_value = dff[feature_name].min()
        result[feature_name] = (dff[feature_name] - min_value) / (max_value - min_value)
    return result


def validation_set(df):

    df_latest = df[
        df["date"].str.contains("2024", na=False)
        | df["date"].str.contains("2023", na=False)
    ]
    df.drop(df_latest.index, inplace=True)

    non_numeric_columns = df_latest.select_dtypes(["object"]).columns

    df_numeric_only = df_latest.drop(non_numeric_columns, axis=1)

    df_latest = df_numeric_only

    df_latest = df_latest.drop(["match_id"], axis=1)

    df_latest = df_latest.fillna(df_latest.median())

    y_latest = pd.DataFrame(df_latest["y"])
    x_latest = df_latest.drop(["y"], axis=1)

    return df, x_latest, y_latest
