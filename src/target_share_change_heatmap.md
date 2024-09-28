---
title: Rush Share wow
toc: true
sql:
  player_game: ./data/game_player_2024.parquet
---

```sql id=game_player_q display
SELECT
    *,
    target_share - LAG(target_share) OVER (PARTITION BY player_id ORDER BY week) AS wow
FROM player_game
WHERE target_share > .1
```

```js
function target_share_change_heatmap(data, { width }) {
  return Plot.plot({
  marginLeft: 120,
  padding: 0,
  y: {label: null},
  color: {scheme: "turbo", legend: true},
  marks: [
    Plot.cell(
      data,
      Plot.group(
        {fill: "median"},
        {x: (d) => d.week, y: "display_name",fill: "wow", inset: 0.5, sort: 
        {y: "fill"}}
      )
    )
  ]
})
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => target_share_change_heatmap(game_player_q, {width}))}
  </div>
</div>