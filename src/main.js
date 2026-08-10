const analyzeButton = document.querySelector("#analyzeButton");
const websiteUrl = document.querySelector("#websiteUrl");
const status = document.querySelector("#status");

// ANALYZE WEBSITE

analyzeButton.addEventListener("click", async () => {

    const url = websiteUrl.value.trim();

    if (url === "") {
        status.textContent = "Please enter a website URL.";
        return;
    }

    status.textContent = "Analyzing website...";

    try {

        // Python backend connection will be added here later.

        status.textContent = "Backend connection is not available yet.";

    } catch (error) {

        console.error(error);
        status.textContent = "Analysis failed.";

    }

});


// NEW ANALYSIS

const newAnalysis = document.querySelector("#newAnalysis");

newAnalysis.addEventListener("click", () => {

    websiteUrl.value = "";
    status.textContent = "";

    document.querySelector("#websitePreview").innerHTML =
        "<p>Website screenshot will appear here.</p>";

    document.querySelector("#attentionPreview").innerHTML =
        "<p>Attention analysis will appear here.</p>";

    // RESET UI ANALYSIS

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

            attentionPreview.innerHTML =
                "<p>Original website view.</p>";

        } else if (view === "heatmap") {

            attentionPreview.innerHTML = `
                <div class="heatmap-placeholder">
                    <strong>Heatmap</strong>
                    <span>ML attention visualization will appear here.</span>
                </div>
            `;

        } else if (view === "overlay") {

            attentionPreview.innerHTML = `
                <div class="overlay-placeholder">
                    <strong>Attention Overlay</strong>
                    <span>Attention areas will be displayed here.</span>
                </div>
            `;

        }

    });

});

