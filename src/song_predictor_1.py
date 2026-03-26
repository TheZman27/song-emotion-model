import pandas
# from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.multioutput import MultiOutputRegressor


def get_song_predictor(file_address='./out/merged_data.csv') -> MultiOutputRegressor:
    """Returns a trained sklearn.MultiOutputRegressor model on our survey data. 
    The model inputs are:
        release_year, duration_ms.x, explicit, 
        mode, speechiness, acousticness,
        instrumentalness, liveness, valence,
        tempo, time_signature
    The model outputs are
        'delta: sad to happy',
        'delta: calm to energetic',
        'delta: relaxed to stressed'
    """
    df = pandas.read_csv(file_address)
    X = df.loc[
        :,
        [
            'release_year', 'duration_ms.x', 'explicit', 
            'mode', 'speechiness', 'acousticness',
            'instrumentalness', 'liveness', 'valence',
            'tempo', 'time_signature'
        ]
    ] 
    Y = df.loc[
        :,
        [
            'delta: sad to happy',
            'delta: calm to energetic',
            'delta: relaxed to stressed'
        ]
    ] 

    # X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)


    base_estimator = linear_model.LinearRegression()
    model = MultiOutputRegressor(base_estimator)
    model.fit(X, Y)

    print(f"Training score (R^2) {model.score(X, Y)}")

    return model