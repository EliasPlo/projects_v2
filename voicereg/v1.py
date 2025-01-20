import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

def extract_features(file_path, n_mfcc=13):
    try:
        y, sr = librosa.load(file_path, mono=True, duration=30)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        mfccs_mean = np.mean(mfccs, axis=1)
        return mfccs_mean
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def prepare_data(dataset_path):
    features = []
    labels = []

    for genre_dir in os.listdir(dataset_path):
        genre_path = os.path.join(dataset_path, genre_dir)
        if not os.path.isdir(genre_path):
            continue

        for file in os.listdir(genre_path):
            file_path = os.path.join(genre_path, file)
            mfccs = extract_features(file_path)
            if mfccs is not None:
                features.append(mfccs)
                labels.append(genre_dir)

    return np.array(features), np.array(labels)

def main():
    dataset_path = "path/to/your/dataset"  # Replace with your dataset path

    print("Extracting features...")
    X, y = prepare_data(dataset_path)

    print("Encoding labels...")
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    print("Normalizing features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

    print("Training KNN model...")
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)

    print("Evaluating model...")
    accuracy = knn.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

    print("Testing with a single file...")
    test_file = "path/to/test/file.wav"  # Replace with your test file path
    test_features = extract_features(test_file)
    if test_features is not None:
        test_features_scaled = scaler.transform([test_features])
        prediction = knn.predict(test_features_scaled)
        predicted_genre = label_encoder.inverse_transform(prediction)
        print(f"Predicted genre: {predicted_genre[0]}")

if __name__ == "__main__":
    main()
