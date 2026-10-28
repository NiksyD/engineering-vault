---
title: PasaCPA Frontend Design & UI Architecture
category: Design System & UX
status: Active
priority: P0
created: 2026-10-28
platform: Flutter (Mobile)
style: Utility Neo-Brutalism
---

# 🎨 PasaCPA: Frontend Design & UI Architecture

## 1. Design Philosophy: "Utility Neo-Brutalism"

**PasaCPA** avoids the generic, soft, pastel aesthetic of consumer language apps. The Philippine CPA Board Examination is a high-stakes, 3-day professional endurance trial with a 75% national mortality rate. The interface must respect the gravity of the examination.

**Utility Neo-Brutalism (The Casio / Warm Ledger Hybrid)** evokes the physical tools of the accounting profession:
- Casio JW-200SC desktop calculators
- Columnar pads and double-entry general ledgers
- Physical law codals and SEC filings
- Official PRC board examination answer sheets

### Core Structural Rules:
1. **0px Border Radius Everywhere:** Buttons, cards, modals, text inputs, and bottom sheets use pure rectangular geometry (`borderRadius: BorderRadius.zero`).
2. **2px Solid Borders:** Clean, uncompromising boundary separation (`border: Border.all(color: AppColors.frameBlack, width: 2)`).
3. **Hard Offset Drop Shadows (Zero Blur):** Perpendicular depth without soft Gaussian gradients (`BoxShadow(offset: Offset(2, 2), blurRadius: 0, spreadRadius: 0)`).
4. **Tactile Micro-Press Feedback:** Buttons physically shift down and right by `(2px, 2px)` on touch, flattening the shadow to provide instant haptic and visual confirmation under time pressure.

---

## 2. Color Tokens & Semantic Palette

To prevent ocular fatigue during 8-hour daily review sessions, PasaCPA uses a **warm newsprint canvas** rather than clinical, blinding `#FFFFFF`.

### Light Mode (The Warm Ledger)

| Token | Hex Value | Semantic Usage |
| :--- | :--- | :--- |
| `canvasPaper` | `#FAF9F6` | Master screen background (warm, eye-friendly off-white) |
| `frameBlack` | `#1A1C1A` | Primary text, borders, high-contrast headings |
| `surfaceWhite` | `#FFFFFF` | Card backgrounds, elevated problem containers |
| `bufferGray` | `#EFEEEB` | Table headers, neutral badges, inactive tabs |
| `voltGreen` | `#00E676` | Correct answers, active on-device AI, passing scores |
| `radicalOrange` | `#FF3D00` | Wrong answers, Ebbinghaus decay alert, time-trap warnings |
| `accentGold` | `#FFD600` | Flagged items for review, milestone badges |

### Dark Mode (Inverted Brutalism)

| Token | Hex Value | Semantic Usage |
| :--- | :--- | :--- |
| `canvasPaper` | `#121312` | Deep charcoal matte background |
| `frameBlack` | `#E0E0E0` | High-contrast borders, active primary text |
| `surfaceWhite` | `#1E201E` | Elevated cards and problem containers |
| `bufferGray` | `#2A2D2A` | Table headers, secondary surfaces |
| `voltGreen` | `#00E676` | Unaltered neon green for maximum legibility |
| `radicalOrange` | `#FF3D00` | Unaltered radical orange alert |

> **Accessibility Rule:** Color is never used as the sole indicator of state. Correct/incorrect options always feature bold supporting glyphs (`check_circle` vs `cancel`) alongside color changes to ensure WCAG AAA accessibility for colorblind candidates.

---

## 3. Typography System: The Tri-Font Architecture

```
┌────────────────────────────────────────────────────────┐
│ 1. ANTON (Display / Headline)                          │
│    - Used for: Subject titles, exam timers, badges     │
│    - Style: Heavy condensed display, uppercase         │
├────────────────────────────────────────────────────────┤
│ 2. SPACE MONO (Numbers & Telemetry)                    │
│    - Used for: Balance sheets, tax tables, latency     │
│    - Style: Monospaced, vertically aligned decimals    │
├────────────────────────────────────────────────────────┤
│ 3. GEIST / INTER (Body & Case Studies)                 │
│    - Used for: Case prompts, legal text, explanations  │
│    - Style: Highly legible sans-serif, 1.5 line height │
└────────────────────────────────────────────────────────┘
```

