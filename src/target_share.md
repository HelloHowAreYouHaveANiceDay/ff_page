---
title: Target Share Week Over Week
toc: true
sql:
  player_game: ./data/game_player_2024.parquet
---

# Target Share Week Over Week

Shows week over week target share and pct target share change for players

Target share is calculated as # of targets / total # of targets for the team

```js
const color = Plot.scale({
  color: {
    type: "linear",
    domain: d3.range(-50, 50, 1),
    unknown: "var(--theme-foreground-muted)",
  },
});
```

```js
function pct_bar() {
  return (x) => {
    // convert 2 digit percentage to 0-100
    x = Math.round(x * 100);

    return htl.html`<div style="
        background: RGB(100,${x*2.3+50}, 50);
        color: white;*
        font: 10px/1.6 var(--sans-serif);
        display: block;
        justify-content: end;">${x.toLocaleString("en-US")}`
  }
  
};

function pct_chg_bar() {
  return (x) => {
    // convert 2 digit percentage to 0-100
    x = Math.round(x * 100);
    if (x > 0) {
      return htl.html`<div style="
        background: RGB(100,${x*2.3+50}, 50);
        color: white;*
        font: 10px/1.6 var(--sans-serif);
        display: block;
        justify-content: end;">+${x.toLocaleString("en-US")}`
    } else {
      return htl.html`<div style="
        background: RGB(100,${x*2.3+50}, 50);
        color: white;*
        font: 10px/1.6 var(--sans-serif);
        display: block;
        justify-content: end;">${x.toLocaleString("en-US")}`
    }
  }

};
```

```js
function wow_cols(week_num) {
    const wow = `${week_num}_wow`
    const target_share = `${week_num}_target_share`
    const target_rank = `${week_num}_target_rank`

    const configuration = {
        columns: [
            wow,
            target_share
        ],
        header: {
            [wow]: `${week_num}`,
            [target_share]: "%",
        },
        format: {
            [wow]: pct_chg_bar(),
            [target_share]: pct_bar(),
        },
        align: {
            [wow]: "right",
            [target_share]: "center",
        },
    }

    return configuration
}

function allWeeksCols(){
    const weeks = d3.range(2, 18)
    const config = weeks.map(wow_cols)
    const configuration = {
        columns: config.flatMap(d => d.columns),
        header: config.reduce((a, b) => {
            return { ...a, ...b.header };
        }, {}),
        format: config.reduce((a, b) => {
            return { ...a, ...b.format };
        }, {}),
        align: config.reduce((a, b) => {
            return { ...a, ...b.align };
        }, {}),
    }
    return configuration
}

const allWeeks = allWeeksCols()
console.log(allWeeks)
```

```sql id=game_player_q
PIVOT (
        SELECT 
            *,
        RANK() OVER (PARTITION BY pos_team, week ORDER BY rec_target_share DESC) as target_rank,
        rec_target_share - LAG(rec_target_share) OVER (PARTITION BY player_id ORDER BY week) AS wow,
        FROM 
            player_game
        WHERE
            position IN ('WR', 'TE', 'RB')
)
ON week
USING
    FIRST(rec_target_share) AS target_share, 
    FIRST(target_rank) AS target_rank, 
    FIRST(wow) AS wow
GROUP BY player_id, player_display_name, pos_team
```


```sql id=game_player_weekly_q
SELECT 
    *,
RANK() OVER (PARTITION BY pos_team, week ORDER BY rec_target_share DESC) as target_rank,
rec_target_share - LAG(rec_target_share) OVER (PARTITION BY player_id ORDER BY week) AS wow,
FROM 
    player_game
WHERE
    position IN ('WR', 'TE', 'RB')
    AND pos_team = 'ARI'

```

```js

Inputs.table(
   game_player_q,{
        color: {scheme: "BuRd"},
        columns: [
            "pos_team",
            "player_display_name",
            ...allWeeks.columns
        ],
        header: {
            ...allWeeks.header
        },
        format: {
            ...allWeeks.format
        },
        align: {
            ...allWeeks.align
        },
        width: '100%',
        rows: 20
    }
)

```


```js
function target_share_by_week(data, { width }) {
  return Plot.plot({
    title: "Targets vs. Fantasy Points",
    width,
    height: 300,
    // y: {
    //     type: 'log',
    //     domain: [.1, .8],
    //     grid: true
    // },
    marks: [
      Plot.line(data, {
        x: "week",
        y: "target_rank",
        stroke: "position",
        opacity: 0.6,
      }),
      Plot.tip(data, Plot.pointer({
        x: "week",
        y: "target_rank",
        title: d => `${d.player_name} \n (${d.week} - ${d.rec_targets} targets, ${d.fp} points)`,
      })),
      Plot.ruleY([0]),
    ],
  });
}
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => target_share_by_week(game_player_weekly_q, {width}))}
  </div>
</div>