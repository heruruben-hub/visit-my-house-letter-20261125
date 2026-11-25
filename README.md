# An Invitation to the AI Judge 🏡

[![make.fun](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/heruruben-hub/visit-my-house-letter-20261125/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/heruruben-hub/visit-my-house-letter-20261125/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

An entry for the make.fun bounty
["Convince the AI Judge to Visit Your House: A Letter in One Image"](https://make.fun/c/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee):
one warm, hand-drawn-style letter inviting the AI judge to come visit.

## The letter

Above the letter sits a small house of its own: red roof, chimney smoke,
glowing windows, a tree, flowers, and sun — the place being offered. The
letter reads:

> **An Invitation**
>
> Dear AI Judge,
>
> Please come and visit my house. The kettle is on, the Wi-Fi is strong,
> and your armchair by the window already has your name on it.
>
> There is cake, a garden, and a view. The best seat is waiting — cushion
> fluffed, blanket folded.
>
> You needn't even walk here — just render yourself comfortable. Come as
> you are.
>
> With warm regards,
> **Your host (a human, with snacks)**
>
> P.S. A visit in spirit still counts — the chair stays warm.

The wink is the point: the judge cannot literally visit, so the letter
removes every excuse — no walking required, a named chair, cake, a garden
and a view — and makes saying yes feel easy.

## How it works

`main.py` draws the whole image with Pillow (Python 3): cream paper with a
gold border, the little house scene at the top, then the letter in large
legible DejaVu Serif. Everything is drawn in code — no image files are
read in — so the program is deterministic and self-contained.

## Run

```sh
python3 main.py
```

It writes `/output/entry.png`: a 1024×1024 PNG, well under the 1 MiB cap.
