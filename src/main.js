document.querySelector("#website").innerHTML = `

    <header class="header">
        <div class="logo"><b>Visual Attention & UX Analyzer</b></div>
        <div class="header-subtitle">ML-Powered Website Analysis</div>
    </header>

    <main class="container">

        <section class="hero">
            <h1>Analyze a Website</h1>

            <p>
                Enter a website URL to analyze its
                visual attention and user experience.
            </p>

            <div class="url-box">
                <input
                    id="websiteUrl"
                    type="text"
                    placeholder="https://example.com"
                >

                <button id="analyzeButton">
                    Analyze Website
                </button>
            </div>

            <p id="status"></p>
        </section>


        <section class="card">

            <div class="section-header">
                <h2>Website Preview</h2>

                <span class="badge">
                    Original
                </span>
            </div>

            <div id="websitePreview" class="preview">
                <p>Website screenshot will appear here.</p>
            </div>

        </section>


        <section class="card">

            <div class="section-header">
                <h2>Visual Attention</h2>
            </div>

            <div class="tabs">

                <button class="tab active" data-view="original">
                    Original
                </button>

                <button class="tab" data-view="heatmap">
                    Heatmap
                </button>

                <button class="tab" data-view="overlay">
                    Overlay
                </button>

            </div>

            <div id="attentionPreview" class="attention-preview">
                <p>Attention analysis will appear here.</p>
            </div>

        </section>


        <section class="card">

            <h2>UI Element Analysis</h2>

            <div class="analysis-grid">

                <div class="analysis-item">
                    <span>CTA Prominence</span>
                    <strong id="ctaScore">—</strong>
                </div>

                <div class="analysis-item">
                    <span>Headline Prominence</span>
                    <strong id="headlineScore">—</strong>
                </div>

                <div class="analysis-item">
                    <span>Visual Clutter</span>
                    <strong id="clutterScore">—</strong>
                </div>

                <div class="analysis-item">
                    <span>Text Density</span>
                    <strong id="textScore">—</strong>
                </div>

            </div>

        </section>


        <section class="card">

            <h2>UX Performance</h2>

            <div class="metrics-grid">

                <div class="metric">
                    <span>Overall UX</span>
                    <strong id="uxScore">—</strong>
                </div>

                <div class="metric">
                    <span>Visual Hierarchy</span>
                    <strong id="hierarchyScore">—</strong>
                </div>

                <div class="metric">
                    <span>CTA Visibility</span>
                    <strong id="ctaVisibility">—</strong>
                </div>

                <div class="metric">
                    <span>Above Fold Attention</span>
                    <strong id="aboveFold">—</strong>
                </div>

            </div>

        </section>


        <section class="card">

            <h2>Key Findings</h2>

            <div id="findings">
                <p class="empty">
                    Analysis findings will appear here.
                </p>
            </div>

        </section>


        <section class="card">

            <h2>Recommendations</h2>

            <div id="recommendations">
                <p class="empty">
                    Recommendations will appear here.
                </p>
            </div>

        </section>


        <div class="actions">

            <button id="newAnalysis" class="secondary-button">
                New Analysis
            </button>

            <button id="downloadReport" class="primary-button">
                Download Report
            </button>

        </div>

    </main>


    <footer>
        Visual attention is predicted by machine learning
        and does not represent actual eye movements.
    </footer>

`;


/* ANALYZE */

const analyzeButton = document.querySelector("#analyzeButton");
const websiteUrl = document.querySelector("#websiteUrl");
const status = document.querySelector("#status");

analyzeButton.addEventListener("click", () => {

    const url = websiteUrl.value.trim();

    if (url === "") {
        status.textContent = "Please enter a website URL.";
        return;
    }

    status.textContent = "Analyzing website...";

    document.querySelector("#ctaScore").textContent = "82%";
    document.querySelector("#headlineScore").textContent = "91%";
    document.querySelector("#clutterScore").textContent = "28%";
    document.querySelector("#textScore").textContent = "35%";

    document.querySelector("#uxScore").textContent = "86%";
    document.querySelector("#hierarchyScore").textContent = "89%";
    document.querySelector("#ctaVisibility").textContent = "84%";
    document.querySelector("#aboveFold").textContent = "78%";

    document.querySelector("#findings").innerHTML = `
        <div class="finding">
            Strong visual hierarchy detected.
        </div>

        <div class="finding">
            Primary CTA has good visual prominence.
        </div>

        <div class="finding">
            Text density is relatively low.
        </div>
    `;

    document.querySelector("#recommendations").innerHTML = `
        <div class="recommendation">
            Keep the primary CTA visually prominent.
        </div>

        <div class="recommendation">
            Maintain clear spacing between major sections.
        </div>

        <div class="recommendation">
            Consider improving attention toward secondary content.
        </div>
    `;

    status.textContent = "Analysis completed.";
});


/* NEW ANALYSIS */

const newAnalysis = document.querySelector("#newAnalysis");

newAnalysis.addEventListener("click", () => {

    websiteUrl.value = "";
    status.textContent = "";

    document.querySelector("#websitePreview").innerHTML = `
        <p>Website screenshot will appear here.</p>
    `;

    document.querySelector("#attentionPreview").innerHTML = `
        <p>Attention analysis will appear here.</p>
    `;

    document.querySelector("#ctaScore").textContent = "—";
    document.querySelector("#headlineScore").textContent = "—";
    document.querySelector("#clutterScore").textContent = "—";
    document.querySelector("#textScore").textContent = "—";

    document.querySelector("#uxScore").textContent = "—";
    document.querySelector("#hierarchyScore").textContent = "—";
    document.querySelector("#ctaVisibility").textContent = "—";
    document.querySelector("#aboveFold").textContent = "—";

    document.querySelector("#findings").innerHTML = `
        <p class="empty">
            Analysis findings will appear here.
        </p>
    `;

    document.querySelector("#recommendations").innerHTML = `
        <p class="empty">
            Recommendations will appear here.
        </p>
    `;
});


/* TABS */

const tabs = document.querySelectorAll(".tab");
const attentionPreview = document.querySelector("#attentionPreview");

tabs.forEach((tab) => {

    tab.addEventListener("click", () => {

        tabs.forEach((item) => {
            item.classList.remove("active");
        });

        tab.classList.add("active");

        const view = tab.dataset.view;

        if (view === "original") {

            attentionPreview.innerHTML = `
                <p>
                    Original website view.
                </p>
            `;

        }

        if (view === "heatmap") {

            attentionPreview.innerHTML = `
                <div class="heatmap-placeholder">

                    <strong>Heatmap</strong>

                    <span>
                        ML attention visualization will appear here.
                    </span>

                </div>
            `;

        }

        if (view === "overlay") {

            attentionPreview.innerHTML = `
                <div class="overlay-placeholder">

                    <strong>Attention Overlay</strong>

                    <span>
                        Attention areas will be displayed here.
                    </span>

                </div>
            `;

        }

    });

});
