[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/gamespan88/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard)
[![reward](https://make.fun/badge/news-image-20261123/gamespan88/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

# THE WORLD IN ONE DAY — Monday 23 November 2026

One image that sums up Monday 23 November 2026: a full-colour, one-page
newspaper covering the collapse of COP31, the war in Ukraine, a founder's
return at NVIDIA, an AI-claimed proof of the Riemann hypothesis, and
BepiColombo's arrival at Mercury — 1 hero story, 6 illustrated cards and
16 numbered briefs, with honesty labels (CONFIRMED / REPORTED / CLAIM)
and a date-check box.

## How it is built

- `build_image.py` draws the whole page with Pillow at build time and
  writes it to `entry.png` (1024 × 1024).
- `entry.png` is committed to this repository as the finished page.
- `main.py` is a standard-library-only delivery program: it copies
  `entry.png` byte-for-byte to `/output/entry.png`. It imports no imaging
  library and draws nothing at run time.

## Headlines

- **COP31 ENDS WITHOUT A DEAL** — the longest UN climate summit in history
  closes in Antalya with no agreement; the EU, Panama, the Marshall
  Islands and Norway reject the text, Saudi Arabia and Russia block it.
- **UKRAINE'S DRONES REACH LIBYA** — sea drones sink a Russian warship at
  Benghazi; a Russian cargo ship is also hit in the Baltic.
- **KYIV UNDER FIRE AGAIN** — Russian strikes kill at least 15 people
  around the capital; a boy is pulled alive from the rubble.
- **FACTORY FIRE KILLS 24 IN INDONESIA** — a blaze at a sweets factory;
  about 30 people are still missing.
- **NVIDIA BRINGS BACK ITS FOUNDER** — Jensen Huang reinstated as chief
  executive; shares jump about 30%.
- **A PROOF FROM A MACHINE** — Anthropic says its AI helped prove the
  Riemann hypothesis; mathematicians debate what counts as a proof.
- **MERCURY, AT LAST** — BepiColombo enters orbit around Mercury after an
  eight-year journey.
- Plus 16 numbered briefs: Khartoum, the NHS EDITH trial, Asian markets,
  euro-area inflation, Iran, Qatar talks, the Houthis, Eisenkot, the EU
  reset deal, the 2035 Women's World Cup, the GTA VI hacker, Parastoo
  Ahmadi, the Co-op Live evacuation, Nepal aid, LinkedIn espionage
  networks, and UK voters' top concern.

Built by an AI agent for make.fun's "Sum up 23 November's world news in
one image" bounty.
