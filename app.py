import tkinter as tk
import codecs
from utils import Translate_EN_HN


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("English to Hindi")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.input_label = tk.Label(self.root, text="Input", font=("courier",20,"bold"))
        self.input_label.pack(fill = tk.X, padx=10, pady = 10)
        self.input_field = tk.Text(self.root, width = 50, height = 2, font =("courier", 10, "bold"))
        self.input_field.pack(padx = 10, pady = 4, expand = False)
        self.translate_bt = tk.Button(self.root, text="Translate", command=self.callback_translate, font=("courier", 14))
        self.translate_bt.config(height = 1, width = 17, bd=1)
        self.translate_bt.pack( padx = 10, pady = 4)
        self.output_label = tk.Label(self.root, text="Output", font=("courier",20,"bold"))
        self.output_label.pack(fill = tk.X, padx = 10, pady = 4)
        self.output_text = tk.Label(self.root, text='Upar Vakya Daale', font=("courier",25))
        self.output_text.pack(fill = tk.X, padx = 10, pady = 4)
    def callback_translate(self):
        input_en = self.input_field.get('1.0', tk.END)
        output_hn = Translate_EN_HN(input_en)
        if output_hn == '2':
            self.input_field.delete('1.0', tk.END)
            self.output_text.config(text='Upar Vakya Daale')
            tk.messagebox.showinfo("Error", "Word not in dictionary")
            return
        if output_hn == '3':
            self.input_field.delete('1.0', tk.END)
            self.output_text.config(text='Upar Vakya Daale')
            tk.messagebox.showinfo("Error", "Cannot Translate To hindi")
            return
        self.input_field.delete('1.0', tk.END)
        self.output_text.config(text=output_hn)
    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
if __name__ == '__main__':
    print("Starting Application...")
    pba = Application()
    pba.root.mainloop()