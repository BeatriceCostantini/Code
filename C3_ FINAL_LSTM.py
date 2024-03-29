
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from keras.optimizers import Adam

# Carica il dataset CSV
file_path = '/Users/b.costantini/Desktop/DATABASE_HEELCONTACT_CA_final.csv'
data = pd.read_csv(file_path)

# Prendi le features e il target
features = ['R_RF', 'R_VL', 'R_VM', 'R_G', 'R_BFCL', 'R_TA', 'R_PL', 'R_SO', 'R_GL', 'R_GMA']
target = 'Patology'

X = data[features].values  # Features
y = data[target].values  # Target

# Codifica il target in valori numerici
label_encoder = LabelEncoder()
encoded_targets = label_encoder.fit_transform(y)

# Dividi il dataset in training set e test set
X_train, X_test, y_train, y_test = train_test_split(X, encoded_targets, test_size=0.2, random_state=42)

# Definisci la funzione per creare il modello LSTM
def create_model():
    model = Sequential()
    model.add(LSTM(units=50, input_shape=(X_train.shape[1], 1)))  # Consideriamo 1 come numero di time steps
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    
    opt = Adam(learning_rate=0.031)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
    return model

# Crea il modello LSTM
model = create_model()

# Addestra il modello
model.fit(X_train.reshape((X_train.shape[0], X_train.shape[1], 1)), y_train, epochs=30, batch_size=32, verbose=0)

# Valuta il modello sul test set
y_pred_prob = model.predict(X_test.reshape((X_test.shape[0], X_test.shape[1], 1)))
y_pred = (y_pred_prob > 0.5).astype(int)

# Calcola le metriche di performance
target_names = label_encoder.classes_
print("Metriche di performance generali:")
print(classification_report(y_test, y_pred, target_names=target_names))

# Calcola le metriche di performance per le due classi (macro e micro)
for class_idx in range(len(target_names)):
    target_class = label_encoder.inverse_transform([class_idx])[0]
    class_indices = np.where(y_test == class_idx)[0]
    y_test_class = np.zeros_like(y_test)
    y_test_class[class_indices] = 1
    
    y_pred_class = np.zeros_like(y_pred)
    y_pred_class[np.where(y_pred == class_idx)[0]] = 1
    
    print(f"Metriche di performance per la classe '{target_class}':")
    print(classification_report(y_test_class, y_pred_class, target_names=[f'not {target_class}', target_class]))
