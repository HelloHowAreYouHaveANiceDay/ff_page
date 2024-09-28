---
title: Receivers
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
    SUM(rec_yards) as rec_yards,
    SUM(rec_tds) as rec_tds,
    SUM(rec_completes) as rec_completes,
    SUM(rec_targets) as rec_targets,
    ROUND(100.0 * AVG(target_share),0) as target_share,
    ROUND(100.0 * SUM(rec_completes) / SUM(rec_targets),0) as catch_rate,
    SUM(rec_fp) as rec_fp,
    RANK() OVER (PARTITION BY FIRST(position) ORDER BY SUM(fp) DESC) as pos_rank,
    SUM(fp) as fp,
  FROM game_player
  WHERE rec_fp > 0 AND rec_targets > 5
  GROUP BY player_id
```

```js
const receiver_tip = (d) => `
${d.pos_team}|${d.position}|${d.player_name}\n
T:${d.rec_targets}|C:${d.rec_completes}|Y:${d.rec_yards}\n
CR:${d.catch_rate}%|TS:${d.target_share}%\n
G:${d.games}|TD:${d.rec_tds}\n
`

const highlight_top_10 = x => is_top_10(x) ? "red" : "grey"

const is_top_10 = (d) => d.position === 'WR' ? d.pos_rank <= 20 : false
```

```js
function targets_fp_scatter(data, { width }) {
  return Plot.plot({
    title: "Targets vs Rec Fantasy Points",
    width,
    color: {scheme: "BrBg"},
    x: {label: "Rec FP"},
    y: {label: "Targets"},
    marks: [
    Plot.dot(data, {x: "rec_fp", y: "rec_targets", fill:highlight_top_10}),
    Plot.linearRegressionY(data, {x: "rec_fp", y: "rec_targets", stroke: "red"}),
    Plot.tip(data, Plot.pointer({
        x: "rec_fp",
        y: "rec_targets",
        title: receiver_tip,
      })),
  ]
  });
}
```


```js
function catches_yards_scatter(data, { width }) {
  return Plot.plot({
    title: "Completions vs Yards",
    width,
    color: {scheme: "BrBg"},
    x: {label: "Yards"},
    y: {label: "TDs"},
    marks: [
    Plot.dot(data, {x: "rec_yards", y: "rec_tds", fill:highlight_top_10}),
    Plot.linearRegressionY(data, {x: "rec_yards", y: "rec_tds", stroke: "red"}),
    Plot.tip(data, Plot.pointer({
        x: "rec_yards",
        y: "rec_tds",
        title: receiver_tip,
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
    x: {label: "Target Share"},
    y: {label: "Catch Rate"},
    marks: [
    Plot.dot(data, {x: "target_share", y: "catch_rate", fill:highlight_top_10}),
    Plot.linearRegressionY(data, {x: "target_share", y: "catch_rate", stroke: "red"}),
    Plot.tip(data, Plot.pointer({
        x: "target_share",
        y: "catch_rate",
        title: receiver_tip,
      })),
    Plot.ruleX([d3.median(data, x => x.target_share)], {stroke: "red"}),
     Plot.ruleY([d3.median(data, x => x.catch_rate)], {stroke: "red"}),
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