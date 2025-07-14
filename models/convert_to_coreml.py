import coremltools as ct
import joblib

sk_model = joblib.load('anomaly_detector.pkl')
coreml_model = ct.converters.sklearn.convert(
    sk_model,
    input_features=['hour','length'],
    output_feature_names=['anomaly_score']
)
coreml_model.save('anomaly_detector.mlmodel')
print("✅ Core ML model saved to anomaly_detector.mlmodel")
