from kazakh_tagger import KazakhTagger
import tkinter as tk
from tkinter import filedialog



# with open('1_zakon_20.07.2018_kz_raw.txt', encoding='utf-8') as file:
#     text = file.read()
# arr = text.replace('!', '.').replace('?', '.').replace('...', '.').split('.')
# print(arr)
# kz.tag(arr)


def tag_all():
    global btn, btn2
    btn.destroy()
    btn2.destroy()
    btn = tk.Button(window, text='Теггировать файл', command=upload_file,
                    font=("Courier", 24))
    btn2 = tk.Button(window, text='Назад', command=main_screen,
                     font=("Courier", 24))
    btn.grid(column=1, row=0)
    btn2.grid(column=1, row=1)


def main_screen():
    global btn, btn2, btn3, txt, rate_down, rate_up, lbl
    if btn:
        btn.destroy()
    if btn2:
        btn2.destroy()
    if btn3:
        btn3.destroy()
    if txt:
        # txt.delete('1.0', tk.END)
        txt.destroy()
    if rate_down:
        rate_down.destroy()
    if rate_up:
        rate_up.destroy()
    if lbl:
        lbl.destroy()
    btn = tk.Button(window, text="Разметка казахского текста", command=tag_all,
                    font=("Courier", 34))
    btn2 = tk.Button(window, text="Анализ разметки текста", command=analize,
                     font=("Courier", 34))
    btn.grid(column=1, row=0)
    btn2.grid(column=1, row=1)
    window.mainloop()


def analize():
    global btn, btn2
    btn.destroy()
    btn2.destroy()
    btn = tk.Button(window, text='Открыть файл', command=upload_file2,
                    font=("Courier", 24))
    btn2 = tk.Button(window, text='Назад', command=main_screen,
                     font=("Courier", 24))
    btn.grid(column=1, row=0)
    btn2.grid(column=1, row=1)


def file_save(text):
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    f.write(text)
    f.close()


def file_save_grade(kz):
    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if file is None:
        return
    for word in kz.tagged_list_of_words:
        try:
            grade = word[3]
        except IndexError:
            grade = ''
        file.write(f'{word[0]}: {word[1]}: {grade} \n')
    file.write(text)
    file.close()


def upload_file(event=None):
    from tkinter import scrolledtext
    global btn3, txt
    filename = filedialog.askopenfilename()
    if filename is None:
        return
    print('Selected:', filename)
    with open(filename, encoding="utf-8") as file:
        text = file.read()
    arr = text.replace('!', '.').replace('?', '.').replace('...', '.').split(
        '.')
    kz = KazakhTagger()
    kz.tag(arr)
    with open('output.txt', encoding="utf-8") as file:
        res = file.read()
    txt = scrolledtext.ScrolledText(window, width=60, height=30)
    txt.insert(tk.INSERT, res)

    txt.grid(column=2, row=2)
    btn3 = tk.Button(window, text='Сохранить в файл',
                     command=lambda: file_save(res),
                     font=("Courier", 14))
    btn3.grid(column=2, row=0)


def grade_up(kz):
    global idx, text, txt, rate_up, rate_down, lbl
    for sentens in kz.tagged_list_of_words:
        if sentens[2] == idx:
            sentens.append('Correct')
    idx += 1
    txt.delete('1.0', tk.END)
    try:
        text = kz.sentences[idx]
        if not text:
            idx += 1
            text = kz.sentences[idx]
    except IndexError:
        rate_up.destroy()
        rate_down.destroy()
        txt.insert(tk.INSERT, 'Готово! Сохраните ваши ответы.')
        lbl.destroy()
    else:
        txt.insert(tk.INSERT, text)
        sub = ''
        obj = ''
        pred = ''
        for res in kz.tagged_list_of_words:
            if res[2] == idx:
                if res[1] == 'SUB':
                    sub = res[0]
                if res[1] == 'OBJ':
                    obj = res[0]
                if res[1] == 'PRED':
                    pred = res[0]
        label_text = f'SUB: {sub}\n OBJ: {obj}\nPRED: {pred}'
        lbl.delete('1.0', tk.END)
        lbl.insert(tk.INSERT, label_text)


def grade_down(kz):
    global idx, text, txt, rate_up, rate_down, lbl
    for sentens in kz.tagged_list_of_words:
        if sentens[2] == idx:
            sentens.append('Wrong')
    idx += 1
    txt.delete('1.0', tk.END)
    try:
        text = kz.sentences[idx]
        if not text:
            idx += 1
            text = kz.sentences[idx]
    except IndexError:
        rate_up.destroy()
        rate_down.destroy()
        txt.insert(tk.INSERT, 'Готово! Сохраните ваши ответы.')
        lbl.destroy()
    else:
        txt.insert(tk.INSERT, text)
        sub = ''
        obj = ''
        pred = ''
        for res in kz.tagged_list_of_words:
            if res[2] == idx:
                if res[1] == 'SUB':
                    sub = res[0]
                if res[1] == 'OBJ':
                    obj = res[0]
                if res[1] == 'PRED':
                    pred = res[0]
        label_text = f'SUB: {sub}\n OBJ: {obj}\nPRED: {pred}'
        lbl.delete('1.0', tk.END)
        lbl.insert(tk.INSERT, label_text)

def upload_file2(event=None):
    from tkinter import scrolledtext
    global btn3, idx, text, rate_up, rate_down, txt, lbl
    filename = filedialog.askopenfilename()
    if filename is None:
        return
    print('Selected:', filename)
    with open(filename, encoding="utf-8") as file:
        text = file.read()
    arr = text.replace('!', '.').replace('?', '.').replace('...', '.').split(
        '.')
    kz = KazakhTagger()
    kz.tag(arr)
    txt = scrolledtext.ScrolledText(window, width=60, height=15)
    idx = 0
    try:
        text = kz.sentences[idx]
        if not text:
            idx += 1
            text = kz.sentences[idx]
    except IndexError:
        pass
    else:
        sub = ''
        obj = ''
        pred = ''
        for res in kz.tagged_list_of_words:
            if res[2] == idx:
                if res[1] == 'SUB':
                    sub = res[0]
                if res[1] == 'OBJ':
                    obj = res[0]
                if res[1] == 'PRED':
                    pred = res[0]
        label_text = f'SUB: {sub}\n OBJ: {obj}\nPRED: {pred}'
        lbl = scrolledtext.ScrolledText(window, width=60, height=15)
        lbl.grid(column=2, row=3)
        lbl.insert(tk.INSERT, label_text)
        txt.insert(tk.INSERT, text)
        txt.grid(column=2, row=2)
        rate_up = tk.Button(window, text='Верно',
                            command=lambda: grade_up(kz),
                            font=("Courier", 20))
        rate_down = tk.Button(window, text='Неверно',
                              command=lambda: grade_down(kz),
                              font=("Courier", 20))

        btn3 = tk.Button(window, text='Сохранить оценённый файл',
                         command=lambda: file_save_grade(kz))
        btn3.grid(column=2, row=0)
        rate_up.grid(column=3, row=0)
        rate_down.grid(column=4, row=0)


window = tk.Tk()

window.title("Kazakh tagger")
window.geometry('1000x700')
btn, btn2, btn3, txt, rate_up, rate_down, lbl = None, None, None, None, None, None, None
idx = 0
text = ''
main_screen()
window.mainloop()
