import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load and featurize
df = pd.read_csv('../honeypot.log', sep=' - ', names=['timestamp','message'], engine='python')
df['hour']   = pd.to_datetime(df['timestamp']).dt.hour
df['length'] = df['message'].str.len()
X = df[['hour','length']]

# Train
clf = IsolationForest(contamination=0.05, random_state=42)
clf.fit(X)
joblib.dump(clf, 'anomaly_detector.pkl')
print("✅ Model trained and saved to anomaly_detector.pkl")
