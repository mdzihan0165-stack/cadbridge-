# CadBridge

<p align="center">
  <strong>Convert Simple JSON into Professional AutoCAD (.dxf) Floor Plans — Automatically</strong>
</p>

<p align="center">
  <a href="https://github.com/mdzihan0165-stack/cadbridge-/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/AutoCAD-DXF%20R2018%20(AC1032)-EB3C00.svg?logo=autodesk&logoColor=white" alt="AutoCAD DXF R2018">
  <img src="https://img.shields.io/badge/Layer%20Standard-AIA%20%7C%20ISO%2013567-purple.svg" alt="AIA CAD / ISO 13567">
  <img src="https://img.shields.io/badge/Build-Passing-2ea44f.svg" alt="Build Passing">
</p>

---

## 💡 What is CadBridge?

**CadBridge** is a Python tool that generates production-ready **AutoCAD (`.dxf`) architectural floor plans** from simple, human-readable JSON files. 

You **do not need AutoCAD installed** to use it. You write or generate a simple room layout in JSON, and CadBridge automatically:
1. Draws double-line exterior and interior walls with real architectural thickness.
2. Inserts doors with proper frames and 90° swing arcs.
3. Places windows with exterior sills and glass lines.
4. Adds dimension lines, centered room labels, and sheet title blocks.
5. Calculates room carpet areas, total square footage, and exports a complete Bill of Quantities (BOQ).
6. Renders high-resolution image previews (`PNG`) in dark modelspace and light paper styles.

---

## 🔄 How It Works

```
┌───────────────────────────────┐        ┌──────────────┐        ┌──────────────────────────────────────┐
│      1. Simple JSON File      │        │              │        │        3. Output Deliverables        │
│                               │  ───>  │  CadBridge   │  ───>  │  📁 my_drawing.dxf (AutoCAD File)    │
│  - Room sizes (width, length) │        │    Engine    │        │  🖼️ preview.png    (Visual Image)    │
│  - Doors & Window placements  │        │              │        │  📊 boq.md / .csv  (Area Schedule)   │
└───────────────────────────────┘        └──────────────┘        └──────────────────────────────────────┘
```

---

## 🎯 The Problem vs. The CadBridge Solution

| Traditional Manual Drafting | With CadBridge Automation |
|---|---|
| ⏳ **Hours of repetitive drawing:** Manually offsetting walls, drawing arcs for doors, and adding dimension lines one by one. | ⚡ **Done in 1 second:** Define your room dimensions in JSON, run one command, and get a complete drawing. |
| 🧮 **Manual area calculation:** Measuring every room by hand or with a calculator to determine square footage. | 📈 **Automated Takeoffs (BOQ):** Generates net carpet area, gross built-up area (BUA), and door/window schedules automatically. |
| 🖥️ **Requires expensive CAD software:** Need AutoCAD installed on a high-end PC just to view or draft plans. | 🌐 **Headless & 100% Free:** Runs on any computer with pure Python and outputs standard DXF files openable anywhere. |

---

## 📸 Verified in Autodesk AutoCAD Web

Every `.dxf` drawing produced by CadBridge conforms strictly to **AIA CAD Layer Guidelines** and **ISO 13567**. Here is a generated clinic plan opened directly inside **Autodesk's official AutoCAD Web App**:

<p align="center">
  <img src="assets/autocad_web_verification.png" alt="AutoCAD Web Verification" width="95%" />
</p>

---

## 🖼️ Sample Outputs

<table>
  <tr>
    <td width="50%" align="center">
      <strong>Medical Consultation Clinic (AutoCAD Dark Modelspace)</strong><br/><br/>
      <img src="assets/clinic_floorplan_dark.png" alt="Medical Clinic Dark" width="100%" />
    </td>
    <td width="50%" align="center">
      <strong>Medical Consultation Clinic (Architectural Plot Style)</strong><br/><br/>
      <img src="assets/clinic_floorplan_light.png" alt="Medical Clinic Light" width="100%" />
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <strong>Modern 2BHK Apartment (AutoCAD Dark Modelspace)</strong><br/><br/>
      <img src="assets/apartment_2bhk_dark.png" alt="2BHK Apartment Dark" width="100%" />
    </td>
    <td width="50%" align="center">
      <strong>Modern 2BHK Apartment (Architectural Plot Style)</strong><br/><br/>
      <img src="assets/apartment_2bhk_light.png" alt="2BHK Apartment Light" width="100%" />
    </td>
  </tr>
