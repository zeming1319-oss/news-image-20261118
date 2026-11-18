# SPEC: news-image-20261118

Build a program that generates an infographic PNG summarizing the world news of 18 November 2026.

## Requirements

- Entry point: `main.py`, runnable with `python3 main.py`, must exit with code 0.
- Output file: `news.png`, generated with Pillow (PIL). Size: 1200 pixels wide, height chosen to fit content.
- Output must be **deterministic**: two consecutive runs produce byte-identical PNG files. No wall-clock time, no randomness (or seeded), no network calls, no unordered iteration affecting output.
- No external assets or fonts fetched at runtime; use Pillow's default fonts or fixed local resources only.
- `python3 main.py` should regenerate `news.png` fresh each run.

## Content: news items for 18 November 2026 (data list to render)

Title: "World News — November 18, 2026"

1. Middle East: US strikes on Iran's Qeshm Island raise Gulf tensions; Kuwait and Bahrain on alert after hostile drone attacks and air-defence interceptions near the Strait of Hormuz.
2. Iran attacks Kuwait's Ali Al Salem Air Base and Bahrain, expanding targets while striking shipping in the Strait of Hormuz; US moves a third carrier strike group (USS Theodore Roosevelt) into the region.
3. Yemen: Saudi-led coalition launches a major air attack across Houthi-held territory, saying 60 military targets were destroyed; Houthis report at least 17 killed.
4. Shenzhen, China: Xi Jinping and Vladimir Putin hold talks ahead of Thursday's historic trilateral summit with Donald Trump; fears the three leaders could decide Ukraine's fate over Kyiv's and Europe's heads.
5. Xi Jinping greets Trump on arrival in Shenzhen and calls at APEC for an open Asia-Pacific economy with deeper cooperation in AI and digital trade.
6. India: PM Modi returns to New Delhi after attending the ASEAN Summit in Manila.
7. US: Trump says he takes "very seriously" reports of an alleged Iranian "dirty bomb" plot; Tehran dismisses the report as "Iraq War-style propaganda".

## Design guidance

- Clean infographic layout: header band with the title, one row/card per news item (numbered), a footer with a data-source note ("Compiled from AP, Reuters, WSJ, The Hindu, NYT, TOI — Nov 18, 2026").
- Use a restrained palette (e.g., dark header, light body, one accent color), wrapped text lines, consistent spacing.
- Keep the layout logic simple and fully deterministic (fixed item order as listed above).

## Verification expected

- Run `python3 main.py` twice and confirm `news.png` is byte-identical across runs (e.g., via sha256).
- Confirm the image is 1200 px wide, PNG format, and that all 7 news items appear.
