---
title: Target Share
toc: true
sql:
  player_game: ./data/game_player_2024.parquet
---



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
```

```js
Inputs.table(
    sql`
        PIVOT (
                SELECT 
                    *,
                RANK() OVER (PARTITION BY pos_team, week ORDER BY target_share DESC) as target_rank,
                target_share - LAG(target_share) OVER (PARTITION BY player_id ORDER BY week) AS wow,
                FROM 
                    player_game
        )
        ON week
        USING
            FIRST(target_share) AS target_share, 
            FIRST(target_rank) AS target_rank, 
            FIRST(wow) AS wow
        GROUP BY player_id, display_name, pos_team
    `,{
        color: {scheme: "BuRd"},
        columns: [
            "pos_team",
            "display_name",
            "2_wow",
            "2_target_rank",
            "2_target_share",
            "3_wow",
            "3_target_rank",
            "3_target_share",
            "4_wow",
            "5_wow",
            "6_wow",
            "7_wow",
            "8_wow",
            "9_wow",
            "10_wow",
            "11_wow",
            "12_wow",
            "13_wow",
            "14_wow",
            "15_wow",
            "16_wow",
            "17_wow",
        ],
        header: {
            "2_wow": "2",
            "2_target_rank": "r",
            "2_target_share": "%",
            "3_wow": "3",
            "3_target_rank": "r",
            "3_target_share": "%",
            "4_wow": "4",
            "5_wow": "5",
            "6_wow": "6",
            "7_wow": "7",
            "8_wow": "8",
            "9_wow": "9",
            "10_wow": "10",
            "11_wow": "11",
            "12_wow": "12",
            "13_wow": "13",
            "14_wow": "14",
            "15_wow": "15",
            "16_wow": "16",
            "17_wow": "17",
        },
        format: {
            "2_wow": pct_bar(),
            "2_target_share": pct_bar(),
            "3_wow": pct_bar(),
            "3_target_share": pct_bar(),
            "4_wow": pct_bar(),
            "5_wow": pct_bar(),
            "6_wow": pct_bar(),
            "7_wow": pct_bar(),
            "8_wow": pct_bar(),
            "9_wow": pct_bar(),
            "10_wow": pct_bar(),
            "11_wow": pct_bar(),
            "12_wow": pct_bar(),
            "13_wow": pct_bar(),
            "14_wow": pct_bar(),
            "15_wow": pct_bar(),
            "16_wow": pct_bar(),
            "17_wow": pct_bar()
        },
        align: {
            "2_wow": "center",
            "2_target_rank": "center",
            "2_target_share": "center",
            "3_wow": "center",
            "3_target_rank": "center",
            "3_target_share": "center",
        },
        rows: 20
    }
)


```

```sql id=target_share_rank
  PIVOT (
            SELECT 
            *,
            RANK() OVER (PARTITION BY pos_team, week ORDER BY target_share DESC) as target_rank,
            target_share - LAG(target_share) OVER (PARTITION BY player_id ORDER BY week) AS wow,
            FROM 
                player_game
            WHERE target_share > .1
        )
        ON week
        USING
            FIRST(target_share) AS target_share, 
            FIRST(target_rank) AS target_rank, 
            FIRST(wow) AS wow
        GROUP BY player_id, display_name, pos_team
```


<!-- 
```sql id=target_share_rank display
SELECT 
    *,
    RANK() OVER (PARTITION BY pos_team, week ORDER BY target_share DESC) as target_rank
    -- week,
    -- player_id,
    -- target_share,
FROM 
player_game
WHERE target_share > .1
``` -->
<!-- 
```js
Plot.plot({
    marks: [
        Plot.frame(),
        Plot.line(target_share_rank, {
            x: "week",
            y: "target_rank",
            fy: "pos_team",
            z: "player_id",
            stroke: "pos_team"
        }),
    ]
})
``` -->