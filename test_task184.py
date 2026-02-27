import sys
import os

# Add the path to 'Cloned tasks/Nexatest' so Python can find 'app'
base_path = os.path.join(os.getcwd(), "Cloned tasks", "Nexatest")
sys.path.insert(0, base_path)

# Now the import should work
from app.services.parsing.orchestrator import Orchestrator

# Initialize Orchestrator
orc = Orchestrator()

# Process the test PDF
result = orc.process(
    job_id="demo_root",
    file_path="sample.docx"  # Making sure this file exists
)

print("\n=== RESULT ===")
print(result)