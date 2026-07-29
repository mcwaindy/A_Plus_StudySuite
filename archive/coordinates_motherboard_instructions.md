markdown_content = """# 🛠️ Motherboard Hotspot Coordinate Picker & JSON Guide

This guide explains how to use the built-in **Coordinate Picker** tool inside `DiagramView` to quickly generate pixel-accurate bounding box coordinates for any motherboard component.

---

## 🚀 How to Use the Coordinate Picker

The Coordinate Picker translates mouse click-and-drag selections on the scaled GUI canvas into native `908×871` image pixel coordinates automatically.

### Step-by-Step Instructions

1. **Launch the Application:**
   - Run `main.py` and select **1.c Motherboard Diagram** from the sidebar.

2. **Enable Picker Mode:**
   - Ensure the **Coordinate Picker** toggle switch in the top header is switched **ON** (a message `🔧 Coordinate Picker Mode: ENABLED` will print to the console).

3. **Select a Component:**
   - Position your mouse over the **top-left corner** of a motherboard component (e.g., LGA 1700 CPU Socket).
   - **Left-click and drag** across to the **bottom-right corner** of the component.
   - A red dashed bounding box will outline your selection in real time.

4. **Copy the Output:**
   - Release the mouse button. The terminal/console will print the exact formatted `coords` array:
     ```text
     🎯 --- NEW HOTSPOT COORDINATES ---
     "coords": [312, 185, 520, 395]
     ------------------------------------
     ```

5. **Paste into JSON:**
   - Copy the generated `[x1, y1, x2, y2]` array directly into the target component inside `data/motherboard/motherboard_nodes.json`.

6. **Test the Selection:**
   - Toggle the **Coordinate Picker** switch **OFF**.
   - Left-click your newly mapped area to verify the highlight box aligns cleanly and populates the right-hand details panel.

---

## 📓 Bounding Box Mapping Schema (`data/motherboard/motherboard_nodes.json`)

Below is the structured JSON template for `modern_atx`. As you map new components using the picker, replace the placeholder `coords` with your actual console outputs:

```json
{
  "modern_atx": {
    "title": "Modern Workstation / ATX Board",
    "image_path": "assets/images/motherboard/modern_eatx_908x871.png",
    "resolution": [908, 871],
    "components": [
      {
        "id": "cpu_socket",
        "name": "LGA 1700 CPU Socket",
        "coords": [345, 192, 545, 401],
        "summary": "Land Grid Array socket designed for modern desktop processors. Connecting pins are located on the socket rather than the CPU."
      },
      {
        "id": "dimm_slots",
        "name": "DDR4 DIMM Slots",
        "coords": [617, 157, 781, 436],
        "summary": "Dual In-Line Memory Module slots operating in dual-channel mode for system memory."
      },
      {
        "id": "pcie_x16_1",
        "name": "PCIe 4.0 x16 Slot (Primary)",
        "coords": [227, 505, 635, 575],
        "summary": "Primary high-bandwidth expansion slot used for dedicated graphics cards or high-speed add-in cards."
      },
      {
        "id": "pcie_x16_2",
        "name": "PCIe 4.0 x16 Slot (Secondary)",
        "coords": [227, 610, 635, 680],
        "summary": "Secondary expansion slot operating at x4 or x8 electrical bandwidth for capture cards, high-speed storage expansion, or secondary GPUs."
      },
      {
        "id": "m2_nvme",
        "name": "M.2 Key M NVMe Slot",
        "coords": [320, 440, 500, 485],
        "summary": "High-speed M.2 storage slot utilizing PCIe lanes directly from the CPU or chipset for NVMe SSDs."
      },
      {
        "id": "atx_power",
        "name": "24-Pin ATX Main Power",
        "coords": [772, 279, 863, 453],
        "summary": "Primary power connector delivering +3.3V, +5V, +12V, and -12V DC power from the PSU to the motherboard."
      },
      {
        "id": "cpu_power",
        "name": "8-Pin EPS / ATX 12V Power",
        "coords": [180, 50, 310, 110],
        "summary": "Dedicated +12V power connector supplying dedicated power exclusively to the processor VRMs."
      },
      {
        "id": "sata_ports",
        "name": "SATA 3.0 (6Gbps) Ports",
        "coords": [780, 520, 865, 680],
        "summary": "Serial ATA ports for connecting traditional 2.5-inch SSDs, 3.5-inch HDDs, and optical drives."
      },
      {
        "id": "rear_io",
        "name": "Rear I/O Panel Cluster",
        "coords": [20, 120, 150, 580],
        "summary": "External port stack including USB Type-A/Type-C, DisplayPort, HDMI, RJ-45 Ethernet, COM/Serial ports, and audio jacks."
      }
    ]
  }
}