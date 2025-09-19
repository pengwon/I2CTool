I2CTool UI Prototypes

Files
- i2ctool_prototype.html - Two-tab interactive prototype for general I2C read/write and EEPROM staging workflows.
- i2ctool_prototype.svg - Legacy static snapshot of an earlier layout (kept for comparison).
- ui_flows.md - Flow notes describing layout intent and interaction states.

How to view
1. Open `prototypes/i2ctool_prototype.html` in a desktop browser.
2. Explore the General R/W tab to try the transaction builder, auto poll toggles, and sequence inspector.
3. Switch to the EEPROM Writer tab to review staged jobs, preview payloads, and job settings.
4. Toggle the theme button to compare dark and light tokens, or open the queue preview modal to review payload metadata.

Notes
- All interactions are mocked for demonstration purposes only.
- Use this prototype as the blueprint when implementing PySide6 widgets or a Tauri frontend.
- The SVG snapshot remains available for historical reference and can be regenerated later if needed.
