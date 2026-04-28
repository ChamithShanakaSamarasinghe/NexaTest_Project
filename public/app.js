const API_URL = "/api/full-analysis";

async function processFiles() {
  const statusEl = document.getElementById("status");

  statusEl.innerText = "Processing... 🔄";

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

    // 🔥 BETTER ERROR HANDLING
    if (!res.ok) {
      const errorText = await res.text();
      console.error("Backend Error Response:", errorText);
      throw new Error(`API Error ${res.status}: ${errorText}`);
    }

    const data = await res.json();

    console.log("✅ FULL BACKEND RESPONSE:", data);

    statusEl.innerText = "Done ✅";


    // SAFE DATA EXTRACTION

    const requirements = data.requirements || [];
    const features = data.features || data.features_extracted || [];
    const clusters = data.fpr?.clusters || [];
    const testCases = data.test_cases || [];

 
    // UI COUNTERS

    document.getElementById("reqCount").innerText =
      "📌 Requirements: " + requirements.length;

    document.getElementById("featureCount").innerText =
      "✨ Features: " + features.length;

    document.getElementById("clusterCount").innerText =
      "🧠 Clusters: " + clusters.length;

    document.getElementById("testCount").innerText =
      "🧪 Test Cases: " + testCases.length;

   
    // RENDER OUTPUT
    renderOutput(data);

  } catch (err) {
    console.error("❌ Frontend Error:", err);

    document.getElementById("status").innerText =
      "Error ❌ (Check Console)";
  }
}

// RENDER FUNCTION 
function renderOutput(data) {
  const output = document.getElementById("output");
  output.innerHTML = "";

  // 📌 Requirements
  output.innerHTML += `<h2>📌 Requirements</h2>`;
  (data.requirements || []).forEach(r => {
    output.innerHTML += `<div class="section">${r}</div>`;
  });

  // 📄 Sections
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

  // 🧠 Clusters
  const clusters = data.fpr?.clusters || [];
  if (clusters.length > 0) {
    output.innerHTML += `<h2>🧠 Clusters</h2>`;
    clusters.forEach(c => {
      output.innerHTML += `<div class="section">${c}</div>`;
    });
  }

  // 🧪 Test Cases
  const testCases = data.test_cases || [];
  if (testCases.length > 0) {
    output.innerHTML += `<h2>🧪 Test Cases</h2>`;
    testCases.forEach(tc => {
      output.innerHTML += `
        <div class="section">
          <b>${tc.id}</b><br/>
          ${tc.requirement}
        </div>
      `;
    });
  }
}