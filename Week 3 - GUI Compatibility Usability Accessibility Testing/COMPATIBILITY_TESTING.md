# PyTodo Pro · Week 3 compatibility and configuration testing

Playwright ran in headless mode on Ubuntu 24.04.5 LTS x86_64 with device scale factor 1, en-US locale and UTC. Tablet and mobile used touch emulation. Firefox used resized touch-enabled contexts because Playwright Firefox does not support the mobile viewport flag. The matrix reports the version returned by each launched engine. Full configuration and user-agent strings are in [results.json](logs/results.json).

| ID | Procedure | Expected result |
| --- | --- | --- |
| C01 | Register, create Mobile layout sample, open Tasks and measure the layout viewport and document. | Layout viewport equals configured width and there is no document overflow. |
| C02 | From Tasks open Dashboard and measure layout and count summary cards. | Layout viewport equals configured width, the document fits and all five cards are present. |

Each result cell lists measured layout viewport / document width in CSS pixels. Mobile-mode browsers can scale the full page into the configured view even when the layout remains much wider. Screenshots use the configured viewport.

| Configuration | Browser version | Viewport | Profile | C01 · Tasks | C02 · Dashboard |
| --- | --- | --- | --- | --- | --- |
| chromium-desktop | 159.0.8154.6 | 1440 × 900 | Mobile off, touch off | **Pass** · 1440 / 1440 px · [Screenshot](screenshots/compatibility/chromium-desktop-C01.png) | **Pass** · 1440 / 1440 px, 5 cards |
| chromium-tablet | 159.0.8154.6 | 768 × 1024 | Mobile on, touch on | **Fail** · 980 / 980 px · [Screenshot](screenshots/compatibility/chromium-tablet-C01.png) | **Fail** · 980 / 980 px, 5 cards · [Screenshot](screenshots/compatibility/chromium-tablet-C02.png) |
| chromium-mobile | 159.0.8154.6 | 390 × 844 | Mobile on, touch on | **Fail** · 980 / 980 px · [Screenshot](screenshots/compatibility/chromium-mobile-C01.png) | **Fail** · 980 / 980 px, 5 cards · [Screenshot](screenshots/compatibility/chromium-mobile-C02.png) |
| firefox-desktop | 159.0 | 1440 × 900 | Mobile off, touch off | **Pass** · 1440 / 1440 px · [Screenshot](screenshots/compatibility/firefox-desktop-C01.png) | **Pass** · 1440 / 1440 px, 5 cards |
| firefox-tablet | 159.0 | 768 × 1024 | Mobile off, touch on | **Pass** · 768 / 768 px · [Screenshot](screenshots/compatibility/firefox-tablet-C01.png) | **Pass** · 768 / 768 px, 5 cards |
| firefox-mobile | 159.0 | 390 × 844 | Mobile off, touch on | **Fail** · 390 / 563 px · [Screenshot](screenshots/compatibility/firefox-mobile-C01.png) | **Pass** · 390 / 390 px, 5 cards · [Screenshot](screenshots/compatibility/firefox-mobile-C02.png) |
| webkit-desktop | 27.2 | 1440 × 900 | Mobile off, touch off | **Pass** · 1440 / 1440 px · [Screenshot](screenshots/compatibility/webkit-desktop-C01.png) | **Pass** · 1440 / 1440 px, 5 cards |
| webkit-tablet | 27.2 | 768 × 1024 | Mobile on, touch on | **Fail** · 980 / 980 px · [Screenshot](screenshots/compatibility/webkit-tablet-C01.png) | **Fail** · 980 / 980 px, 5 cards · [Screenshot](screenshots/compatibility/webkit-tablet-C02.png) |
| webkit-mobile | 27.2 | 390 × 844 | Mobile on, touch on | **Fail** · 980 / 980 px · [Screenshot](screenshots/compatibility/webkit-mobile-C01.png) | **Fail** · 980 / 980 px, 5 cards · [Screenshot](screenshots/compatibility/webkit-mobile-C02.png) |

