const BASE = window.location.origin;
let API_KEY = '';

function headers() {
  const h = { 'Content-Type': 'application/json' };
  if (API_KEY) h['X-API-Key'] = API_KEY;
  return h;
}

function setApiKey() {
  API_KEY = document.getElementById('api-key').value;
  document.getElementById('auth-status').textContent = API_KEY ? 'Connected' : '';
  loadMerchants();
}

async function api(path) {
  const res = await fetch(`${BASE}/api/v1${path}`, { headers: headers() });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

async function loadMerchants() {
  try {
    const data = await api('/onboarding/');
    const tbody = document.querySelector('#merchants-table tbody');
    tbody.innerHTML = '';
    data.forEach(m => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${m.id}</td>
        <td>${m.company_name || m.name || '-'}</td>
        <td><span class="status-badge status-${m.status}">${m.status}</span></td>
        <td>${new Date(m.created_at).toLocaleDateString()}</td>
        <td><button class="btn-view" onclick="showDetail('${m.id}')">View</button></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error('Failed to load merchants:', e);
  }
}

async function showDetail(id) {
  document.getElementById('merchant-list').style.display = 'none';
  document.getElementById('merchant-detail').style.display = 'block';
  try {
    const m = await api(`/onboarding/${id}`);
    document.getElementById('detail-name').textContent = m.company_name || m.name;
    document.getElementById('detail-status').innerHTML = `<span class="status-badge status-${m.status}">${m.status}</span>`;
    loadTab('checklist', id);
    document.querySelectorAll('.tab').forEach(t => {
      t.onclick = () => {
        document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
        t.classList.add('active');
        loadTab(t.dataset.tab, id);
      };
    });
  } catch (e) {
    document.getElementById('tab-content').innerHTML = `<p>Error: ${e.message}</p>`;
  }
}

function showList() {
  document.getElementById('merchant-list').style.display = 'block';
  document.getElementById('merchant-detail').style.display = 'none';
}

async function loadTab(tab, merchantId) {
  const el = document.getElementById('tab-content');
  try {
    if (tab === 'checklist') {
      const items = await api(`/checklist/?merchant_id=${merchantId}`);
      el.innerHTML = items.length ? `<table><thead><tr><th>Item</th><th>Status</th></tr></thead><tbody>${items.map(i => `<tr><td>${i.name || i.item_key}</td><td><span class="status-badge status-${i.status}">${i.status}</span></td></tr>`).join('')}</tbody></table>` : '<p>No checklist items</p>';
    } else if (tab === 'snapshots') {
      const snaps = await api(`/monitor/snapshots/${merchantId}`);
      el.innerHTML = snaps.length ? snaps.map(s => `<div><img src="${s.screenshot_url}" style="max-width:400px"><p>${new Date(s.created_at).toLocaleString()} | Diff: ${s.diff_percentage || 0}%</p></div>`).join('') : '<p>No snapshots</p>';
    } else if (tab === 'purchases') {
      const purchases = await api(`/test-purchase/?merchant_id=${merchantId}`);
      el.innerHTML = purchases.length ? `<table><thead><tr><th>Date</th><th>Amount</th><th>Result</th></tr></thead><tbody>${purchases.map(p => `<tr><td>${new Date(p.created_at).toLocaleDateString()}</td><td>${p.amount || '-'}</td><td><span class="status-badge status-${p.result}">${p.result}</span></td></tr>`).join('')}</tbody></table>` : '<p>No purchases</p>';
    } else if (tab === 'crm') {
      const workflows = await api(`/crm/${merchantId}`);
      el.innerHTML = `<pre>${JSON.stringify(workflows, null, 2)}</pre>`;
    }
  } catch (e) {
    el.innerHTML = `<p>Error loading ${tab}: ${e.message}</p>`;
  }
}

document.addEventListener('DOMContentLoaded', loadMerchants);
