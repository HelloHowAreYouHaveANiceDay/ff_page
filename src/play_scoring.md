---
title: Spread
toc: true
sql:
  game_player: ./data/game_player_2024.parquet
---

```sql id=game_player_q
SELECT
    *
FROM game_player
```

```js
const omit_zeros = view(Inputs.toggle({label: "Omit Zero", value: true}));
```

```js
const position = view(Inputs.checkbox(["WR", "QB", "RB", "TE"], {label: "Position", value:["WR", "QB", "RB", "TE"]}));
```

```js
function filter_checks(x) {
    const checks = [
        omit_zeros ? x['fp'] !== 0 : true,
        position.includes(x['position'])
    ]

    return checks.every(f => f)
}
```

```js
const game_player_data = d3.filter(game_player_q, filter_checks);
```

```js
function playsHistogram(data, { width }) {
  return Plot.plot({
    title: "Week over Week Play Type",
    width,
    color: { scheme: "BuRd", legend: true },
    marks: [
      Plot.rectY(data, Plot.binX({ y: "count" }, { x: "fp"})),
      Plot.rectY(game_player_q, Plot.binX({ y: "count" }, { x: "fp"})),
      Plot.ruleX([d3.mean(game_player_q, x => x.fp)]),
      Plot.ruleX([d3.mean(data, x => x.fp)], {stroke: "red"})
    ]
  });
}
```
<div class="grid grid-cols-3">
    <div>Median FP: ${d3.median(game_player_data, x => x.fp)}</div>
    <div>Mean FP: ${d3.mean(game_player_data, x => x.fp)}</div>
    <div>Max FP: ${d3.max(game_player_data, x => x.fp)}</div>


</div>

<div class="grid grid-cols-1">
  <div class="card">
     ${resize((width) => playsHistogram(game_player_data, {width}))}
  </div>
</div>
