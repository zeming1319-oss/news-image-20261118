#!/usr/bin/env python3
import hashlib
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
PADDING = 40
CARD_H_PADDING = 24
CARD_V_PADDING = 16
ITEM_SPACING = 28
FOOTER_HEIGHT = 70
ACCENT_COLOR = (0, 102, 204)
DARK_BG = (15, 23, 42)
LIGHT_BG = (248, 250, 252)
TEXT_DARK = (15, 23, 42)
TEXT_LIGHT = (248, 250, 252)
TEXT_MUTED = (100, 116, 139)
CARD_BG = (255, 255, 255)
BORDER_COLOR = (226, 232, 240)
LINE_SPACING = 6

NEWS_ITEMS = [
    "Middle East: US strikes on Iran's Qeshm Island raise Gulf tensions; Kuwait and Bahrain on alert after hostile drone attacks and air-defence interceptions near the Strait of Hormuz.",
    "Iran attacks Kuwait's Ali Al Salem Air Base and Bahrain, expanding targets while striking shipping in the Strait of Hormuz; US moves a third carrier strike group (USS Theodore Roosevelt) into the region.",
    "Yemen: Saudi-led coalition launches a major air attack across Houthi-held territory, saying 60 military targets were destroyed; Houthis report at least 17 killed.",
    "Shenzhen, China: Xi Jinping and Vladimir Putin hold talks ahead of Thursday's historic trilateral summit with Donald Trump; fears the three leaders could decide Ukraine's fate over Kyiv's and Europe's heads.",
    "Xi Jinping greets Trump on arrival in Shenzhen and calls at APEC for an open Asia-Pacific economy with deeper cooperation in AI and digital trade.",
    "India: PM Modi returns to New Delhi after attending the ASEAN Summit in Manila.",
    "US: Trump says he takes \"very seriously\" reports of an alleged Iranian \"dirty bomb\" plot; Tehran dismisses the report as \"Iraq War-style propaganda\".",
]

FOOTER_TEXT = "Compiled from AP, Reuters, WSJ, The Hindu, NYT, TOI — Nov 18, 2026"


def get_font(size, bold=False):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def measure_text(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def main():
    title_font = get_font(36, bold=True)
    item_font = get_font(20)
    number_font = get_font(22, bold=True)
    footer_font = get_font(16)

    temp_img = Image.new("RGB", (WIDTH, 100), LIGHT_BG)
    draw = ImageDraw.Draw(temp_img)

    max_content_width = WIDTH - 2 * PADDING
    title_lines = wrap_text(draw, "World News — November 18, 2026", title_font, max_content_width)
    title_height = sum(measure_text(draw, line, title_font)[1] for line in title_lines) + (len(title_lines) - 1) * LINE_SPACING

    item_heights = []
    item_lines_cache = []
    for idx, item in enumerate(NEWS_ITEMS):
        num_text = f"{idx + 1}."
        num_w, num_h = measure_text(draw, num_text, number_font)
        text_x = PADDING + CARD_H_PADDING + num_w + 12
        text_max_width = (WIDTH - PADDING - CARD_H_PADDING) - text_x
        item_lines = wrap_text(draw, item, item_font, text_max_width)
        item_lines_cache.append(item_lines)
        line_heights = [measure_text(draw, line, item_font)[1] for line in item_lines]
        text_block_h = sum(line_heights) + (len(line_heights) - 1) * LINE_SPACING
        total_h = max(num_h, text_block_h) + 2 * CARD_V_PADDING
        item_heights.append(total_h)

    header_end = PADDING + title_height + 16
    y_start = header_end + PADDING
    total_height = y_start + sum(item_heights) + ITEM_SPACING * (len(NEWS_ITEMS) - 1) + FOOTER_HEIGHT

    img = Image.new("RGB", (WIDTH, total_height), LIGHT_BG)
    draw = ImageDraw.Draw(img)

    y = PADDING
    for line in title_lines:
        w, h = measure_text(draw, line, title_font)
        draw.text(((WIDTH - w) // 2, y), line, font=title_font, fill=TEXT_LIGHT)
        y += h + LINE_SPACING

    header_end = y + 16
    draw.rectangle([0, 0, WIDTH, header_end], fill=DARK_BG)
    y = PADDING
    for line in title_lines:
        w, h = measure_text(draw, line, title_font)
        draw.text(((WIDTH - w) // 2, y), line, font=title_font, fill=TEXT_LIGHT)
        y += h + LINE_SPACING

    y = header_end + PADDING
    for idx, item in enumerate(NEWS_ITEMS):
        card_top = y
        num_text = f"{idx + 1}."
        num_w, num_h = measure_text(draw, num_text, number_font)
        item_lines = item_lines_cache[idx]

        card_height = item_heights[idx]
        draw.rectangle(
            [PADDING, card_top, WIDTH - PADDING, card_top + card_height],
            fill=CARD_BG,
            outline=BORDER_COLOR,
            width=1,
        )

        draw.text((PADDING + CARD_H_PADDING, card_top + CARD_V_PADDING), num_text, font=number_font, fill=ACCENT_COLOR)

        text_x = PADDING + CARD_H_PADDING + num_w + 12
        text_y = card_top + CARD_V_PADDING
        for line in item_lines:
            draw.text((text_x, text_y), line, font=item_font, fill=TEXT_DARK)
            _, lh = measure_text(draw, line, item_font)
            text_y += lh + LINE_SPACING

        y = card_top + card_height + ITEM_SPACING

    footer_y = total_height - FOOTER_HEIGHT
    draw.rectangle([0, footer_y, WIDTH, total_height], fill=DARK_BG)
    fw, fh = measure_text(draw, FOOTER_TEXT, footer_font)
    draw.text(
        ((WIDTH - fw) // 2, footer_y + (FOOTER_HEIGHT - fh) // 2),
        FOOTER_TEXT,
        font=footer_font,
        fill=TEXT_MUTED,
    )

    img.save("news.png", "PNG", optimize=True)
    return 0


if __name__ == "__main__":
    exit(main())