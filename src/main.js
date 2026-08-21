const analyzeButton = document.querySelector("#analyzeButton");
const websiteUrl = document.querySelector("#websiteUrl");
const statusMessage = document.querySelector("#status");

// ANALYZE WEBSITE

analyzeButton.addEventListener("click", async () => {
  const url = websiteUrl.value.trim();

  if (!url) {
    statusMessage.textContent = "Please enter a website URL.";
    return;
  }

  statusMessage.textContent = "Analyzing website...";
  analyzeButton.disabled = true;

  try {
    const response = await fetch("http://127.0.0.1:8000/api/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to analyze website.");
    }

    const result = await response.json();

    // ORIGINAL SCREENSHOT

    websitePreview.innerHTML = "";

    const screenshot = document.createElement("img");

    screenshot.src = "http://127.0.0.1:8000/api/screenshot";

    screenshot.alt = "Website screenshot";

    websitePreview.appendChild(screenshot);

    // METRICS

    document.querySelector("#uxScore").textContent =
      result.metrics.overall_ux_score;

    document.querySelector("#hierarchyScore").textContent =
      result.metrics.visual_hierarchy;

    document.querySelector("#ctaVisibility").textContent =
      result.metrics.cta_visibility;

    document.querySelector("#ctaScore").textContent =
      result.ui_metrics.cta_prominence;

    document.querySelector("#headlineScore").textContent =
      result.ui_metrics.headline_prominence;

    document.querySelector("#clutterScore").textContent =
      result.ui_metrics.visual_clutter;

    document.querySelector("#textScore").textContent =
      result.ui_metrics.text_density;

    // RECOMMENDATIONS

    const recommendationBox = document.querySelector("#recommendations");

    recommendationBox.innerHTML = "";

    result.recommendations.forEach((recommendation) => {
      const p = document.createElement("p");

      p.textContent = recommendation;

      recommendationBox.appendChild(p);
    });

    const findingsBox = document.querySelector("#findings");

    findingsBox.innerHTML = "";

    result.findings.forEach((finding) => {
      const p = document.createElement("p");

      p.textContent = finding;

      findingsBox.appendChild(p);
    });

    // STORE OVERLAY URL

    window.latestOverlay = "http://127.0.0.1:8000" + result.overlay;

    statusMessage.textContent = "Website analyzed successfully.";
  } catch (error) {
    console.error(error);
    statusMessage.textContent = `Error: ${error.message}`;

    websitePreview.innerHTML =
      "<p> Unable to capture the website screenshot. </p>";
  } finally {
    analyzeButton.disabled = false;
  }
});

// NEW ANALYSIS

const newAnalysis = document.querySelector("#newAnalysis");

newAnalysis.addEventListener("click", () => {
  websiteUrl.value = "";
  statusMessage.textContent = "";

  document.querySelector("#websitePreview").innerHTML =
    "<p>Website screenshot will appear here.</p>";

  document.querySelector("#attentionPreview").innerHTML =
    "<p>Attention analysis will appear here.</p>";

  document.querySelector("#ctaScore").textContent = "-";
  document.querySelector("#headlineScore").textContent = "-";
  document.querySelector("#clutterScore").textContent = "-";
  document.querySelector("#textScore").textContent = "-";

  // RESET UX METRICS

  document.querySelector("#uxScore").textContent = "-";
  document.querySelector("#hierarchyScore").textContent = "-";
  document.querySelector("#ctaVisibility").textContent = "-";
  document.querySelector("#aboveFold").textContent = "-";

  // RESET FINDINGS

  document.querySelector("#findings").innerHTML =
    '<p class="empty">Analysis findings will appear here.</p>';

  // RESET RECOMMENDATIONS

  document.querySelector("#recommendations").innerHTML =
    '<p class="empty">Recommendations will appear here.</p>';
});

// VISUAL ATTENTION TABS

const tabs = document.querySelectorAll(".tab");
const attentionPreview = document.querySelector("#attentionPreview");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");

    const view = tab.dataset.view;

    if (view === "original") {
      attentionPreview.innerHTML = "";

      const image = document.createElement("img");

      image.src = "http://127.0.0.1:8000/api/screenshot";

      attentionPreview.appendChild(image);
    } else if (view === "overlay") {
      attentionPreview.innerHTML = "";

      const image = document.createElement("img");

      image.src = window.latestOverlay;

      attentionPreview.appendChild(image);
    }
  });
});
