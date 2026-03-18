import song_predictor_1
import pandas
import numpy as np
model = song_predictor_1.get_song_predictor()

running = True

address = "../out/clean_data.csv"
df = pandas.read_csv(address, encoding="MacRoman")
X = df.loc[
    :,
    [
        'release_year', 'duration_ms.x', 'explicit', 
        'mode', 'speechiness', 'acousticness',
        'instrumentalness', 'liveness', 'valence',
        'tempo', 'time_signature'
    ]
] 
while running:
    start_emotion = np.array([0,0,0])
    end_emotion = np.array([1,1,1])
    delta_emotion = end_emotion-start_emotion
    print(f"Searching for song with emotion delta:{delta_emotion}")
    model.predict(X)
