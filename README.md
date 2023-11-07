# The Useless Machine

Implement of a [useless machine](https://youtu.be/mqvh3R8nKSA) as an event-driven web app, which
needs to comply to a fictitious overly bureaucratic process.

## Quick Start

To quickly spool up the application, please use Docker Compose. E.g. on Ubuntu systems:

```shell
sudo apt install docker-compose-v2
docker compose up
```

This will expose a webserver on port 8000 on your host:

```shell
curl http://localhost:8000/switch-1

  {"name":"switch-1","state":"off"}
```

## Business Process

![](http://www.plantuml.com/plantuml/svg/ZP9FIyD04CNlyoc6Uj5316rF4QJz02hu1o-vRBAJRMZSYPj95SJlxaut9g0MF6NvvRsTzuPTzsA232yjv4yzXHnDZ_Gk5Bnf0JfJxOmZt7GTVW1YVbT6qNxKbImN2c-CDsvcbygUEUncj5Iq6MmZFB4LHBXuU6kasYwKdVQ7ynd09y1t1in2TZtzmfEsyPG7ibTwE2-vjPZZ8plN4YOHieT9dmtHhJcFE6zPceeA7xSWyLDjZNS4QaY3jSuHwpsz3jGBIXmUkTEv1tbci-HS_ktKRGRU4nflaOEbKFZvadgi0Ng1vlzV-nW-gGhFTGrZ1Pk2h3Hjnq6cWB-nplg9r-HjV1fV)

An **external operator** can toggle the switch.

Internally, the responsibilities are split up into different roles:

| Role     | Responsibility                                               |
|----------|--------------------------------------------------------------|
| Observer | Observe switch and request counter-measure from **Manager**. |
| Manager  | Can make the decision whether the switch should be toggled.  |
| Worker   | Operates the switch.                                         |
| Auditor  | Keeps a record of the toggling of the switch.                |

## Service Architecture

![](http://www.plantuml.com/plantuml/svg/RPF1JiCm44Jl_ehzWS2zgg9oWXwGIbE9IoNan1jYaTZ6knO7r7ydSLhNAUqjEszsLcDrGomzXw4NZHsSDMWOdfo3Nm7ZprdFMmFlM5Us-K86II2T-w3ubIClXyFkedRCJeYefgNJZklUEqRwqTnqqPiZo_Z4vHSiSwge9s7-X28KCIdDipWeogMMDH6KveENka_YTHINfjiIi3WGrZcI62LPrf8GzgWqYN_NggASfHLKR3qU3R7aG14ytLQxjpscOdDXExWU1pIZLrkJcurb1BOER1ljoVoC1hrkmAFpI1VhX75tfPHkM_HJX1_D10fRRL21DWlCUTiWqKCSe54nTZxWEs10sCkwrlpw9kQXT2wzIFP0IKkTBakExhoyeaoRLx0BTQ-fEvgca-OJIToyudeqP7WLQcgyhiztBYkCS7cFVZoQSv0uYGqQDVsb_W00)
