import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv

DB_FILE = 'nilai_siswa.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_siswa TEXT NOT NULL,
                biologi REAL NOT NULL,
                fisika REAL NOT NULL,
                inggris REAL NOT NULL,
                prediksi_fakultas TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_nilai(nama, bio, fis, ing, prediksi):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO nilai_siswa (nama_siswa,
        biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, bio, fis, ing, prediksi))
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('SELECT id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa ORDER BY id DESC')
    rows = cur.fetchall()   
    conn.close()
    return rows             

def predict_fakultas(biologi, fisika, inggris):
    # Nilai tertinggi jelas
    if biologi > fisika and biologi > inggris:
        return 'Kedokteran'
    elif fisika > biologi and fisika > inggris:
        return 'Teknik'
    elif inggris > biologi and inggris > fisika:
        return 'Bahasa'
    else:
        # tie -> priority
        max_val = max(biologi, fisika, inggris)

        if biologi == max_val:
            return 'Kedokteran'
        elif fisika == max_val:
            return 'Teknik'
        else:
            return 'Bahasa'


class NilaiSiswaApp :
    def __init__(self, root) :
        self.root = root
        self.root.title('Input Nilai Siswa - SQLite')
        root.geometry('900x520')
        root.minsize(800, 480)

        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception :
            pass
        style.configure('TLabel', font = ('Segoe UI', 10))
        style.configure('TButton', font = ('Segoe UI,', 10), padding = 6)
        style.configure('Header.TLabel', font = ('Segoe UI', 12, 'bold'))
        style.configure('Treeview.Heading', font = ('Segoe UI', 10, 'bold'))
        style.configure('Treeview', font = ('Segoe UI', 10))

        frm_left = ttk.LabelFrame(root, text='Form Input', padding=(12, 12))
        frm_left.grid(row=0, column=0, padx=12, pady=12, sticky='NWS')
        frm_right = ttk.LabelFrame(root, text='Data Nilai Siswa', padding=(12, 12))

        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        ttk.Label(frm_left, text='Nama Siswa:',style='Header.TLabel').grid(row=0, column=0, sticky='W',)
        self.entry_nama = ttk.Entry(frm_left, width=34)
        self.entry_nama.grid(row=1, column=0, pady=6, sticky='W')
