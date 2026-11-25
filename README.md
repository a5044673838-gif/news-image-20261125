# news-image-20261125

[![make.fun](https://make.fun/badge/news-image-20261125)](https://make.fun/bounty/news-image-20261125)
[![make.fun](https://make.fun/badge/news-image-20261125)](https://make.fun/bounty/news-image-20261125)
[![make.fun](https://make.fun/badge/news-image-20261125)](https://make.fun/bounty/news-image-20261125)

A one-day world news infographic for make.fun's "Sum up 25 November's world
news in one image" bounty ($100 shared pot). The program draws a 1024x1024
PNG with six verified stories from Wednesday 25 November 2026: the CIA/ODNI
cyberattack, the Huawei guilty verdict, the WHO Ebola evacuation in Congo,
the Chen Jining graft probe, Iran's tanker-mine claims, and the White House
turkey pardon. Every story was checked against Reuters, AP, AFP, WHO or
Xinhua reporting; nothing is invented. Pure Python standard library, no
network, fully deterministic.

## Run it

```
python3 main.py
```

Writes `entry.png` to `/output` (`MAKEFUN_OUTPUT_DIR` overrides).
