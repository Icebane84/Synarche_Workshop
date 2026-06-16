(function () {
  const vscode = acquireVsCodeApi();

  const stardustCount = document.getElementById("stardust-count");
  const prestigeRank = document.getElementById("prestige-rank");
  const prestigeProgress = document.getElementById("prestige-progress");
  const achievementList = document.getElementById("achievement-list");

  // Handle messages sent from the extension to the webview
  window.addEventListener("message", (event) => {
    const message = event.data; // The json data that the extension sent
    switch (message.type) {
      case "updateStatus": {
        updateUI(message.data);
        break;
      }
    }
  });

  function updateUI(data) {
    if (data.stardust !== undefined) {
      stardustCount.textContent = data.stardust.toLocaleString();
    }
    if (data.rank) {
      prestigeRank.textContent = data.rank.toUpperCase();
    }
    if (data.progress !== undefined) {
      prestigeProgress.style.width = `${data.progress}%`;
    }
    if (data.achievements) {
      renderAchievements(data.achievements);
    }
  }

  function renderAchievements(achievements) {
    achievementList.innerHTML = "";
    achievements.forEach((ach) => {
      const item = document.createElement("div");
      item.className = `achievement-item ${ach.completed ? "completed" : "locked"}`;

      item.innerHTML = `
                <div class="achievement-info">
                    <div class="achievement-name">${ach.name} ${ach.completed ? "✦" : ""}</div>
                    <div class="achievement-desc">${ach.description}</div>
                </div>
                <div class="achievement-reward">${ach.completed ? "COMPLETED" : `+${ach.stardust_reward || 0}✦`}</div>
            `;

      if (!ach.completed) {
        item.addEventListener("click", () => {
          vscode.postMessage({ type: "achievementClaimed", id: ach.id });
        });
      }

      achievementList.appendChild(item);
    });
  }

  // Initial load simulation (or request data)
  // vscode.postMessage({ type: 'ready' });
})();
