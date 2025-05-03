from threading import Thread
from server import create_app
from gui.main import start_gui  # adjust if needed

if __name__ == "__main__":
    app = create_app()
    Thread(target=lambda: app.run(host="0.0.0.0", port=5000), daemon=True).start()
    start_gui()
