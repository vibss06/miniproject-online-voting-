const backendUrl = () => window.BACKEND_URL;

// Helpers
const q = (id) => document.getElementById(id);
const alertErr = (msg) => alert(msg || "Something went wrong");

// -------- Signup --------
async function doSignup(e) {
  e?.preventDefault();
  const name = q("s-name").value.trim();
  const email = q("s-email").value.trim();
  const username = q("s-username").value.trim();
  const password = q("s-password").value.trim();
  if (!name || !email || !username || !password) return alertErr("Fill all fields");

  const res = await fetch(`${backendUrl()}/signup`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ name, email, username, password })
  });
  const data = await res.json();
  if (res.ok) {
    alert("Signup successful!");
    q("signup-form").reset();
    window.location.href = "login.html";
  } else alertErr(data.error);
}

// -------- Login --------
async function doLogin(e) {
  e?.preventDefault();
  const username = q("l-username").value.trim();
  const password = q("l-password").value.trim();
  if (!username || !password) return alertErr("Enter username & password");

  const res = await fetch(`${backendUrl()}/login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ username, password })
  });
  const data = await res.json();
  if (res.ok) {
    // Store voter id for voting
    localStorage.setItem("voter_id", data.voter.id);
    localStorage.setItem("voter_name", data.voter.name);
    window.location.href = "vote.html";
  } else alertErr(data.error);
}

// -------- Load Candidates --------
async function loadCandidates() {
  const listEl = q("cand-list");
  const selectEl = q("cand-select");
  if (!listEl && !selectEl) return;

  const res = await fetch(`${backendUrl()}/candidates`);
  const data = await res.json();

  if (listEl) {
    listEl.innerHTML = "";
    data.forEach(c => {
      const li = document.createElement("li");
      li.textContent = `${c.name} (${c.party})`;
      listEl.appendChild(li);
    });
  }
  if (selectEl) {
    selectEl.innerHTML = "";
    data.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = `${c.name} (${c.party})`;
      selectEl.appendChild(opt);
    });
  }
}

// -------- Add Candidate (Admin demo) --------
async function addCandidate(e) {
  e?.preventDefault();
  const name = q("c-name").value.trim();
  const party = q("c-party").value.trim();
  if (!name || !party) return alertErr("Enter name & party");

  const res = await fetch(`${backendUrl()}/candidates`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ name, party })
  });
  const data = await res.json();
  if (res.ok) {
    alert("Candidate added");
    q("cand-form").reset();
    loadCandidates();
  } else alertErr(data.error);
}

// -------- Cast Vote --------
async function castVote(e) {
  e?.preventDefault();
  const voter_id = Number(localStorage.getItem("voter_id"));
  const candidate_id = Number(q("cand-select").value);
  if (!voter_id) return alertErr("Please login first");
  if (!candidate_id) return alertErr("Please choose a candidate");

  const res = await fetch(`${backendUrl()}/vote`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ voter_id, candidate_id })
  });
  const data = await res.json();
  if (res.ok) {
    alert("Vote cast successfully!");
    window.location.href = "results.html";
  } else alertErr(data.error);
}

// -------- Results --------
async function loadResults() {
  const res = await fetch(`${backendUrl()}/results`);
  const data = await res.json();
  const container = q("results");
  if (!container) return;

  container.innerHTML = "";
  data.forEach(r => {
    const div = document.createElement("div");
    div.className = "card";
    div.innerHTML = `<strong>${r.name}</strong> (${r.party}) — <b>${r.votes}</b> vote(s)`;
    container.appendChild(div);
  });
}

// Bind on pages
document.addEventListener("DOMContentLoaded", () => {
  if (q("signup-form")) q("signup-form").addEventListener("submit", doSignup);
  if (q("login-form")) q("login-form").addEventListener("submit", doLogin);
  if (q("cand-form")) q("cand-form").addEventListener("submit", addCandidate);
  if (q("cand-list") || q("cand-select")) loadCandidates();
  if (q("results")) loadResults();
  if (q("vote-form")) q("vote-form").addEventListener("submit", castVote);
});
