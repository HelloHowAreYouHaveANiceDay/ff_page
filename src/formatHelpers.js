import * as htl from "npm:htl"

export function gamePointsIndicator(value) {
  if (value === null) {
    return "🔘";
  }
  return value > 30
    ? "🧀"
    : value > 20
    ? "🟪"
    : value > 15
    ? "🟦"
    : value > 10
    ? "🟩"
    : value > 5
    ? "🟨"
    : "💩";
}

export function sparkbar(max) {
  return (x) => htl.html`<div style="
      background: var(--theme-foreground-focus);
      color: white;
      font: 10px/1.6 var(--sans-serif);
      width: ${(100 * x) / max}%;
      float: right;
      padding-right: 3px;
      box-sizing: border-box;
      overflow: visible;
      display: flex;
      justify-content: end;">${x.toLocaleString("en-US")}`;
}
