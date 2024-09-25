---
title: Top 20
toc: true
---

# Top 20

```js
const plays = await FileAttachment("data/players.json").json();
// console.log(plays)
```

```js
import { gamePointsIndicator } from "./formatHelpers.js";

function sparkbar(max) {
  return (x) => htl.html`<div style="
      background: var(--theme-yellow);
      color: black;
      font: 10px/1.6 var(--sans-serif);
      width: ${(100 * x) / max}%;
      float: right;
      padding-right: 3px;
      box-sizing: border-box;
      overflow: visible;
      display: flex;
      justify-content: end;">${x.toLocaleString("en-US")}`;
}

```

```js
function topTwentyOverall(data, { width })
    {
        return Inputs.table(data.sort((a, b) => b.fantasy_points - a.fantasy_points).slice(0, 20), {
            columns: [
                "rank",
                "pos_rank",
                "position",
                "player_name",
                "fantasy_points",
                "fp_game_list",
            ],
            format: {
                "fp_game_list": d => d.map(x => `${gamePointsIndicator(x)}`).join(""),
                "fantasy_points": sparkbar(d3.max(data, d => d.fantasy_points))
            },
            align: {
                "fp_game_list": "right"
            },
            rows:25
        })
    }
```

<div class="">
    <p>Top 20 Overall</p>
   ${resize((width) => topTwentyOverall(plays, {width}))}
</div>


```js
function topTwentyRB(data, { width })
    {
        return Inputs.table(data.sort((a, b) => b.fantasy_points - a.fantasy_points).slice(0, 20), {
            columns: [
                "pos_rank",
                "position",
                "player_name",
                "rush_attempts",
                "rush_yards",
                "rush_td",
                "rec_fantasy_points",
                "fantasy_points",
                "fp_game_list",
            ],
            format: {
                "fp_game_list": d => d.map(x => `${gamePointsIndicator(x)}`).join(""),
                "fantasy_points": sparkbar(d3.max(data, d => d.fantasy_points)),
                "rush_yards": sparkbar(d3.max(data, d => d.rush_yards))
            },
            align: {
                "fp_game_list": "right"
            },
            rows:25
        })
    }
```

<div class="">
    <p>Top 20 RB</p>
   ${resize((width) => topTwentyRB(plays.filter(p => p.position === "RB"), {width}))}
</div>

```js
function topTwentyWR(data, { width })
    {
        return Inputs.table(data.sort((a, b) => b.fantasy_points - a.fantasy_points).slice(0, 20), {
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
            format: {
                "fp_game_list": d => d.map(x => `${gamePointsIndicator(x)}`).join(""),
                "fantasy_points": sparkbar(d3.max(data, d => d.fantasy_points)),
                "target_share_game_list": d => d.map(x => _.round(x, 2)),
            },
            align: {
                "fp_game_list": "right"
            },
            rows:25
        })
    }
```

<div class="">
    <p>Top 20 WR</p>
   ${resize((width) => topTwentyWR(plays.filter(p => p.position === "WR"), {width}))}
</div>

```js
function topTwentyQB(data, { width })
    {
        return Inputs.table(data.sort((a, b) => b.fantasy_points - a.fantasy_points).slice(0, 20), {
            columns: [
                "pos_rank",
                "player_name",
                "position",
                "pass_attempts",
                "pass_complete",
                "pass_tds",
                "rush_fantasy_points",
                "fantasy_points",
                "fp_game_list"
            ],
            format: {
                "fp_game_list": d => d.map(x => `${gamePointsIndicator(x)}`).join(""),
                "fantasy_points": sparkbar(d3.max(data, d => d.fantasy_points))
            },
            align: {
                "fp_game_list": "right"
            },
            rows:25
        })
    }
```

<div class="">
    <p>Top 20 QB</p>
   ${resize((width) => topTwentyQB(plays.filter(p => p.position === "QB"), {width}))}
</div>