const API_URL = "/api/full-analysis";

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

    const data = await res.json();

    console.log("BACKEND RESPONSE:", data);

    if (!res.ok) {
      throw new Error(JSON.stringify(data));
    }

    document.getElementById("status").innerText = "Done ✅";

    document.getElementById("reqCount").innerText =
      "📌 Requirements: " + (data.requirements?.length || 0);

    document.getElementById("featureCount").innerText =
      "✨ Features: " + (data.features?.length || 0);

    document.getElementById("clusterCount").innerText =
      "🧠 Clusters: " + (data.fpr?.clusters?.length || 0);

    document.getElementById("testCount").innerText =
      "🧪 Test Cases: " + (data.test_cases?.length || 0);

    renderOutput(data);

  } catch (err) {
    console.error("ERROR:", err);
    document.getElementById("status").innerText = "Error ❌ (Check Console)";
  }
}