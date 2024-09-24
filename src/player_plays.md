---
theme: dashboard
title: Player Plays
toc: false
---

# Rocket plays 🚀

<!-- Load and transform the data -->

```js
const plays = await FileAttachment("data/plays.json").json();
// console.log(plays)
```

<!-- A shared color scale for consistency, sorted by the number of plays -->

```js
// get unique player names
const playerNames = Array.from(new Set(plays.map((d) => d.player_name)));
const positions = Array.from(new Set(plays.map((d) => d.position)));

const color = Plot.scale({
  color: {
    type: "categorical",
    domain: positions,
    unknown: "var(--theme-foreground-muted)",
  },
});
```

<!-- Cards with big numbers -->
<!-- 
<div class="grid grid-cols-4">
  <div class="card">
    <h2>United States 🇺🇸</h2>
    <span class="big">${plays.filter((d) => d.stateId === "US").length.toLocaleString("en-US")}</span>
  </div>
  <div class="card">
    <h2>Russia 🇷🇺 <span class="muted">/ Soviet Union</span></h2>
    <span class="big">${plays.filter((d) => d.stateId === "SU" || d.stateId === "RU").length.toLocaleString("en-US")}</span>
  </div>
  <div class="card">
    <h2>China 🇨🇳</h2>
    <span class="big">${plays.filter((d) => d.stateId === "CN").length.toLocaleString("en-US")}</span>
  </div>
  <div class="card">
    <h2>Other</h2>
    <span class="big">${plays.filter((d) => d.stateId !== "US" && d.stateId !== "SU" && d.stateId !== "RU" && d.stateId !== "CN").length.toLocaleString("en-US")}</span>
  </div>
</div> -->

<!-- Plot of launch history -->

```js
function launchTimeline(data, { width }) {
  return Plot.plot({
    title: "Targets vs. Fantasy Points",
    width,
    height: 300,
    color: { ...color, legend: true },
    marks: [
      Plot.dot(data, {
        x: "rec_targets",
        y: "fantasy_points",
        fill: "position",
        opacity: 0.6,
      }),
      Plot.tip(data, Plot.pointer({
        x: "rec_targets",
        y: "fantasy_points",
        title: d => `${d.player_name} \n (${d.game_id} - ${d.rec_targets} targets, ${d.fantasy_points} points)`,
      })),
      Plot.ruleY([0]),
    ],
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => launchTimeline(plays.filter(p => p.rec_targets > 0), {width}))}
  </div>
</div>

<!-- Plot of launch vehicles -->

```js
function vehicleChart(data, { width }) {
  return Plot.plot({
    title: "Popular launch vehicles",
    width,
    height: 300,
    marginTop: 0,
    marginLeft: 50,
    x: { grid: true, label: "games" },
    y: { label: null },
    color: { ...color, legend: true },
    marks: [
      Plot.rectY(
        data,
        Plot.binX(
          { y: "count" },
          {
            x: "fantasy_points",
            fill: "position",
            tip: true,
            sort: { x: "-y" },
          }
        )
      ),
      Plot.ruleY([0]),
    ],
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => vehicleChart(plays, {width}))}
  </div>
</div>
