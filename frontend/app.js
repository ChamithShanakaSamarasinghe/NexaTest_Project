const API_URL = "https://nexa-test-project.vercel.app/api/full-analysis";

async function processFiles() {

  document.getElementById("status").innerText = "Processing... 🔄";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        doc_id: 1
      })
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`API Error: ${res.status} - ${errorText}`);
    }

    const data = await res.json();

    console.log("API RESPONSE:", data);

    document.getElementById("status").innerText = "Done ✅";

    // SAFE UI UPDATES
    document.getElementById("reqCount").innerText =
      "📌 Requirements: " + (data.requirements?.length || 0);

    document.getElementById("featureCount").innerText =
      "✨ Features: " + (data.features?.length || 0);

    document.getElementById("clusterCount").innerText =
      "🧠 Clusters: " + (data.fpr?.clusters?.length || 0);

    document.getElementById("testCount").innerText =
      "🧪 Test Cases: " + (data.fpr?.test_cases?.length || 0);

    renderOutput(data);

  } catch (err) {
    console.error("Frontend Error:", err);
    document.getElementById("status").innerText = "Error ❌";
  }
}