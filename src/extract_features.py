import os

INPUT_REQ_PATH = "data/output/functional_requirements.txt"
OUTPUT_FEATURE_PATH = "data/output/feature_mapping.txt"

FEATURE_KEYWORDS = {
    "Authentication": ["login", "authenticate", "password", "credentials"],
    "Authorization": ["role", "access control", "rbac"],
    "Security": ["encrypt", "secure", "authorization"],
    "User Management": ["user", "student", "lecturer", "administrator"],
    "Course Management": ["course", "enrol"],
    "Grading": ["grade", "grading", "gpa"],
    "Reporting": ["report", "pdf"],
    "Notification": ["email", "notify"],
    "Audit & Logging": ["log", "audit"]
}


def load_requirements(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def extract_features(requirements):
    results = []

    for req in requirements:
        matched_features = []

        for feature, keywords in FEATURE_KEYWORDS.items():
            if any(k.lower() in req.lower() for k in keywords):
                matched_features.append(feature)

        results.append({
            "requirement": req,
            "features": matched_features
        })

    return results


def save_feature_mapping(results, path):
    with open(path, "w", encoding="utf-8") as f:
        for item in results:
            f.write(f"Requirement: {item['requirement']}\n")
            f.write(f"Features: {', '.join(item['features'])}\n\n")


if __name__ == "__main__":
    print("Loading functional requirements...")
    requirements = load_requirements(INPUT_REQ_PATH)

    print("Extracting software features...")
    feature_mapping = extract_features(requirements)

    for item in feature_mapping:
        print(item)

    save_feature_mapping(feature_mapping, OUTPUT_FEATURE_PATH)
    print("\n[SAVED] Feature mapping saved to:", OUTPUT_FEATURE_PATH)

#This code is the same code I am using from SRS segmentation task in sprint 1