const API_URL = "https://nexa-test-project.vercel.app/full-analysis";

async function processFiles() {

  document.getElementById("status").innerText = "Processing... 🔄";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        doc_id: 1   // ⚠️ change this to a valid doc_id in your DB
      })
    });

    if (!res.ok) {
      throw new Error("API Error: " + res.status);
    }

    const data = await res.json();

    document.getElementById("status").innerText = "Done ✅";

    document.getElementById("reqCount").innerText =
      "📌 Requirements: " + (data.requirements?.length || 0);

    document.getElementById("featureCount").innerText =
      "✨ Features: " + (data.features?.length || 0);

    document.getElementById("clusterCount").innerText =
      "🧠 Clusters: " + (data.fpr?.clusters?.length || 0);

    document.getElementById("testCount").innerText =
      "🧪 Test Cases: 0";

    renderOutput(data);

  } catch (err) {
    console.error(err);
    document.getElementById("status").innerText = "Error ❌";
  }
}