import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import os
from datetime import datetime
import pyscreenshot as ImageGrab
from fastmcp import FastMCP
from fastmcp.utilities.types import Image

class ScreenshotMCPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📸 Screenshot MCP Server (GUI + Hermes)")
        self.root.geometry("480x380")
        self.root.resizable(False, False)

        self.running = False
        self.server_thread = None
        self.screenshot_count = 0
        
        # Save to ./screenshot/ folder
        self.save_dir = os.path.join(os.getcwd(), "screenshot")
        os.makedirs(self.save_dir, exist_ok=True)

        # Title
        tk.Label(root, text="Screenshot MCP Server", font=("Arial", 18, "bold"), 
                 fg="#2c3e50").pack(pady=12)

        # Status
        self.status_label = tk.Label(root, text="● Status: Stopped", 
                                     font=("Arial", 12), fg="#e74c3c")
        self.status_label.pack(pady=5)

        self.port_label = tk.Label(root, text="Hermes → http://192.168.1.33:8001", 
                                   font=("Arial", 9), fg="#7f8c8d")
        self.port_label.pack(pady=2)

        # Counter
        self.count_label = tk.Label(root, text="Screenshots taken: 0", font=("Arial", 11))
        self.count_label.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        self.start_btn = tk.Button(btn_frame, text="▶ START MCP SERVER", 
                                   command=self.start_server, bg="#27ae60", fg="white",
                                   font=("Arial", 11, "bold"), width=22, height=2)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(btn_frame, text="■ STOP SERVER", 
                                  command=self.stop_server, bg="#e74c3c", fg="white",
                                  font=("Arial", 11, "bold"), width=22, height=2,
                                  state=tk.DISABLED)
        self.stop_btn.pack(pady=5)

        tk.Button(btn_frame, text="📸 Take Screenshot Now", 
                  command=self.take_now, bg="#3498db", fg="white",
                  font=("Arial", 11, "bold"), width=22, height=2).pack(pady=5)

        # Folder info
        tk.Label(root, text=f"Screenshots saved to: {self.save_dir}", 
                 font=("Arial", 9), fg="#555555").pack(pady=5)

        # Footer
        tk.Label(root, text="EXACT same logic as your working auto_screenshot.py", 
                 font=("Arial", 8), fg="#7f8c8d").pack(pady=10)

    def start_server(self):
        if not self.running:
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="● Status: MCP Server Running", fg="#27ae60")

            self.server_thread = threading.Thread(target=self.run_mcp_server, daemon=True)
            self.server_thread.start()

    def stop_server(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="● Status: Stopped", fg="#e74c3c")

    def run_mcp_server(self):
        mcp = FastMCP("screenshot", version="1.0.0")

        @mcp.tool()
        async def take_screenshot(region: str = "full"):
            try:
                # EXACT same logic as your working auto_screenshot.py
                if region == "full":
                    img = ImageGrab.grab()
                else:
                    x, y, w, h = map(int, region.split(","))
                    img = ImageGrab.grab(bbox=(x, y, x + w, y + h))

                # Save to ./screenshot/ folder
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(self.save_dir, f"screenshot_{timestamp}.png")
                img.save(filename)

                self.screenshot_count += 1
                self.root.after(0, lambda: self.count_label.config(
                    text=f"Screenshots taken: {self.screenshot_count}"))

                with open(filename, "rb") as f:
                    data = f.read()
                return Image(data=data, format="png")
            except Exception as e:
                return f"Failed: {str(e)}"

        mcp.run(transport="http", host="0.0.0.0", port=8001)

    def take_now(self):
        try:
            # EXACT same logic as your working auto_screenshot.py
            img = ImageGrab.grab()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.save_dir, f"screenshot_{timestamp}.png")
            img.save(filename)

            self.screenshot_count += 1
            self.count_label.config(text=f"Screenshots taken: {self.screenshot_count}")

            messagebox.showinfo("Success", f"Screenshot saved!\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotMCPGUI(root)
    root.mainloop()
