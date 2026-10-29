// Mirrors calc.py: keep the two in sync.
const $ = (id) => document.getElementById(id);
const parse = (v) => {
  const t = String(v ?? "").trim().replace(/\s/g, "").replace(",", ".");
  if (!t) return null;
  const n = Number(t);
  return Number.isFinite(n) ? n : NaN;
};
const fmt = (n, d = 2) => n.toLocaleString(undefined, { maximumFractionDigits: d });

const rowsEl = $("rows");

function addRow(focus) {
  const li = document.createElement("li");
  li.className = "row";
  li.innerHTML = `<div class="row-top">
    <div class="field label"><input class="name" placeholder="Label (optional)" aria-label="Label"></div>
    <div class="field amt"><input class="val" inputmode="decimal" autocomplete="off" placeholder="Amount" aria-label="Amount"></div>
    <span class="pct">–</span>
    <button class="del" type="button" aria-label="Remove row" title="Remove">×</button></div>
    <div class="bar"><i></i></div>`;
  rowsEl.appendChild(li);
  if (focus) li.querySelector(".val").focus();
  update();
}

function update() {
  const t = parse($("total").value);
  const validTotal = t !== null && !Number.isNaN(t) && t > 0;
  $("total").parentElement.classList.toggle("invalid", t !== null && !validTotal);
  $("total-hint").textContent = t === null ? "" :
    Number.isNaN(t) ? "That doesn't look like a number." :
    t <= 0 ? "Total must be greater than zero." : "";

  let sum = 0;
  rowsEl.querySelectorAll(".row").forEach((row) => {
    const a = parse(row.querySelector(".val").value);
    const field = row.querySelector(".val").parentElement;
    field.classList.toggle("invalid", Number.isNaN(a));
    const pct = row.querySelector(".pct"), fill = row.querySelector(".bar i");
    if (a !== null && !Number.isNaN(a)) sum += a;
    if (validTotal && a !== null && !Number.isNaN(a)) {
      const p = a / t * 100;
      pct.textContent = fmt(p) + "%";
      fill.style.width = Math.max(0, Math.min(100, p)) + "%";
      fill.classList.toggle("over", p > 100);
    } else {
      pct.textContent = "–";
      fill.style.width = "0";
    }
  });

  const rem = $("rem").closest(".stat");
  $("sum").textContent = fmt(sum);
  if (validTotal) {
    const r = t - sum, over = r < 0;
    $("sum-pct").textContent = fmt(sum / t * 100) + "% of total";
    $("rem-label").textContent = over ? "Over total by" : "Remaining";
    $("rem").textContent = fmt(Math.abs(r));
    $("rem-pct").textContent = fmt(Math.abs(r) / t * 100) + "%";
    rem.classList.toggle("over", over);
    const f = $("total-fill");
    f.style.width = Math.min(100, sum / t * 100) + "%";
    f.classList.toggle("over", over);
  } else {
    $("sum-pct").textContent = "";
    $("rem-label").textContent = "Remaining";
    $("rem").textContent = "–";
    $("rem-pct").textContent = "";
    rem.classList.remove("over");
    $("total-fill").style.width = "0";
  }
}

document.addEventListener("input", update);
$("add").addEventListener("click", () => addRow(true));
rowsEl.addEventListener("click", (e) => {
  const btn = e.target.closest(".del");
  if (!btn) return;
  const row = btn.closest(".row");
  row.classList.add("leaving");
  setTimeout(() => { row.remove(); update(); }, 200);
});
addRow(false); addRow(false);
