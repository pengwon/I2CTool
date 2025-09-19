# I2CTool UI Prototype Plan

## Goals
- Focus the desktop layout on two primary flows: ad-hoc I2C read/write and structured EEPROM jobs.
- Surface the controls firmware engineers expect (address width, payload editor, auto poll, retry rules) without leaving the main view.
- Provide inspectors for responses and queued steps so the same markup can guide widget implementation in PySide6 or Tauri.

## Layout Overview
1. Header with mode chips, global search, and theme toggle.
2. Left rail for adapter selection, bus tuning, scan results, and reusable command presets.
3. Center workspace with two tabs:
   - **General R/W**: transaction builder, execution timeline, and result panels.
   - **EEPROM Writer**: staged job list, payload preview, and job options.
4. Right rail for pinned commands, live log feed, and watch values.
5. Footer status bar summarising connection, auto poll state, and queue depth.

## General R/W Flow Highlights
- Form grid exposes adapter, device address, register offset, addressing width, payload format, and loop controls.
- Chip toggles and switches enable stop-on-NACK logic, CRC overrides, and auto polling (with visual state).
- Execution timeline displays ordered steps; selecting one updates the inspector, expected payload, and last-response sample.
- Result panels include a hex/ASCII preview, bitfield interpretation notes, and sequence health summary with quick actions.
- Queue preview modal shows the exact metadata that will be staged when adding a step.

## EEPROM Writer Flow Highlights
- Job list presents page writes, verify sweeps, and custom jobs; the detail card summarises payload source and progress.
- Preview window renders a hex snapshot with diff indicators so engineers can verify the image before flashing.
- Job options section captures queue semantics, write cycle delays, and mismatch policies ready for implementation hooks.

## Follow Ups
- Wire up data binding to backend events once the PySide6 layer is ready.
- Add responsive breakpoints or tablet optimisations if the desktop layout needs to scale down.
- Consider a third automation tab once the general flow ships and user feedback is collected.
