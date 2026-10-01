const API_URL = "http://localhost:8000/api";

async function fetchState() {
    try {
        const res = await fetch(`${API_URL}/state`);
        const data = await res.json();

        document.getElementById('val-cpu').innerText = `${data.metrics.cpu_percent}%`;
        document.getElementById('val-mem').innerText = `${data.metrics.memory_percent}%`;

        document.getElementById('process-tree').innerText = data.tree;

        const exps = data.experiments;
        for (const key in exps) {
            const exp = exps[key];

            const probCell = document.getElementById(`st-${key}-prob`);
            if (probCell) probCell.innerHTML = `<strong>${key.toUpperCase()}</strong><br><small>${exp.Problema}</small>`;

            const statCell = document.getElementById(`st-${key}-status`);
            if (statCell) {
                statCell.innerText = exp.estado;

                if (exp.estado.includes("PROBLEMA") || exp.estado === "ACTIVO") statCell.style.color = "#ef4444";
                else if (exp.estado === "CORREGIDO" || exp.estado === "CONTROLADO") statCell.style.color = "#10b981";
                else statCell.style.color = "inherit";
            }

            const antesCell = document.getElementById(`st-${key}-antes`);
            if (antesCell) antesCell.innerText = exp.Antes;

            const despuesCell = document.getElementById(`st-${key}-despues`);
            if (despuesCell) despuesCell.innerText = exp.Despues;

            const mecCell = document.getElementById(`st-${key}-mec`);
            if (mecCell) mecCell.innerHTML = `<strong>${exp.Correccion}</strong><br><small>${exp.Mecanismo}</small>`;
        }
    } catch (e) {
        console.error("Error obteniendo estado", e);
    }
}

async function fetchLogs() {
    try {
        const res = await fetch(`${API_URL}/logs`);
        const data = await res.json();
        const logEl = document.getElementById('events-log');
        logEl.innerText = data.logs;
        logEl.scrollTop = logEl.scrollHeight;

        const dlRes = await fetch(`${API_URL}/logs/deadlock`);
        const dlData = await dlRes.json();
        const dlWindow = document.getElementById('deadlock-logs-window');
        if (dlWindow) {
            dlWindow.innerText = dlData.logs;
            dlWindow.scrollTop = dlWindow.scrollHeight;
        }

        const pcRes = await fetch(`${API_URL}/logs/producer_consumer`);
        const pcData = await pcRes.json();
        const pcWindow = document.getElementById('producer-logs-window');
        if (pcWindow) {
            pcWindow.innerText = pcData.logs;
            pcWindow.scrollTop = pcWindow.scrollHeight;
        }
    } catch (e) { }
}

async function trigger(endpoint) {
    try {
        await fetch(`${API_URL}/simulation/${endpoint}`, { method: 'POST' });
        fetchState();
        fetchLogs();
    } catch (e) {
        alert("Error de red: " + e.message);
    }
}

setInterval(fetchState, 1500);
setInterval(fetchLogs, 1500);
fetchState();
fetchLogs();
