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

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`API Error: ${res.status} - ${errorText}`);
    }

    const data = await res.json();

    // DEBUG
    console.log("FULL BACKEND RESPONSE:", data);

    document.getElementById("status").innerText = "Done ✅";

    // SAFE UI UPDATES (FIXED)

    document.getElementById("reqCount").innerText =
      "📌 Requirements: " + (data.requirements?.length || 0);

    document.getElementById("featureCount").innerText =
      "✨ Features: " + (
        data.features?.length ||
        data.features_extracted?.length ||
        0
      );

    document.getElementById("clusterCount").innerText =
      "🧠 Clusters: " + (data.fpr?.clusters?.length || 0);

    document.getElementById("testCount").innerText =
      "🧪 Test Cases: " + (data.test_cases?.length || 0);

    renderOutput(data);

  } catch (err) {
    console.error("Frontend Error:", err);
    document.getElementById("status").innerText = "Error ❌";
  }
}

// RENDER FUNCTION (UNCHANGED)
function renderOutput(data) {
  const output = document.getElementById("output");
  output.innerHTML = "";

  // Requirements
  output.innerHTML += `<h2>📌 Requirements</h2>`;
  (data.requirements || []).forEach(r => {
    output.innerHTML += `<div class="section">${r}</div>`;
  });

  // Sections
  if (data.sections) {
    output.innerHTML += `<h2>📄 Sections</h2>`;
    Object.entries(data.sections).forEach(([key, value]) => {
      output.innerHTML += `
        <div class="section">
          <b>${key}</b><br/>
          ${value}
        </div>
      `;
    });
  }

  // Clusters
  if (data.fpr?.clusters) {
    output.innerHTML += `<h2>🧠 Clusters</h2>`;
    data.fpr.clusters.forEach(c => {
      output.innerHTML += `<div class="section">${c}</div>`;
    });
  }
}