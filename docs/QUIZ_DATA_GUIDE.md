# Quiz Data Bulk Entry Guide

## Overview
This guide explains how to add quiz data for the 106 hardware images in the catalog efficiently.

## Images by Category & Priority

### High Priority (Core 1 Essentials) - 28 images
These topics are heavily tested on CompTIA A+ Core 1:

**1. Cables & Connectors (17 images)**
- atx_24_pin_power_cable.png
- coaxial_rg6_cable.png
- displayport_cable.png
- dvi_d_cable.png
- eps_8_pin_cpu_power_cable.png
- fiber_optic_patch_lc_to_sc_cable.png
- hdmi_cable.png
- molex_power_cable.png
- pcie_gpu_power_cable.png
- rj_11_phone_cable.png
- rj_45_cable.png
- sata_data_cable.png
- usb_a_cable.png
- usb_a_to_micro_usb_cable.png
- usb_a_to_usb_b_cable.png
- usb_c_cable.png
- vga_cable.png

**2. RAM & Memory (4 images)**
- ddrsodimm_installation.png
- ... (others)

**3. Power Supplies (7 images)**

### Medium Priority (Core 1 Coverage) - 38 images
- CPUs & Sockets (5)
- Storage (7)
- Display (7)
- Expansion Cards (9)
- Cooling (5)

### Lower Priority (Optional/Core 2) - 40 images
- Printers (13)
- Networking (7)
- Tools (7)
- Mobile/Laptop (5)
- Motherboards (8 - board diagrams, may use as diagrams not quizzes)

## Template for Quiz Entry

```json
{
  "id": "cable_usb_c",
  "category": "cables",
  "file": "usb_c_cable.png",
  "name": "USB-C Cable",
  "objectives": ["Core 1 - 1.3 Connectors"],
  "quiz": {
	"options": [
	  "USB 3.0 Type-A",
	  "USB-C (USB 3.1)",
	  "Micro USB",
	  "DisplayPort"
	],
	"correct_index": 1,
	"explanation": "USB-C is the reversible, flat connector that supports high power and fast data transfer (up to 40 Gbps on USB 3.1)."
  }
}
```

## Quiz Option Strategy

Each wrong answer should progress in difficulty:
1. **Option 0 (Wrong)**: Related connector/cable (similar category)
2. **Option 1 (Correct)**: The correct answer
3. **Option 2 (Wrong)**: Common confusion or similar-looking component
4. **Option 3 (Wrong)**: Plausible but very different

For example - USB-C cable:
- USB 3.0 Type-A (same connector family, different type)
- **USB-C (correct)** ← The right answer
- Micro USB (similar size, wrong type)
- DisplayPort (different connector entirely)

## Priority Workflow

### Stage 1: High Priority (Core 1 Essential)
**Target**: Complete cables, RAM, CPUs, power, storage
**Effort**: 36 entries
**Time**: 1-2 hours

Focus on these because they appear most on A+ exams.

### Stage 2: Medium Priority (Expanded Coverage)
**Target**: Displays, expansion cards, cooling
**Effort**: 21 entries
**Time**: 1 hour

### Stage 3: Lower Priority (Completeness)
**Target**: Printers, networking, tools, mobile
**Effort**: 32 entries
**Time**: 1.5 hours

### Stage 4: Diagrams (Reference Only)
**Target**: Motherboard diagrams, cross-sections
**Action**: Set `"quiz": null` to exclude from gameplay
**Purpose**: Keep for study notes reference

## Adding Entries

### Option A: Manual Entry
1. Open `data/image_catalog.json`
2. Add new entry to `"images"` array
3. Fill in all required fields
4. Test by running game and verifying image loads

### Option B: Bulk CSV → JSON Conversion
Create a CSV with columns:
- id | category | file | name | correct_option | wrong1 | wrong2 | wrong3 | explanation

Then use the conversion script to:
1. Parse CSV
2. Randomize option order
3. Generate JSON entries

### Option C: Incremental Population
1. Start with one category
2. Add 5-10 entries
3. Test in game
4. Move to next category

## Example Entries by Category

### Cables (High Priority)
```
USB-C Cable → (reversible connector, high power, 40 Gbps)
HDMI Cable → (video with audio, consumer electronics)
DisplayPort → (video, high bandwidth, daisy-chaining)
Fiber Optic (LC) → (light-based, long distance, high-speed)
RG-6 Coaxial → (cable TV, satellite, RF shielding)
Cat 6A Ethernet → (10 Gbps, twisted pair, EMI protection)
```

### RAM (High Priority)
```
SODIMM → (laptop/portable memory)
UDIMM → (standard desktop RAM)
RDIMM → (server memory, register)
DDR4 3600 MHz → (speed, generation)
```

### CPUs (Medium Priority)
```
Intel LGA 1700 (socket)
AMD Ryzen 5000 series
Apple M1/M2
heat sink and thermal paste mounting
```

### Power Supplies (High Priority)
```
ATX 24-pin (motherboard power)
EPS 8-pin (CPU additional power)
PCIe 6-pin (GPU power)
Molex 4-pin (legacy devices)
SATA power (modern drives)
```

## Quick Reference: Common Wrong Answers

**For Cable Questions:**
- Connector: RJ-45, RJ-11, USB-A, USB-C, DisplayPort, HDMI, DVI, VGA
- Power: ATX 24-pin, EPS 8-pin, 6-pin, 4-pin, Molex
- Data: Cat5e, Cat6, Cat6a, Fiber, Coax
- Video: HDMI, DisplayPort, DVI, VGA

**For RAM Questions:**
- Types: SODIMM, UDIMM, RDIMM, LRDIMM
- Speeds: DDR3 1600, DDR4 3200, DDR4 3600, DDR5 6000
- Form factors: 168-pin, 184-pin, 240-pin, 260-pin

**For CPU Questions:**
- Intel Sockets: LGA 1150, LGA 1151, LGA 1700, LGA 2011
- AMD Sockets: AM4, AM5, TRX4
- Brands: Intel, AMD, Apple Silicon, ARM

## Validation Checklist

Before submitting quiz entry:
- [ ] Image file exists in correct category folder
- [ ] ID is unique and descriptive (snake_case)
- [ ] Category key matches categories list
- [ ] Exactly 4 options provided
- [ ] correct_index is 0-3
- [ ] All options are distinct and plausible
- [ ] Explanation is clear and informative
- [ ] JSON is valid (test with JSONLint)

## Testing After Addition

```bash
# Run the game and verify:
1. Category appears in dropdown
2. Image loads without errors
3. Options display correctly
4. Correct answer is validated
5. Explanation appears on selection
```

## File Size & Performance

- Current catalog: ~89 lines
- Target catalog: ~400-500 lines (106 entries)
- Performance: Negligible (fast JSON parse, ~10ms)
- No optimization needed

## Next Steps

1. Start with cables (17 images)
2. Add RAM, CPU, Power (16 images)
3. Complete storage, cooling, expansion (21 images)
4. Add optional categories

---

**Estimated Total Time**: 3-4 hours for high + medium priority
**Recommended Approach**: Do one category per session

