---
title: Receivers
toc: true
---

```js
import {sparkbar, gamePointsIndicator} from "./formatHelpers.js";
```


```js
const payload = await FileAttachment("data/players.json").json();
const data = payload.filter(d => d.position === "WR");

const player_game_raw = await FileAttachment("data/plays.json").json();
const player_game = player_game_raw.filter(d => d.position === "WR");
```
```js
// get unique player names
const cat = Array.from(new Set(player_game.map((d) => d.pos_team)));

const color = Plot.scale({
  color: {
    type: "categorical",
    domain: cat,
    unknown: "var(--theme-foreground-muted)",
  },
});
```

```js
function targetShare(data, { width }) {
  return Plot.plot({
    title: "Fantasy Points Week Over Week",
    width,
    height: 300,
    color: { ...color, legend: true },
    marks: [
        Plot.line(data, {
            x: "week",
            y: "target_share",
            z: "player_id",
            stroke: "pos_team"
        }),
    Plot.tip(data, Plot.pointer({
        x: "week",
        y: "target_share",
        title: d => `${d.player_name} \n (${d.game_id} - ${d.rec_targets} targets, ${d.fantasy_points} points)`,
      })),
    Plot.dot(data.filter(d => d.target_share > .4), {
        x: "week",
        y: "target_share",
        fill: 'pos_team',
        radius: 3
      }),
    ],
  });
}
```

```js
function launchTimeline(data, { width }) {
  return Plot.plot({
    title: "Fantasy Points Week Over Week",
    width,
    height: 300,
    // color: { ...color, legend: true },
    marks: [
        Plot.line(data, {
            x: "week",
            y: "fantasy_points",
            z: "player_id",
            color: "pos_team"
        }),
    Plot.tip(data, Plot.pointer({
        x: "week",
        y: "fantasy_points",
        title: d => `${d.player_name} \n (${d.game_id} - ${d.rec_targets} targets, ${d.fantasy_points} points)`,
      })),
    ],
  });
}
```

<div class="grid grid-cols-2">
  <div class="card">
    ${resize((width) => launchTimeline(player_game, {width}))}
  </div>
   <div class="card">
    ${resize((width) => targetShare(player_game, {width}))}
  </div>
</div>

```js
function topTwentyWR(data, { width })
    {
        return Inputs.table(data.sort((a, b) => b.fantasy_points - a.fantasy_points).slice(0, 40), {
            columns: [
                "pos_rank",
                "position",
                "player_name",
                "rec_targets",
                "rec_receptions",
                "rec_td",
                "rec_yards",
                "rush_fantasy_points",
                "fantasy_points",
                "avg_target_share",
                "fp_game_list",
                "target_share_game_list"
            ],
            header: {
                "pos_rank": "Rank",
                "position": "Pos",
                "player_name": "Player",
                "rec_targets": "Tgt",
                "rec_receptions": "Rec",
                "rec_td": "TD",
                "rec_yards": "Yds",
                "rush_fantasy_points": "RuFP",
                "fantasy_points": "FP",
                "avg_target_share": "Tgt Share",
                "fp_game_list": "FP/G",
                "target_share_game_list": "Tgt Share/G"
            },
            format: {
                "fp_game_list": d => d.map(x => `${gamePointsIndicator(x)}`).join(""),
                "fantasy_points": sparkbar(d3.max(data, d => d.fantasy_points)),
                "target_share_game_list": d => d.map(x => _.round(x, 2)),
            },
            align: {
                "fp_game_list": "right"
            },
            rows:50
        })
    }
```

<div class="">
    <p>Top 20 WR</p>
   ${resize((width) => topTwentyWR(data, {width}))}
</div>
