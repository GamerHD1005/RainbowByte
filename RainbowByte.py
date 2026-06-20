import customtkinter as ctk
import wmi
import threading
import time
import colorsys

# Setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x550")
        self.title("RainbowByte")

        # 1. Titel-Label
        self.title_label = ctk.CTkLabel(self, text="RainbowByte", font=("Arial", 32, "bold"))
        self.title_label.pack(pady=(20, 10))

        # 2. Button
        self.btn = ctk.CTkButton(self, text="Search", command=self.get_all_serials)
        self.btn.pack(pady=10, padx=20, fill="x")

        # 3. Großes Textfeld
        self.display = ctk.CTkTextbox(self, width=450, height=350, font=("Arial", 18, "bold"))
        self.display.pack(pady=10, padx=20, fill="both", expand=True)
        self.display.configure(state="disabled")

        # Regenbogen-Animation sofort starten
        threading.Thread(target=self.rainbow_effect, daemon=True).start()

    def get_all_serials(self):
        c = wmi.WMI()
        info = "--- HARDWARE IDENTIFIER ---\n\n"
        try:
            info += f"Mainboard: {c.Win32_BaseBoard()[0].SerialNumber}\n"
            info += f"BIOS: {c.Win32_BIOS()[0].SerialNumber}\n"
            info += f"CPU ID: {c.Win32_Processor()[0].ProcessorId}\n"
            for disk in c.Win32_DiskDrive():
                info += f"Disk: {disk.SerialNumber}\n"
        except Exception as e:
            info += f"Fehler beim Laden: {e}"
        
        self.display.configure(state="normal")
        self.display.delete("0.0", "end")
        self.display.insert("0.0", info)
        self.display.configure(state="disabled")

    def rainbow_effect(self):
        hue_title = 0
        hue_text = 0.33
        hue_btn = 0.66
        
        while True:
            # Farben berechnen
            c1 = colorsys.hsv_to_rgb(hue_title, 1, 1)
            c2 = colorsys.hsv_to_rgb(hue_text, 1, 1)
            c3 = colorsys.hsv_to_rgb(hue_btn, 1, 1)
            
            hex_title = '#%02x%02x%02x' % (int(c1[0]*255), int(c1[1]*255), int(c1[2]*255))
            hex_text = '#%02x%02x%02x' % (int(c2[0]*255), int(c2[1]*255), int(c2[2]*255))
            hex_btn = '#%02x%02x%02x' % (int(c3[0]*255), int(c3[1]*255), int(c3[2]*255))
            
            # Anwenden
            self.title_label.configure(text_color=hex_title)
            self.display.configure(text_color=hex_text)
            self.btn.configure(fg_color=hex_btn, hover_color=hex_btn)
            
            # Rotation
            hue_title += 0.02
            hue_text += 0.02
            hue_btn += 0.02
            if hue_title >= 1: hue_title = 0
            if hue_text >= 1: hue_text = 0
            if hue_btn >= 1: hue_btn = 0
            
            time.sleep(0.05)

if __name__ == "__main__":
    app = App()
    app.mainloop()
