#!/usr/bin/env python3

# Turn the display off

import ST7789

# Create the display object
disp = ST7789.ST7789(
    port=1,
    cs=ST7789.BG_SPI_CS_BACK,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=26,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000,
)

disp.set_backlight(0)