### Type Scale (Mobile Standard)

```dart
static const TextTheme textTheme = TextTheme(
  // Anton Display
  displayLarge: TextStyle(fontFamily: 'Anton', fontSize: 32, letterSpacing: 1.0, color: AppColors.frameBlack),
  displayMedium: TextStyle(fontFamily: 'Anton', fontSize: 24, letterSpacing: 0.8, color: AppColors.frameBlack),
  displaySmall: TextStyle(fontFamily: 'Anton', fontSize: 20, letterSpacing: 0.5, color: AppColors.frameBlack),

  // Space Mono (Data / Financials)
  labelLarge: TextStyle(fontFamily: 'SpaceMono', fontSize: 15, fontWeight: FontWeight.bold, color: AppColors.frameBlack),
  labelMedium: TextStyle(fontFamily: 'SpaceMono', fontSize: 13, fontWeight: FontWeight.bold, color: AppColors.frameBlack),
  labelSmall: TextStyle(fontFamily: 'SpaceMono', fontSize: 11, fontWeight: FontWeight.w400, color: AppColors.frameBlack),

  // Geist (Reading & Body)
  bodyLarge: TextStyle(fontFamily: 'Geist', fontSize: 16, height: 1.5, color: AppColors.frameBlack),
  bodyMedium: TextStyle(fontFamily: 'Geist', fontSize: 14, height: 1.4, color: AppColors.frameBlack),
  bodySmall: TextStyle(fontFamily: 'Geist', fontSize: 12, height: 1.3, color: AppColors.frameBlack),
);
```

---

## 4. Reusable Flutter Component Recipes

### A. The Tactile Brutalist Button
```dart
class BrutalistButton extends StatefulWidget {
  final VoidCallback onPressed;
  final Widget child;
  final Color backgroundColor;
  final double shadowOffset;

  const BrutalistButton({
    super.key,
    required this.onPressed,
    required this.child,
    this.backgroundColor = AppColors.surfaceWhite,
    this.shadowOffset = 3.0,
  });

  @override
  State<BrutalistButton> createState() => _BrutalistButtonState();
}

class _BrutalistButtonState extends State<BrutalistButton> {
  bool _isPressed = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => setState(() => _isPressed = true),
      onTapUp: (_) => setState(() => _isPressed = false),
      onTapCancel: () => setState(() => _isPressed = false),
      onTap: widget.onPressed,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 40),
        transform: Matrix4.translationValues(
          _isPressed ? widget.shadowOffset : 0,
          _isPressed ? widget.shadowOffset : 0,
          0,
        ),
        decoration: BoxDecoration(
          color: widget.backgroundColor,
          border: Border.all(color: AppColors.frameBlack, width: 2),
          boxShadow: _isPressed
              ? []
              : [
                  BoxShadow(
                    color: AppColors.frameBlack,
                    offset: Offset(widget.shadowOffset, widget.shadowOffset),
                    blurRadius: 0,
                  ),
                ],
        ),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: widget.child,
      ),
    );
  }
}
```

