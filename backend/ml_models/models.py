from pymongo import MongoClient
import pandas as pd


#warnings are irritating me so yea removing em
import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

#initialising client variable
client=MongoClient("mongodb+srv://Z33xD:MxVEi2OTvIs4HfjM@el-plan-stem.12pthvy.mongodb.net/?retryWrites=true&w=majority&appName=El-Plan-STEM")
db=client['El-Plan-STEM']

#creating dataframes for the collections so that can be easily accessed via pandas
lap_times_df=pd.DataFrame(list(db['lap_times'].find()))
races_df=pd.DataFrame(list(db['races'].find()))
drivers_df=pd.DataFrame(list(db['drivers'].find()))
pit_stops_df=pd.DataFrame(list(db['pit_stops'].find()))
results_df=pd.DataFrame(list(db['results'].find()))
constructors_df=pd.DataFrame(list(db['constructors'].find()))
driver_standings_df=pd.DataFrame(list(db['driver_standings'].find()))


#removing id columns so it doesnt give any issues later (OCD wali problem)
lap_times_df = lap_times_df.drop(columns=['_id'], errors='ignore')


#importing libraries that i forgot :(
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping


#now we create a 20x20 matrix for each race
#20 drivers and 20 laps cz first 20 laps tell us the most about a race start just like a sprint
selected_races=lap_times_df['raceId'].unique()[:500] #prevents ram from going boom
sample=[]
label=[]
for race_id in selected_races:
    race_data = lap_times_df[lap_times_df['raceId'] == race_id]
    pivot = race_data.pivot(index='lap', columns='driverId', values='milliseconds')
    pivot = pivot.iloc[:20, :20]  # First 20 laps

    #20 drivers should be there, im leaving 22 drivers scenario cz they wont give much changes
    if pivot.shape[1] == 20:
        matrix = pivot.fillna(pivot.mean()).values  #missing values replaced with mean
        if matrix.shape == (20, 20):
            matrix = (matrix - matrix.mean()) / matrix.std()
            sample.append(matrix)

            # Label: High-momentum race if lap-to-lap variance is high
            lap_diff = np.diff(matrix, axis=0)
            momentum_variance = np.std(lap_diff)
            label.append(1 if momentum_variance > 0.5 else 0)

# Convert to arrays
X = np.array(sample)
y = np.array(label)

#reshaping cnn for 20x20
X = X.reshape(-1, 20, 20, 1)

# favorite part, train test split
print(f"Label distribution: {np.bincount(y)}")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# making cnn model
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(20, 20, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')  
])
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

#training the model
model.fit(X_train, y_train, epochs=30, batch_size=16, validation_data=(X_test, y_test), class_weight={0: 28.4, 1: 1.0})
#evaluating the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"🅱️asterplan Model trained. Test Accuracy: {accuracy:.4f}")