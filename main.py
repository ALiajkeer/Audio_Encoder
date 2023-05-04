import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import subprocess
from PIL import Image, ImageTk
import logging

APP_DEF_WIDTH = 210
APP_DEF_HEIGHT = 225
FLAC_ENCODER_PASS = "D:/Program Files/FLAC/flac.exe"


class FlacEncoder(tk.LabelFrame):
    def __init__(self, root):
        try:
            super().__init__(root, bd=2, relief="ridge", text="登録アプリ")
            self.grid(row=0, sticky="we")
            self.root = root

            # エンコードする音楽ファイルのパス
            self.source_file = ""
            # FLACエンコーダーのパス
            self.flac_encoder = FLAC_ENCODER_PASS

            # 音符ラベルを表示
            img = Image.open('./symbol007.png')
            resized_img = img.resize((200, 200))
            self.img = ImageTk.PhotoImage(resized_img)
            self.label = tk.Label(self, image=self.img)
            self.label.pack()

            # ドラッグアンドドロップ
            self.label.drop_target_register(DND_FILES)
            self.label.dnd_bind('<<Drop>>', self.func_drag_and_drop)

        except Exception as e:
            logging.exception("アプリ表示関数の初期化処理で異常発生: %s", e)

    # ドラッグアンドドロップ時、wav→flacに変換する
    def func_drag_and_drop(self, event):
        try:
            # ドロップされたファイルからアプリ情報を取得
            full_path = event.data.strip('{}\'')
            # ファイル名を除いたフォルダパスを取得
            folder_path = os.path.dirname(full_path)
            # 拡張子を除いたファイル名を取得
            filename = os.path.splitext(os.path.basename(full_path))[0]

            # exeファイルのみDBへ登録
            if full_path.lower().endswith(".wav"):
                self.source_file = full_path
            else:
                messagebox.showerror("警告", "wavファイル以外のファイルは登録できません。")
                return

            # 出力するFLACファイルのパス
            output_file = folder_path + "/" + filename + ".flac"
            # FLACエンコードのコマンドライン引数
            flac_args = ["-o", output_file, self.source_file]
            # FLACエンコーダーを呼び出す
            enc_result = subprocess.run([self.flac_encoder] + flac_args).returncode
            # 出力ファイルが作成されたか確認する
            if enc_result == 0:
                print("FLACファイルが作成されました。")
                messagebox.showinfo("成功", "FLACファイルが作成されました。")
            else:
                messagebox.showerror("警告", "FLACファイルの作成に失敗しました。")
        except Exception as e:
            logging.exception("アプリ登録処理で異常発生: %s", e)


def main():
    # インスタンス作成
    root = TkinterDnD.Tk()

    # ログレベル設定
    logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(message)s', )

    # ウィンドウサイズ、タイトルの設定
    root.geometry(f'{APP_DEF_WIDTH}x{APP_DEF_HEIGHT}')
    root.minsize(APP_DEF_WIDTH, APP_DEF_HEIGHT)
    root.maxsize(APP_DEF_WIDTH + 100, APP_DEF_HEIGHT + 100)
    root.title(f'FLACエンコーダー')

    app = FlacEncoder(root=root)

    app.mainloop()


main()
