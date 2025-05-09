# SSSAdmin: Sales and Inventory Management System

**SSSAdmin** is a Python desktop application for managing inventory, tracking purchases, and generating insightful statistics. It features an intuitive graphical interface, image-based item entries, local sales history storage, export to Excel, and dynamic graph plotting.

---

## ✨ Features

- **Item Management**:
  - Add, edit, delete items with associated images.
  - Support for items assigned to multiple "stånd" (stands).
- **Purchase Logging**:
  - Records purchases locally by day.
  - Buffered syncing for offline usage with a mobile companion app.
- **Sales Statistics**:
  - Daily summaries.
  - Revenue and quantity per item and stand.
- **Custom Graphs**:
  - Visualize sales trends with selectable axes (e.g., date, item, stand, quantity).
- **Data Export**:
  - Generate Excel files from purchase history.
- **Developer Console**:
  - Built-in debug console with live logs.
- **Keyboard Shortcuts**:
  - `Ctrl+A` – Add item
  - `Ctrl+S` – View stats
  - `Ctrl+G` – Create graph
  - `Ctrl+P` – Export Excel
  - `Ctrl+H` – Help overlay
  - `Ctrl+T` – Open console
  - `Ctrl+C` – Exit app
- **Cross-Platform Ready**:
  - Runs on Windows and development environments via PyInstaller packaging.

---

## 🖥️ Setup Instructions

### Requirements

- **Python 3.12.10**
- Dependencies (listed in `requirements.txt`):  
  Flask, Pillow, matplotlib, openpyxl, etc.

### Install and Run

```bash
# Clone the repository
git clone <repo-url>
cd SSSAdmin

# Create virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
# or
source venv/bin/activate  # macOS/Linux

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### First-Time Setup

Ensure these folders exist (or are created automatically on first run):

- `images/` – for item images
- `purchases/` – for daily purchase logs
- `items.json` – auto-generated if missing

---

## 🛠️ Packaging as Executable (Windows)

PyInstaller is used to bundle the app and assets into a standalone `.exe`.

**Create a bundled executable**:

```bash
pyinstaller SSSAdmin.spec
```

Ensure `app.ico` is in the root directory for proper icon display in the taskbar and Explorer.

> **Note:** To persist data in production (i.e., after packaging), ensure `items.json`, `images/`, and `purchases/` are either bundled via the `.spec` file or placed in a writable directory like `%APPDATA%/SSSAdmin`.

---

## 📁 File Structure

```
.
├── app.py                  # Entry point
├── gui/                    # GUI logic and components
├── server/                 # Flask server + config
├── items.json              # Inventory data
├── purchases/              # JSON purchase logs
├── images/                 # Item thumbnails
├── SSSAdmin.spec           # PyInstaller spec for bundling
```

---

## 📜 License

MIT © 2025 [Joakim Gustavsson]