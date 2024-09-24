
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
