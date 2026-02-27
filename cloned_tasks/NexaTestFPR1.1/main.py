from src.pipeline import run_pipeline

metrics, keywords = run_pipeline(feature_type="OHE")

print("Metrics:", metrics)
print("Keywords:", keywords)