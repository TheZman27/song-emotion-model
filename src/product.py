import song_predictor_1
import pandas
import numpy as np

model = song_predictor_1.get_song_predictor()
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

def update_predictions(start_emotion):
    X['before: sad to happy'] = np.array([start_emotion[0]]*len(X))
    X['before: calm to energetic'] = np.array([start_emotion[1]]*len(X))
    X['before: relaxed to stressed'] = np.array([start_emotion[2]]*len(X))
    model.predict(X)

def get_closest_songs(delta_emotion, n=3):
    songs = []

    return songs

def emotion_distance(emotion_1, emotion_2):
    assert len(emotion_1) == len(emotion_2)
    return sum([(emotion_1[i]-emotion_2[i])**2 for i in range(len(emotion_1))])

def main():    
    running = True
    while running:
        # input("Starting emotion> ")
        current_emotion_input = input("Current emotion: ")
        start_emotion = np.array([float(current_emotion_input.split()[i]) for i in range(3)])
        goal_emotion_input = input("Goal emotion: ")
        goal_emotion = np.array([float(goal_emotion_input.split()[i]) for i in range(3)])
        delta_emotion = goal_emotion-start_emotion
        print(f"Searching for song with emotion delta:{delta_emotion}")
        predictions = model.predict(X)
        min_dist = 9999
        for i in range(len(predictions)):
            prediction = predictions[i]
            prediction_distance = emotion_distance(delta_emotion, prediction)
            if prediction_distance < min_dist:
                min_dist = prediction_distance
                best_prediction_i = i
        print(df.iloc[best_prediction_i])
        print(df.iloc[best_prediction_i]['song_link'])
if __name__ == "__main__":
    main()