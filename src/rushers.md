---
title: Rushers
toc: true
sql:
  game_player: ./data/game_player_2024.parquet
---


```sql id=game_player_q display
  SELECT
    player_id,
    FIRST(player_name) as player_name,
    FIRST(pos_team) as pos_team,
    FIRST(position) as position,
    COUNT(DISTINCT(game_id)) as games,
    SUM(rush_yards) as rush_yards,
    ROUND(AVG(rush_yards),0) as avg_rush_yards,
    SUM(rush_tds) as rush_tds,
    SUM(rec_tds) as rec_tds,
    SUM(rush_attempts) as rush_attempts,
    ROUND(SUM(rush_yards) / SUM(rush_attempts),0) as ypc,
    ROUND(100.0 * AVG(rush_share),0) as rush_share,
    SUM(fp) as fp,
    STDDEV(fp) as fp_var,
    SUM(rush_fp) as rush_fp,
    RANK() OVER (PARTITION BY FIRST(position) ORDER BY SUM(fp) DESC) as pos_rank
  FROM game_player
  WHERE rush_fp > 0 AND rush_attempts > 5
  GROUP BY 1
```

```js
const rusher_tip = (d) => `
${d.pos_team}|${d.position}|${d.player_name}\n
A:${d.rush_attempts}|Y:${d.rush_yards}\n
YPC: ${d.ypc}|YPG:${d.avg_rush_yards}|%:${d.rush_share}\n
G:${d.games}|TD:${d.rush_tds + d.rec_tds}\n
`

const highlight_top_10 = x => is_top_10(x) ? "red" : "grey"

const is_top_10 = (d) => d.position === 'RB' ? d.pos_rank <= 20 : false
```

```js
function targets_fp_scatter(data, { width }) {
  return Plot.plot({
    title: "Attempts vs Fantasy Points",
    width,
    color: {scheme: "BrBg"},
    x: {label: "fp"},
    y: {label: "attempts"},
    marks: [
    Plot.dot(data, {x: "rush_fp", y: "rush_attempts", fill: highlight_top_10}),
    Plot.linearRegressionY(data, {x: "rush_fp", y: "rush_attempts", stroke: "red"}),
    Plot.tip(data, Plot.pointer({
        x: "rush_fp",
        y: "rush_attempts",
        title: rusher_tip,
      })),
  ]
  });
}
```


```js
function catches_yards_scatter(data, { width }) {
  return Plot.plot({
    title: "Touchdown Dependence (Rush FP vs TDs)",
    width,
    color: {scheme: "BrBg"},
    x: {label: "Rush FP"},
    y: {label: "TDs"},
    marks: [
    Plot.dot(data, {x: "rush_fp", y: "rush_tds", fill:highlight_top_10}),
    Plot.linearRegressionY(data, {x: "rush_fp", y: "rush_tds", stroke: "red"}),
    Plot.tip(data, Plot.pointer({
        x: "rush_fp",
        y: "rush_tds",
        title: rusher_tip,
      })),
  ]
  });
}
```

```js
function target_share_catch_rate_scatter(data, { width }) {
  return Plot.plot({
    title: "Opportunity Efficiency",
    width,
    color: {scheme: "BrBg"},
    x: {label: "Rush Share"},
    y: {label: "YPC"},
    marks: [
    Plot.dot(data, {x: "rush_share", y: "ypc", fill:highlight_top_10}),
    Plot.linearRegressionY(data, {x: "rush_share", y: "ypc", stroke: "red"}),
    Plot.tip(data, Plot.pointer({
        x: "rush_share",
        y: "ypc",
        title: rusher_tip,
      })),
    Plot.ruleX([d3.median(data, x => x.rush_share)], {stroke: "red"}),
  ]
  });
}
```

<div class="grid grid-cols-2">
  <div class="card">
    ${resize((width) => targets_fp_scatter(game_player_q, {width}))}
  </div>
  <div class="card">
    ${resize((width) => catches_yards_scatter(game_player_q, {width}))}
  </div>
  <div class="card">
    ${resize((width) => target_share_catch_rate_scatter(game_player_q, {width}))}
  </div>
</div>