</table>

---

## 🚀 30-Second Quick Start

### 1. Install

```bash
# Clone the repository
git clone https://github.com/mdzihan0165-stack/cadbridge-.git
cd cadbridge-

# Install required packages (ezdxf, matplotlib)
pip install -r requirements.txt
```

### 2. Generate a Floor Plan

Run this single command to turn the template into an AutoCAD `.dxf` drawing and an image preview:

```bash
python json2dxf.py spec_template.json -o sample_floorplan.dxf --snapshot --theme dark
```

This creates:
- `sample_floorplan.dxf` — Open in any CAD viewer (AutoCAD, LibreCAD, AutoCAD Web).
- `sample_floorplan.png` — An image preview of your drawing you can view immediately.

### 3. Generate Area Schedule & Bill of Quantities (BOQ)

```bash
python cad_boq.py spec_template.json -o boq_schedule.md --csv rooms.csv
```

---

## 📝 How Simple is the Input? (Understanding the JSON)

You don't need CAD knowledge to create a floor plan. Here is how easy it is to define a room:

```json
{
  "name": "Master Bedroom",
  "width": 4000,
  "length": 4500,
  "wall_thickness": 125,
  "doors": [
    { "wall": "south", "pos": 600, "width": 900, "swing": "inward_right" }
  ],
  "windows": [
    { "wall": "north", "pos": 1500, "width": 1200 }
  ]
}
```

- **`width` & `length`:** Room size in millimeters (`mm`).
- **`wall`:** Which side the opening is on (`north`, `south`, `east`, or `west`).
- **`pos`:** Distance from the wall corner.
- **`swing`:** Door opening direction (`inward_right`, `inward_left`, `outward_right`, `outward_left`).

---

## 📊 Sample Automated Area Report (BOQ)

CadBridge automatically calculates net usable carpet area and circulation efficiency for the entire building:

| Room Name | Net Area (m²) | Area (sq.ft) | Dimensions (mm) |
|---|---|---|---|
| Reception & Waiting Lounge | 24.28 | 261.35 | 5250 × 4625 |
| Chief Consultant Chamber | 18.06 | 194.40 | 4125 × 4375 |
| Specialist Chamber 2 | 14.77 | 158.98 | 3375 × 4375 |
| Examination & ECG Room | 8.20 | 88.26 | 1875 × 4375 |
| Pharmacy & Dispensary | 6.56 | 70.61 | 2625 × 2500 |
| Sample Collection Lab | 6.56 | 70.61 | 2625 × 2500 |

---

## 📐 Standard CAD Layers

Every generated drawing follows official CAD layer conventions:

| Layer | Color | Purpose |
|---|---|---|
| `A-WALL-EXTR` | Cyan | Exterior structural perimeter walls (250mm) |
| `A-WALL-INTR` | Green | Interior partition walls (125mm) |
| `A-DOOR` | Yellow | Doors with 90° swing arcs |
| `A-GLAZ` | Blue | Windows with sills and glass panes |
| `A-ANNO-TEXT` | White | Centered room labels and tag bubbles |
| `A-ANNO-DIMS` | Red | Exterior dimension lines with ticks |
| `A-TITL` | Cyan | Title block, author info, and sheet border |

---

## 🧪 Running Automated Tests

Run the built-in unit tests to verify your installation:

```bash
python -m unittest discover tests/
```

---

## 👤 Author & Maintainer

**Montasir Tajwar Jihan**  
*Lead Computational CAD & Architectural Automation Engineer*  
- **GitHub:** [@mdzihan0165-stack](https://github.com/mdzihan0165-stack)  
- **Email:** [mdzihan0165@gmail.com](mailto:mdzihan0165@gmail.com)  

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it in your personal and commercial projects.
