import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

class CicilanKendaraan:
    @staticmethod
    def setup_database():
        """Membuat tabel cicilan jika belum ada di MySQL."""
        conn = mysql.connector.connect(
            host="localhost",  # Ganti dengan alamat host MySQL Anda
            user="root",       # Ganti dengan username MySQL Anda
            database="cicilan_kendaraan"  # Ganti dengan nama database Anda
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cicilan (
                id INT AUTO_INCREMENT PRIMARY KEY,
                merk VARCHAR(255) NOT NULL,
                tipe VARCHAR(255) NOT NULL,
                harga INT NOT NULL,
                dp INT NOT NULL,
                tenor INT NOT NULL,
                bunga FLOAT NOT NULL,
                cicilan INT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def load_from_database():
        """Memuat semua data cicilan dari database MySQL."""
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            database="cicilan_kendaraan"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cicilan")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def search_by_merk_and_tipe(merk, tipe):
        """Cari cicilan berdasarkan merk dan tipe kendaraan di MySQL."""
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            database="cicilan_kendaraan"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cicilan WHERE merk LIKE %s AND tipe LIKE %s", ('%' + merk + '%', '%' + tipe + '%'))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def insert_into_database(merk, tipe, harga, dp, tenor, bunga, cicilan):
        """Masukkan data cicilan baru ke dalam database MySQL."""
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            database="cicilan_kendaraan"
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cicilan (merk, tipe, harga, dp, tenor, bunga, cicilan)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (merk, tipe, harga, dp, tenor, bunga, cicilan))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_from_database(cicilan_id):
        """Hapus data cicilan berdasarkan ID di MySQL."""
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            database="cicilan_kendaraan"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cicilan WHERE id = %s", (cicilan_id,))
        conn.commit()
        conn.close()

class AddCicilanWindow:
    def __init__(self, root, refresh_callback=None):
        self.root = root
        self.refresh_callback = refresh_callback
        self.window = tk.Toplevel(root)
        self.window.title("Tambah Cicilan Kendaraan")
        self.window.geometry("400x500")

        self.create_form()

    def create_form(self):
        """Buat form input untuk menambah cicilan baru."""
        self.merk_label = tk.Label(self.window, text="Merk Kendaraan:")
        self.merk_label.pack(pady=5)
        self.merk_entry = tk.Entry(self.window)
        self.merk_entry.pack(pady=5)

        self.tipe_label = tk.Label(self.window, text="Tipe Kendaraan:")
        self.tipe_label.pack(pady=5)
        self.tipe_entry = tk.Entry(self.window)
        self.tipe_entry.pack(pady=5)

        self.harga_label = tk.Label(self.window, text="Harga Kendaraan (Rp):")
        self.harga_label.pack(pady=5)
        self.harga_entry = tk.Entry(self.window)
        self.harga_entry.pack(pady=5)

        self.dp_label = tk.Label(self.window, text="DP (Rp):")
        self.dp_label.pack(pady=5)
        self.dp_entry = tk.Entry(self.window)
        self.dp_entry.pack(pady=5)

        self.tenor_label = tk.Label(self.window, text="Tenor (bulan):")
        self.tenor_label.pack(pady=5)
        self.tenor_entry = tk.Entry(self.window)
        self.tenor_entry.pack(pady=5)

        self.bunga_label = tk.Label(self.window, text="Bunga (%):")
        self.bunga_label.pack(pady=5)
        self.bunga_entry = tk.Entry(self.window)
        self.bunga_entry.pack(pady=5)

        self.submit_button = tk.Button(self.window, text="Tambah Cicilan", command=self.submit_data)
        self.submit_button.pack(pady=20)

    def submit_data(self):
        """Proses data yang diinputkan dan simpan ke database MySQL."""
        merk = self.merk_entry.get().strip()
        tipe = self.tipe_entry.get().strip()
        harga = self.harga_entry.get().strip()
        dp = self.dp_entry.get().strip()
        tenor = self.tenor_entry.get().strip()
        bunga = self.bunga_entry.get().strip()

        if not merk or not tipe or not harga or not dp or not tenor or not bunga:
            messagebox.showerror("Error", "Harap isi semua data!")
            return

        try:
            harga = int(harga.replace("Rp", "").replace(",", "").strip())
            dp = int(dp.replace("Rp", "").replace(",", "").strip())
            tenor = int(tenor)
            bunga = float(bunga)

            # Menghitung cicilan (asumsikan cicilan adalah pokok pinjaman dibagi tenor)
            jumlah_pinjaman = harga - dp
            cicilan = jumlah_pinjaman / tenor

            # Menyimpan data cicilan ke dalam database
            CicilanKendaraan.insert_into_database(
                merk, tipe, harga, dp, tenor, bunga, cicilan
            )

            messagebox.showinfo("Sukses", "Data cicilan berhasil ditambahkan!")
            if self.refresh_callback:
                self.refresh_callback()  # Panggil callback untuk refresh data
            self.window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Pastikan semua data valid!")

class CicilanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Cicilan Kendaraan")
        self.root.geometry("800x600")

        CicilanKendaraan.setup_database()

        # Input untuk Pencarian
        tk.Label(root, text="Cari Berdasarkan Merk:").pack(pady=5)
        self.merk_entry = tk.Entry(root)
        self.merk_entry.pack(pady=5)

        tk.Label(root, text="Cari Berdasarkan Tipe:").pack(pady=5)
        self.tipe_entry = tk.Entry(root)
        self.tipe_entry.pack(pady=5)

        search_button = tk.Button(root, text="Cari", command=self.search_cicilan)
        search_button.pack(pady=5)

        # Table untuk Menampilkan Data
        self.table = ttk.Treeview(root, columns=("id", "merk", "tipe", "harga", "dp", "tenor", "bunga", "cicilan"), show="headings", height=15)
        self.table.pack(pady=10)

        for col in self.table["columns"]:
            self.table.heading(col, text=col.capitalize())
            self.table.column(col, width=100)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Tambah Data", command=self.open_add_cicilan_window)
        add_button.grid(row=0, column=0, padx=10)

        delete_button = tk.Button(button_frame, text="Hapus Data", command=self.delete_cicilan)
        delete_button.grid(row=0, column=1, padx=10)

        # Muat data awal
        self.load_data()

    def load_data(self):
        """Memuat data cicilan ke dalam tabel."""
        data = CicilanKendaraan.load_from_database()
        for row in data:
            row = list(row)
            row[3] = f"Rp {row[3]:,.0f}"  # Harga
            row[4] = f"Rp {row[4]:,.0f}"  # DP
            row[7] = f"Rp {row[7]:,.0f}"  # Cicilan
            self.table.insert("", tk.END, values=row)

    def search_cicilan(self):
        """Cari cicilan berdasarkan merk dan tipe."""
        merk = self.merk_entry.get().strip()
        tipe = self.tipe_entry.get().strip()

        if not merk or not tipe:
            messagebox.showerror("Error", "Harap isi merk dan tipe kendaraan!")
            return

        data = CicilanKendaraan.search_by_merk_and_tipe(merk, tipe)
        if not data:
            messagebox.showinfo("Informasi", "Tidak ada data ditemukan untuk merk dan tipe tersebut.")
            return

        # Tampilkan hasil pencarian di tabel
        self.table.delete(*self.table.get_children())
        for row in data:
            row = list(row)
            row[3] = f"Rp {row[3]:,.0f}"  # Harga
            row[4] = f"Rp {row[4]:,.0f}"  # DP
            row[7] = f"Rp {row[7]:,.0f}"  # Cicilan
            self.table.insert("", tk.END, values=row)

    def open_add_cicilan_window(self):
        """Buka jendela untuk menambah data cicilan."""
        AddCicilanWindow(self.root, self.load_data)

    def delete_cicilan(self):
        """Hapus data cicilan berdasarkan ID yang dipilih."""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih data yang ingin dihapus!")
            return

        cicilan_id = self.table.item(selected_item[0])["values"][0]

        # Hapus data cicilan dari database
        CicilanKendaraan.delete_from_database(cicilan_id)

        # Refresh tabel setelah penghapusan
        self.table.delete(*self.table.get_children())
        self.load_data()

        messagebox.showinfo("Sukses", f"Data cicilan dengan ID {cicilan_id} berhasil dihapus!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CicilanApp(root)
    root.mainloop()
