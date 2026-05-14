window.showMiniBrowser = function(html, url) {
    const panel = document.getElementById('mini-browser-panel');
    panel.style.display = 'block';
    panel.innerHTML = `<div>
        <strong>Agent's web view:</strong> <a href="${url}" target="_blank">${url}</a>
        <pre style="background:#222;color:#eee;max-height:320px;overflow:auto;">${html}</pre>
    </div>`;
}