The tested pages share a template without viewport metadata. See [D12](DEFECT_REPORT.md#d12). Core GUI execution by profile is in [GUI Testing](GUI_TESTING.md).

## BrowserStack manual verification

| ID | Device / browser | Manual procedure and expectation | Actual result | Status |
| --- | --- | --- | --- | --- |
| C-M01 | Physical iPhone / Safari | Run G01–G11, check date picker and confirm dialog, then compare Tasks and Dashboard in both orientations against C01–C02. | No device session executed. | Not Run |
| C-M02 | Physical Android phone / Chrome | Run G01–G11 using touch and software keyboard. Check text size, Task actions and horizontal scrolling. | No device session executed. | Not Run |
| C-M03 | Physical tablet / Safari or Chrome | Repeat C01–C02 in portrait and landscape and verify task form and touch target usability. | No device session executed. | Not Run |

## Playwright device emulation extension

Executed 2026-11-27T10:48:35.849Z to 2026-11-27T10:49:40.753Z on Ubuntu 24.04.5 LTS x86_64 with Playwright 1.65.1. These were Playwright device descriptors running headless on Linux. Each orientation used its own context with the descriptor’s viewport, user agent, touch and mobile flags, and device scale factor (DPR). The run used en-US, UTC and a fresh isolated SQLite database.

Reused G01–G11 for core GUI workflows and C01–C02 for layout. The workflow scripts use Playwright clicks and fill the date field directly. The run did not exercise physical touch hardware, the OS keyboard, native mobile date pickers, or rotation within an active session.

C01 and C02 show the measured layout viewport width / document width in CSS pixels. The expected result is a layout viewport that matches the configured width and content that fits horizontally. C02 also expects five dashboard cards.

| Emulated device and orientation | Engine | Viewport (CSS px) | DPR | GUI pass | GUI fail | GUI Not Run | C01 · Tasks | C02 · Dashboard |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pixel 7 · Portrait | Chromium 159.0.8154.6 | 412 × 839 | 2.625 | 11 | 0 | 0 | **Fail** · 981 / 981 px · [PNG](screenshots/compatibility/devices/pixel-7-portrait-C01.png) | **Fail** · 981 / 981 px, 5 cards · [PNG](screenshots/compatibility/devices/pixel-7-portrait-C02.png) |
| Pixel 7 · Landscape | Chromium 159.0.8154.6 | 863 × 360 | 2.625 | 11 | 0 | 0 | **Fail** · 981 / 981 px · [PNG](screenshots/compatibility/devices/pixel-7-landscape-C01.png) | **Fail** · 981 / 981 px, 5 cards · [PNG](screenshots/compatibility/devices/pixel-7-landscape-C02.png) |
| Galaxy S24 · Portrait | Chromium 159.0.8154.6 | 360 × 780 | 3 | 11 | 0 | 0 | **Fail** · 980 / 980 px · [PNG](screenshots/compatibility/devices/galaxy-s24-portrait-C01.png) | **Fail** · 980 / 980 px, 5 cards · [PNG](screenshots/compatibility/devices/galaxy-s24-portrait-C02.png) |
| Galaxy S24 · Landscape | Chromium 159.0.8154.6 | 780 × 360 | 3 | 11 | 0 | 0 | **Fail** · 980 / 980 px · [PNG](screenshots/compatibility/devices/galaxy-s24-landscape-C01.png) | **Fail** · 980 / 980 px, 5 cards · [PNG](screenshots/compatibility/devices/galaxy-s24-landscape-C02.png) |
| iPhone 15 · Portrait | WebKit 27.2 | 393 × 659 | 3 | 11 | 0 | 0 | **Fail** · 980 / 980 px · [PNG](screenshots/compatibility/devices/iphone-15-portrait-C01.png) | **Fail** · 980 / 980 px, 5 cards · [PNG](screenshots/compatibility/devices/iphone-15-portrait-C02.png) |
| iPhone 15 · Landscape | WebKit 27.2 | 734 × 343 | 3 | 11 | 0 | 0 | **Fail** · 980 / 980 px · [PNG](screenshots/compatibility/devices/iphone-15-landscape-C01.png) | **Fail** · 980 / 980 px, 5 cards · [PNG](screenshots/compatibility/devices/iphone-15-landscape-C02.png) |
| iPad Pro 11 · Portrait | WebKit 27.2 | 834 × 1194 | 2 | 11 | 0 | 0 | **Fail** · 980 / 980 px · [PNG](screenshots/compatibility/devices/ipad-pro-11-portrait-C01.png) | **Fail** · 980 / 980 px, 5 cards · [PNG](screenshots/compatibility/devices/ipad-pro-11-portrait-C02.png) |
| iPad Pro 11 · Landscape | WebKit 27.2 | 1194 × 834 | 2 | 11 | 0 | 0 | **Pass** · 1194 / 1194 px · [PNG](screenshots/compatibility/devices/ipad-pro-11-landscape-C01.png) | **Pass** · 1194 / 1194 px, 5 cards · [PNG](screenshots/compatibility/devices/ipad-pro-11-landscape-C02.png) |

The existing [responsive layout defect D12](DEFECT_REPORT.md#d12) was retested with the device profiles above. Full user agents, measurements and individual outcomes are in the [device results](logs/devices-results.json) and [execution log](logs/devices-execution.log).

### Physical-device verification

| Original case | Physical hardware and browser | Status | Justification |
| --- | --- | --- | --- |
| C-M01 | iPhone / Safari | Not Run | No physical iPhone session was available in this run. The WebKit descriptor emulates the browser context on Linux. |
| C-M02 | Google Pixel or Samsung Galaxy / Chrome | Not Run | No physical Android phone session was available. Chromium descriptors do not exercise the Android keyboard or physical touch. |
| C-M03 | iPad / Safari or Android tablet / Chrome | Not Run | No physical tablet session was available. Separate orientation contexts exercise layout without testing real rotation or tablet OS controls. |
