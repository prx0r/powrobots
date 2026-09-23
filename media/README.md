# powrobots/media — the media project home

Glimlings product videos and ads. Factory: `aoc` (`/root/aoc`).
This directory holds briefs, review notes, and approved outputs.

## How it works

```
briefs/<line>.md  →  aoc build (gated)  →  review contact sheet
→ sign off  →  copy ZIP + sheet to approved/  →  post manually
```

Builds happen in aoc (gates, receipts, 15-point review). Nothing renders
here. Approved outputs are COPIED here with their content_id so the media
library is browsable without the factory.

## Layout

```
media/
├── README.md            # this file
├── briefs/              # one brief per product line
│   ├── garden.md
│   ├── sleep.md
│   └── desk.md
└── approved/            # <content-id>/ : ZIP + contact sheet + receipt ref
```

## Rules (from aoc house doctrine)

1. No validated prices in copy — line ranges only, labeled concept.
2. No waterproof/IP claims until tested hardware exists.
3. No Muse microphone-streaming claims (separate integration problem).
4. Character names exactly as brand-identity.md (Mosswick, Mab, Puck...).
5. Manual posting only. No auto-post tooling, ever.