### B. The MCQ Option Card (With Strikethrough Support)
```dart
enum McqCardState { neutral, selected, correct, incorrect }

class McqOptionCard extends StatelessWidget {
  final String optionLetter; // "A", "B", "C", "D"
  final String optionText;
  final McqCardState state;
  final bool isEliminated;
  final VoidCallback onTap;
  final VoidCallback onLongPress; // Triggers strikethrough

  const McqOptionCard({
    super.key,
    required this.optionLetter,
    required this.optionText,
    required this.state,
    required this.isEliminated,
    required this.onTap,
    required this.onLongPress,
  });

  @override
  Widget build(BuildContext context) {
    Color bgColor = AppColors.surfaceWhite;
    Color textColor = AppColors.frameBlack;
    Widget? trailingIcon;

    if (state == McqCardState.correct) {
      bgColor = AppColors.voltGreen;
      trailingIcon = const Icon(Icons.check_circle, color: AppColors.frameBlack);
    } else if (state == McqCardState.incorrect) {
      bgColor = AppColors.radicalOrange;
      textColor = Colors.white;
      trailingIcon = const Icon(Icons.cancel, color: Colors.white);
    } else if (state == McqCardState.selected) {
      bgColor = AppColors.bufferGray;
    }

    return GestureDetector(
      onTap: isEliminated ? null : onTap,
      onLongPress: onLongPress,
      child: Opacity(
        opacity: isEliminated ? 0.35 : 1.0,
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 4),
          decoration: BoxDecoration(
            color: bgColor,
            border: Border.all(color: AppColors.frameBlack, width: 2),
            boxShadow: const [
              BoxShadow(color: AppColors.frameBlack, offset: Offset(2, 2), blurRadius: 0),
            ],
          ),
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              Container(
                width: 28,
                height: 28,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: AppColors.frameBlack,
                  border: Border.all(color: AppColors.frameBlack),
                ),
                child: Text(
                  optionLetter,
                  style: const TextStyle(fontFamily: 'SpaceMono', color: Colors.white, fontWeight: FontWeight.bold),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  optionText,
                  style: TextStyle(
                    fontFamily: 'Geist',
                    fontSize: 14,
                    color: textColor,
                    fontWeight: FontWeight.w600,
                    decoration: isEliminated ? TextDecoration.lineThrough : null,
                  ),
                ),
              ),
              if (trailingIcon != null) trailingIcon,
            ],
          ),
        ),
      ),
    );
  }
}
```

---

## 5. Mobile Ergonomics & Screen Topology

### A. The 70-Item Mobile Pacing Layout
On mobile screens (360px–420px width), cramming a 400-word accounting problem narrative alongside 4 MCQ choices causes severe scrolling fatigue.

**The Solution: Unified Split-Screen Architecture:**
- **Top 45% (Pinned Case Area):** Master Case narrative with scrollable financial statement ledger table. Features quick-jump chips for grouped caselets (e.g., `[ Item 18 ] [ Item 19 ] [ Item 20 ]`).
- **Bottom 55% (Active Question & Options):** The specific sub-question prompt, 4 choices, and bottom action bar.
- **Floating Action Strip:** Docked at the bottom:
  - `[ 📐 Scratchpad ]` (Pulls up Casio Calculator / T-Account)
  - `[ 🏷️ L1 / L2 / L3 Triage ]` (Quick difficulty tagging)
  - `[ 🚩 Flag ]` (Mark for review)
  - `[ Next Item ➔ ]`

### B. Persistent 4-Tab Bottom Navigation
To eliminate clutter, the bottom navigation bar contains exactly 4 high-value destinations:

1. **EXAM (Assignment Icon):** Active mock exam, 3-day board simulation, and practice drills.
2. **STUDY HUB (Menu Book Icon):** Syllabi breakdown across the 6 subjects and the **Codal & Tax Quick-Vault**.
3. **CARDS (Style Icon):** Spaced-repetition active-recall flashcard deck with 3D flip card interactions.
4. **ANALYTICS (Monitoring Icon):** Mastery percentages, Ebbinghaus decay index, and BOA Conditioned status alerts.

---

## 6. Implementation File Layout in Flutter

All design tokens are placed in `lib/core/theme/`:

```text
lib/core/theme/
├── app_colors.dart         # Static hex definitions (Light & Dark)
├── app_typography.dart     # Anton, Space Mono, Geist text themes
├── app_theme.dart          # Master ThemeData builder
└── widgets/                # Neo-brutalist atomic components
    ├── brutalist_button.dart
    ├── brutalist_card.dart
    ├── mcq_option_card.dart
    └── status_badge.dart
```

