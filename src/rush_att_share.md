---
title: Rushing Share Week Over Week
toc: true
sql:
  player_game: ./data/game_player_2024.parquet
---

# Week Over Week Rush Share

Shows week over week rushing share and pct rush share change for players

Target share is calculated as # of attempts / total # of attempts for the team

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
        background: RGB(100,${x*1+50}, 50);
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
    const rush_share = `${week_num}_rush_share`
    const rush_rank = `${week_num}_rush_rank`

    const configuration = {
        columns: [
            wow,
            rush_share
        ],
        header: {
            [wow]: `${week_num}`,
            [rush_share]: "%",
        },
        format: {
            [wow]: pct_chg_bar(),
            [rush_share]: pct_bar(),
        },
        align: {
            [wow]: "right",
            [rush_share]: "center",
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

```js

Inputs.table(
    sql`
        PIVOT (
                SELECT 
                    *,
                RANK() OVER (PARTITION BY pos_team, week ORDER BY rush_share DESC) as rush_rank,
                rush_share - LAG(rush_share) OVER (PARTITION BY player_id ORDER BY week) AS wow,
                FROM 
                    player_game
                WHERE
                    position IN ('WR', 'TE', 'RB', 'QB')
        )
        ON week
        USING
            FIRST(rush_share) AS rush_share, 
            FIRST(rush_rank) AS rush_rank, 
            FIRST(wow) AS wow
        GROUP BY player_id, player_display_name, pos_team
    `,{
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
