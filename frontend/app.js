
const API_URL = "/api";

const urlInput = document.getElementById('urlInput');
const downloadBtn = document.getElementById('downloadBtn');
const resultsArea = document.getElementById('resultsArea');
const errorMsg = document.getElementById('error-message');
const btnLoader = document.querySelector('.loader');
const btnText = document.querySelector('.btn-text');

downloadBtn.addEventListener('click', handleDownload);

async function handleDownload() {
    // Reset state
    errorMsg.classList.add('hidden');
    resultsArea.innerHTML = '';

    const rawInput = urlInput.value;
    if (!rawInput.trim()) {
        showError("Please enter at least one Instagram URL");
        return;
    }

    const urls = rawInput.split('\n').filter(u => u.trim().length > 0);

    setLoading(true);

    try {
        const response = await fetch(`${API_URL}/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ urls: urls })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Download failed");
        }

        displayResults(data.results);

        if (data.results && data.results.length === 0) {
            showError(data.message || "No valid media found");
        }

    } catch (err) {
        showError(err.message);
    } finally {
        setLoading(false);
    }
}

function displayResults(results) {
    if (!results) return;

    resultsArea.classList.remove('hidden');

    results.forEach(item => {
        const card = document.createElement('div');
        card.className = 'url-result-card';

        const thumbUrl = item.thumbnail_url || 'https://via.placeholder.com/80?text=Insta';

        card.innerHTML = `
            <img src="${thumbUrl}" alt="Thumbnail" class="thumbnail" onerror="this.src='https://via.placeholder.com/80?text=Error'">
            <div class="info">
                <h3>${item.filename}</h3>
                <a href="${item.media_url}" target="_blank" download class="download-link">
                    Download ${item.media_type === 'video' ? 'Video' : 'Image'}
                </a>
            </div>
        `;

        resultsArea.appendChild(card);
    });
}

function setLoading(isLoading) {
    if (isLoading) {
        downloadBtn.disabled = true;
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
    } else {
        downloadBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}

function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.classList.remove('hidden');
}
