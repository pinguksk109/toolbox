import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
import piexif

def load_exif_data(file_path):
    try:
        exif_data = piexif.load(Image.open(file_path).info["exif"])
        return exif_data
    except Exception as e:
        print(f"EXIFデータの読み込みに失敗しました: {e}")
        return None

def parse_exif_data(exif_data):
    if not exif_data:
        return None

    try:
        focal_length = exif_data["Exif"].get(piexif.ExifIFD.FocalLength)
        f_number = exif_data["Exif"].get(piexif.ExifIFD.FNumber)
        exposure_time = exif_data["Exif"].get(piexif.ExifIFD.ExposureTime)
        iso_speed = exif_data["Exif"].get(piexif.ExifIFD.ISOSpeedRatings)

        focal_length = focal_length[0] / focal_length[1] if focal_length else "不明"
        f_number = f_number[0] / f_number[1] if f_number else "不明"
        exposure_time = f"{exposure_time[0]}/{exposure_time[1]}" if exposure_time else "不明"
        iso_speed = iso_speed if iso_speed else "不明"

        return focal_length, f_number, exposure_time, iso_speed
    except Exception as e:
        print(f"EXIFデータの解析に失敗しました: {e}")
        return None

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("JPEGファイル", "*.jpg;*.jpeg")])
    if not file_path:
        return

    exif_data = load_exif_data(file_path)
    parsed_data = parse_exif_data(exif_data)

    if parsed_data:
        focal_length, f_number, exposure_time, iso_speed = parsed_data
        entry_distance.delete(0, tk.END)
        entry_distance.insert(0, focal_length)

        entry_f_value.delete(0, tk.END)
        entry_f_value.insert(0, f_number)

        entry_shutter_speed.delete(0, tk.END)
        entry_shutter_speed.insert(0, exposure_time)

        entry_iso.delete(0, tk.END)
        entry_iso.insert(0, iso_speed)

def convert_format():
    body = entry_body.get()
    lens = entry_lens.get()
    distance = entry_distance.get()
    f_value = entry_f_value.get()
    shutter_speed = entry_shutter_speed.get()
    iso = entry_iso.get()

    formatted_text = f"=====\n{body}\n{lens}\n{distance}  ƒ/{f_value} {shutter_speed}s ISO {iso}\n====="

    output_label.config(text=formatted_text)
    output_label.text = formatted_text


def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(output_label.text)
    root.update()
    copy_button.config(text="コピーしました!", state=tk.DISABLED)
    root.after(
        2000, lambda: copy_button.config(text="コピー", state=tk.NORMAL)
    )


root = tk.Tk()
root.title("カメラ情報変換ツール")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

labels = ["Body", "Lens", "換算距離", "F値", "シャッター速度", "ISO"]
entries = []

body_options = ["", "LUMIX GX7MK2", "Canon PowerShot G5X"]
lens_options = [
    "",
    "LUMIX G VARIO 12-32mm / F3.5-5.6 ASPH. / MEGA O.I.S.",
    "LUMIX G 14mm F2.5 ASPH",
    "LUMIX G VARIO 45-150mm/F4.0-5.6 ASPH",
    "LUMIX G VARIO 14-42mm F3.5-5.6 II ASPH. MEGA O.I.S.",
    "MINOLTA AUTO ROKKOR-PF 55㎜ f:1.8(前期型) 1958年(?)",
    "SIGMA 30mm F1.4 DC DN",
]

for i, label_text in enumerate(labels):
    label = ttk.Label(frame, text=label_text)
    label.grid(row=i, column=0, sticky=tk.W, pady=5)

    if label_text == "Body":
        entry = ttk.Combobox(frame, values=body_options, width=27)
        entry.set("自由入力または選択")
    elif label_text == "Lens":
        entry = ttk.Combobox(frame, values=lens_options, width=27)
        entry.set("自由入力または選択")
    else:
        entry = ttk.Entry(frame, width=30)

    entry.grid(row=i, column=1, pady=5)
    entries.append(entry)

(
    entry_body,
    entry_lens,
    entry_distance,
    entry_f_value,
    entry_shutter_speed,
    entry_iso,
) = entries

button_frame = ttk.Frame(frame)
button_frame.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

file_button = ttk.Button(button_frame, text="JPEGから取得", command=open_file)
file_button.grid(row=0, column=0, padx=5)

convert_button = ttk.Button(button_frame, text="変換", command=convert_format)
convert_button.grid(row=0, column=1, padx=5)

copy_button = ttk.Button(
    button_frame, text="コピー", command=copy_to_clipboard
)
copy_button.grid(row=0, column=2, padx=5)

output_label = ttk.Label(
    root, text="", font=("メイリオ", 12), justify=tk.LEFT, padding=10
)
output_label.grid(row=1, column=0, sticky=(tk.W, tk.E))
output_label.text = ""

root.mainloop()
