(() => {
  "use strict";

  const state = { suppliers: [], claims: [], view: "overview", selectedSupplier: "" };
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const formatRM = (amount) => `RM ${Number(amount || 0).toFixed(2)}`;
  const esc = (value = "") => String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
  const safeDate = (value) => {
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? "Date unavailable" : date.toLocaleString(undefined, { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
  };
  const statusMarkup = (claim) => claim.status === "authorized_demo"
    ? '<span class="badge authorized"><i class="status-dot green"></i>Authorized · demo</span>'
    : '<span class="badge pending"><i class="status-dot amber"></i>Pending review</span>';
  let toastTimer;

  function showToast(message, isError = false) {
    const toast = $("#toast");
    toast.textContent = message;
    toast.classList.toggle("error", isError);
    toast.classList.add("visible");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => toast.classList.remove("visible"), 4200);
  }

  function setLoading(isLoading) {
    const overlay = $("#loading-overlay");
    if (isLoading) {
      overlay.classList.remove("done");
      overlay.classList.remove("hidden");
    } else {
      overlay.classList.add("done");
      window.setTimeout(() => overlay.classList.add("hidden"), 240);
    }
  }

  function getPending() {
    return state.claims.filter((claim) => claim.status === "pending_review").sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  }

  function renderSupplierOptions() {
    const select = $("#supplier-select");
    if (!state.suppliers.length) {
      select.innerHTML = '<option value="">No suppliers available</option>';
      select.disabled = true;
      return;
    }
    const current = state.selectedSupplier || select.value;
    select.innerHTML = `<option value="">Choose a supplier…</option>${state.suppliers.map((supplier) => `<option value="${esc(supplier.name)}">${esc(supplier.name)}</option>`).join("")}`;
    select.disabled = false;
    if (state.suppliers.some((supplier) => supplier.name === current)) select.value = current;
    state.selectedSupplier = select.value;
    updateSupplierDetail();
  }

  function updateSupplierDetail() {
    const supplier = state.suppliers.find((entry) => entry.name === $("#supplier-select").value);
    $("#supplier-item").textContent = supplier ? supplier.item : "Supplier item details appear here";
    $("#supplier-cost").textContent = supplier ? `${formatRM(supplier.cost)} / unit` : "";
    updateEstimate();
  }

  function updateEstimate() {
    const supplier = state.suppliers.find((entry) => entry.name === $("#supplier-select").value);
    const quantity = Number($("#quantity").value);
    const amount = supplier && quantity > 0 ? supplier.cost * quantity : 0;
    $("#estimate-value").innerHTML = `RM <span>${amount.toFixed(2)}</span>`;
  }

  function renderSummary() {
    const pending = getPending();
    const authorized = state.claims.filter((claim) => claim.status === "authorized_demo");
    const total = state.claims.reduce((sum, claim) => sum + Number(claim.loss || 0), 0);
    $("#stat-total").textContent = String(state.claims.length).padStart(2, "0");
    $("#stat-pending").textContent = String(pending.length).padStart(2, "0");
    $("#stat-authorized").textContent = String(authorized.length).padStart(2, "0");
    $("#stat-value").textContent = formatRM(total);
    $("#pending-nav-count").textContent = pending.length;
    $("#review-pending-count").textContent = pending.length;
    $("#queue-count").textContent = pending.length;
    $("#claim-count-label").textContent = `${state.claims.length} ${state.claims.length === 1 ? "RECORD" : "RECORDS"}`;
    $("#audit-total").textContent = `${state.claims.length} ${state.claims.length === 1 ? "RECORD" : "RECORDS"}`;
  }

  function claimRow(claim, withAction = true) {
    const itemCell = `${esc(claim.supplier)}<span class="item-cell">${esc(claim.item)}</span>`;
    const action = withAction && claim.status === "pending_review" ? `<button class="row-action" type="button" data-review-id="${esc(claim.id)}">Review →</button>` : "";
    return `<tr>
      <td><span class="claim-id">${esc(claim.id)}</span><span class="claim-date">${esc(safeDate(claim.createdAt))}</span></td>
      <td><span class="supplier-cell">${itemCell}</span></td>
      <td>${esc(claim.quantity)} units</td>
      <td><span class="amount">${formatRM(claim.loss)}</span></td>
      <td>${statusMarkup(claim)}</td>
      <td>${action}</td>
    </tr>`;
  }

  function renderRecent() {
    const sorted = [...state.claims].sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)).slice(0, 5);
    const body = $("#recent-claims");
    body.innerHTML = sorted.map((claim) => claimRow(claim)).join("");
    $("#claims-empty").classList.toggle("hidden", state.claims.length > 0);
    $(".table-scroll", $(".claims-panel")).classList.toggle("hidden", state.claims.length === 0);
  }

  function renderQueue() {
    const pending = getPending().slice(0, 4);
    const queue = $("#queue-list");
    queue.innerHTML = pending.length ? pending.map((claim) => `<button class="queue-item" type="button" data-review-id="${esc(claim.id)}">
      <span><strong>${esc(claim.supplier)}</strong><small>${esc(claim.id)} · ${esc(claim.quantity)} units</small></span>
      <span class="amount">${formatRM(claim.loss)}</span>
    </button>`).join("") : '<div class="queue-empty">All clear. No claims waiting for review.</div>';
  }

  function renderReview() {
    const pending = getPending();
    const target = $("#review-content");
    if (!pending.length) {
      target.innerHTML = '<div class="review-empty"><strong>Review queue is clear</strong><p>New floor incidents will appear here before any decision is recorded.</p><button class="text-button" type="button" data-jump="intake">Log an incident <span>↗</span></button></div>';
      return;
    }
    target.innerHTML = pending.map((claim) => `<article class="review-claim" data-claim="${esc(claim.id)}">
      <div class="review-claim-head"><div><span class="claim-id">${esc(claim.id)}</span><span class="claim-date">Submitted ${esc(safeDate(claim.createdAt))}</span></div>${statusMarkup(claim)}</div>
      <div class="review-claim-grid">
        <div class="claim-facts">
          <div class="fact-row"><span>SUPPLIER</span><strong>${esc(claim.supplier)}</strong></div>
          <div class="fact-row"><span>ITEM / UNIT COST</span><strong>${esc(claim.item)} · ${formatRM(claim.unitCost)}</strong></div>
          <div class="fact-row"><span>QUANTITY / CLAIMED VALUE</span><strong>${esc(claim.quantity)} units · ${formatRM(claim.loss)}</strong></div>
          <div class="fact-row"><span>FLOOR WORKER NOTES</span><p>${esc(claim.notes || "No additional notes.")}</p></div>
        </div>
        <div><label class="review-letter-label" for="letter-${esc(claim.id)}">CLAIM LETTER DRAFT <span>Editable before authorization</span></label><textarea class="letter-editor" id="letter-${esc(claim.id)}">${esc(claim.letter || "")}</textarea></div>
      </div>
      <div class="review-claim-actions"><input class="manager-name" type="text" autocomplete="name" aria-label="Manager full name" placeholder="Manager full name" required><span class="action-explainer">Authorization is recorded locally for demo purposes only.</span><button class="button button-accent authorize-button" type="button" data-authorize-id="${esc(claim.id)}">Authorize claim <span class="button-arrow">↗</span></button></div>
    </article>`).join("");
  }

  function renderAudit() {
    const all = [...state.claims].sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    $("#audit-claims").innerHTML = all.map((claim) => `<tr>
      <td><span class="claim-id">${esc(claim.id)}</span><span class="claim-date">${esc(safeDate(claim.createdAt))}</span></td>
      <td><span class="supplier-cell">${esc(claim.supplier)}</span></td><td>${esc(claim.item)}</td><td>${esc(claim.quantity)}</td>
      <td><span class="amount">${formatRM(claim.loss)}</span></td><td>${statusMarkup(claim)}</td><td>${claim.authorizedBy ? esc(claim.authorizedBy) : '<span class="claim-date">—</span>'}</td>
    </tr>`).join("");
    $("#audit-empty").classList.toggle("hidden", all.length > 0);
    $(".audit-table-scroll").classList.toggle("hidden", all.length === 0);
  }

  function render() {
    renderSummary();
    renderRecent();
    renderQueue();
    renderReview();
    renderAudit();
  }

  function goTo(view) {
    const validViews = ["overview", "intake", "review", "audit"];
    if (!validViews.includes(view)) return;
    state.view = view;
    $$(".nav-link").forEach((button) => button.classList.toggle("active", button.dataset.view === view || (view === "intake" && button.dataset.view === "overview")));
    $("#crumb-current").textContent = ({ overview: "Control room", intake: "Log incident", review: "Manager review", audit: "Audit history" })[view];
    $(".main-grid").classList.toggle("hidden", view !== "overview");
    $(".status-strip").classList.toggle("hidden", view !== "overview");
    $(".notice").classList.toggle("hidden", view !== "overview");
    $(".page-heading").classList.toggle("hidden", view !== "overview");
    $("#review-view").classList.toggle("hidden", view !== "review");
    $("#audit-view").classList.toggle("hidden", view !== "audit");
    if (view === "intake") {
      $(".main-grid").classList.remove("hidden");
      $(".status-strip").classList.add("hidden");
      $(".notice").classList.remove("hidden");
      $(".page-heading").classList.remove("hidden");
      $("#intake-panel").scrollIntoView({ behavior: "smooth", block: "start" });
    } else if (view === "review" || view === "audit") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  async function loadBootstrap() {
    setLoading(true);
    try {
      const response = await fetch("/api/bootstrap", { headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error(`Workspace request failed (${response.status}).`);
      const data = await response.json();
      state.suppliers = Array.isArray(data.suppliers) ? data.suppliers : [];
      state.claims = Array.isArray(data.claims) ? data.claims : [];
      renderSupplierOptions();
      render();
      $("#intake-message").textContent = "";
    } catch (error) {
      const message = esc(error.message || "Unable to load workspace data.");
      $("#supplier-select").innerHTML = '<option value="">Workspace unavailable</option>';
      $("#supplier-select").disabled = true;
      $("#recent-claims").innerHTML = `<tr><td colspan="6"><div class="error-state">Could not load live workspace data. <button type="button" data-retry>Retry</button><br>${message}</div></td></tr>`;
      $("#queue-list").innerHTML = `<div class="error-state">Could not load the review queue. <button type="button" data-retry>Retry</button></div>`;
      $("#review-content").innerHTML = `<div class="error-state">Could not load manager review. <button type="button" data-retry>Retry</button></div>`;
      $("#audit-claims").innerHTML = `<tr><td colspan="7"><div class="error-state">Could not load audit history. <button type="button" data-retry>Retry</button></div></td></tr>`;
      $("#stat-total").textContent = "—";
      $("#stat-pending").textContent = "—";
      $("#stat-authorized").textContent = "—";
      $("#stat-value").textContent = "—";
      showToast("Live workspace data could not be loaded.", true);
    } finally {
      setLoading(false);
    }
  }

  async function submitIncident(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const message = $("#intake-message");
    const submit = $("#submit-incident");
    const supplier = $("#supplier-select").value;
    const quantity = Number($("#quantity").value);
    const notes = $("#incident-notes").value.trim();
    if (!supplier || !Number.isInteger(quantity) || quantity < 1 || !notes) {
      message.className = "form-message";
      message.textContent = "Choose a supplier, enter a whole quantity, and add the raw incident notes.";
      return;
    }
    submit.disabled = true;
    submit.innerHTML = "<span>Submitting…</span>";
    message.textContent = "";
    try {
      const response = await fetch("/api/claims", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ supplier, quantity, notes })
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || `Incident submission failed (${response.status}).`);
      if (!data.claim) throw new Error("The server response did not include a claim.");
      state.claims = [data.claim, ...state.claims.filter((claim) => claim.id !== data.claim.id)];
      render();
      form.reset();
      state.selectedSupplier = "";
      updateSupplierDetail();
      message.className = "form-message success";
      message.textContent = `Incident ${data.claim.id} submitted. It is now waiting for manager review.`;
      showToast("Incident submitted to the manager review queue.");
    } catch (error) {
      message.className = "form-message";
      message.textContent = error.message || "Incident could not be submitted. Please try again.";
      showToast(message.textContent, true);
    } finally {
      submit.disabled = false;
      submit.innerHTML = "<span>Submit incident</span><span class=\"button-arrow\">↗</span>";
    }
  }

  async function authorizeClaim(button) {
    const id = button.dataset.authorizeId;
    const card = button.closest(".review-claim");
    const managerName = $(".manager-name", card).value.trim();
    const finalLetter = $(".letter-editor", card).value.trim();
    if (!managerName) {
      $(".manager-name", card).focus();
      showToast("Enter the manager’s full name before authorizing.", true);
      return;
    }
    if (!finalLetter) {
      $(".letter-editor", card).focus();
      showToast("The claim letter cannot be empty.", true);
      return;
    }
    button.disabled = true;
    button.innerHTML = "Recording…";
    try {
      const response = await fetch(`/api/claims/${encodeURIComponent(id)}/authorize`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ authorizedBy: managerName, finalLetter })
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.error || `Authorization recording failed (${response.status}).`);
      if (!data.claim) throw new Error("The server response did not include the updated claim.");
      state.claims = state.claims.map((claim) => claim.id === id ? data.claim : claim);
      render();
      showToast("Manager authorization recorded locally for demo purposes only.");
    } catch (error) {
      button.disabled = false;
      button.innerHTML = 'Authorize claim <span class="button-arrow">↗</span>';
      showToast(error.message || "Authorization could not be recorded. Please try again.", true);
    }
  }

  document.addEventListener("click", (event) => {
    const jump = event.target.closest("[data-jump]");
    if (jump) {
      goTo(jump.dataset.jump);
      return;
    }
    const nav = event.target.closest("[data-view]");
    if (nav) {
      goTo(nav.dataset.view);
      return;
    }
    const review = event.target.closest("[data-review-id]");
    if (review) {
      goTo("review");
      const card = $(`[data-claim="${CSS.escape(review.dataset.reviewId)}"]`, $("#review-content"));
      if (card) card.scrollIntoView({ behavior: "smooth", block: "center" });
      return;
    }
    const authorize = event.target.closest("[data-authorize-id]");
    if (authorize) {
      authorizeClaim(authorize);
      return;
    }
    if (event.target.closest("[data-retry]")) loadBootstrap();
  });

  $("#supplier-select").addEventListener("change", (event) => {
    state.selectedSupplier = event.target.value;
    updateSupplierDetail();
  });
  $("#quantity").addEventListener("input", updateEstimate);
  $("#incident-form").addEventListener("submit", submitIncident);
  const now = new Date();
  $("#today-date").textContent = now.toLocaleDateString(undefined, { weekday: "short", day: "2-digit", month: "short", year: "numeric" }).toUpperCase();
  $("#footer-time").textContent = now.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
  loadBootstrap();
})();
