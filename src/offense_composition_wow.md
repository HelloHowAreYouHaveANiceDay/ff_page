---
title: Offense Mix
toc: true
sql:
  player_game: ./data/play_player_2024.parquet
---

```sql id=week_over_week_play_type display
SELECT
    week,
    pos_team,
    play_type,
    COALESCE(rec_yards,0) + COALESCE(rush_yards,0) as yards,
FROM player_game
```

```js
function vehicleChart(data, { width }) {
  return Plot.plot({
    title: "Week over Week Play Type",
    width,
    marginTop: 0,
    marginLeft: 50,
    height: 2000,
    color: { legend: true },
    x: { grid: true, nice: true },
    y: { label: null},
    facet: {
      data,
      y: "pos_team",
    },
    marks: [
      Plot.frame(),
      Plot.barY(data, {x: "week", y: "yards", fill: "play_type"}),
    ],
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => vehicleChart(week_over_week_play_type, {width}))}
  </div>
</div>
