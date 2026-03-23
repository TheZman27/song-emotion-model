import song_predictor_1
import pandas
import numpy as np

"""
Utility functions for song recommender app. If run as main, acts as a command line app.
Usage: python ./src/product.py
TODO:
Take user emotion into account for a better prediction.

"""

model = song_predictor_1.get_song_predictor()
address = "./out/clean_data.csv"
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

predictions = model.predict(X)

def get_closest_song(delta_emotion):
    min_dist = None
    for i in range(len(predictions)):
            prediction_distance = emotion_distance(delta_emotion, predictions[i])
            if (not min_dist) or (prediction_distance < min_dist):
                min_dist = prediction_distance
                best_prediction_i = i
    return df.iloc[best_prediction_i]

def emotion_distance(emotion_1, emotion_2):
    assert len(emotion_1) == len(emotion_2)
    return sum([(emotion_1[i]-emotion_2[i])**2 for i in range(len(emotion_1))])

def main():    
    running = True
    while running:
        current_emotion_input = input("Current emotion: ")
        start_emotion = np.array([float(current_emotion_input.split()[i]) for i in range(3)])
        goal_emotion_input = input("Goal emotion: ")
        goal_emotion = np.array([float(goal_emotion_input.split()[i]) for i in range(3)])
        delta_emotion = goal_emotion-start_emotion
        print(get_closest_song(delta_emotion)['song_link'])
if __name__ == "__main__":
    main()