/* CMD: WRAP_METADATA & STYLIZE_HIERARCHY */
(function() {
    const label = Array.from(document.querySelectorAll('.author-label')).pop();
    const chunk = Array.from(document.querySelectorAll('ms-prompt-chunk')).pop();

    if (label && chunk) {
        // Apply AXION branding
        label.style.setProperty('color', '#00ff00', 'important');
        label.style.fontWeight = 'bold';
        
        // Inject Phoenix Anchor
        const anchor = document.createElement('div');
        anchor.innerHTML = `<div style="font-family: monospace; color: #00ff00; border: 1px solid #00ff00; padding: 10px; margin-bottom: 15px; background: rgba(0,255,0,0.05);">
            [OMNI-ARTIFACT-ANCHOR]<br>ID: SYNG.WORKSHOP.TURN<br>VER: v15.0 [OMEGA]
        </div>`;
        chunk.prepend(anchor);
        
        console.log("🏛️ Substrate Aligned to PRS-001");
    }
})();