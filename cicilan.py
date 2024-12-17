import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class CicilanKendaraan:
    @staticmethod
    def setup_database():
        """Membuat tabel cicilan jika belum ada dan memastikan kolom yang diperlukan ada."""
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Sesuaikan dengan username MySQL Anda
            database="cicilan_kendaraan"  # Sesuaikan dengan nama database Anda
        )
        cursor = conn.cursor()

        # Membuat tabel cicilan dengan kolom yang disesuaikan
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cicilan (
                id INT AUTO_INCREMENT PRIMARY KEY,
                merk VARCHAR(255) NOT NULL,
                tipe VARCHAR(255) NOT NULL,
                harga INT NOT NULL,
                dp INT NOT NULL,
                tenor INT NOT NULL,
                bunga FLOAT NOT NULL,
                cicilan FLOAT NOT NULL
            );
        """)

        conn.commit()
        conn.close()

    @staticmethod
    def save_to_database(merk, harga, dp, tenor, bunga):
        """Menyimpan data cicilan ke database."""
        cicilan_per_bulan = (harga - dp) * (1 + bunga / 100) / tenor
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Sesuaikan dengan username MySQL Anda
            database="cicilan_kendaraan"  # Sesuaikan dengan nama database Anda
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cicilan (merk, harga, dp, tenor, bunga, cicilan)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (merk, harga, dp, tenor, bunga, cicilan_per_bulan))
        conn.commit()
        conn.close()

    @staticmethod
    def load_from_database():
        """Memuat semua data cicilan dari database."""
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Sesuaikan dengan username MySQL Anda
            database="cicilan_kendaraan"  # Sesuaikan dengan nama database Anda
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cicilan")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def search_by_merk_and_tipe(merk, tipe):
        """Mencari cicilan berdasarkan merk dan tipe kendaraan."""
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Sesuaikan dengan username MySQL Anda
            database="cicilan_kendaraan"  # Sesuaikan dengan nama database Anda
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cicilan WHERE merk LIKE %s AND tipe LIKE %s", ('%' + merk + '%', '%' + tipe + '%'))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def delete_from_database(cicilan_id):
        """Menghapus cicilan berdasarkan ID."""
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Sesuaikan dengan username MySQL Anda
            database="cicilan_kendaraan"  # Sesuaikan dengan nama database Anda
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cicilan WHERE id = %s", (cicilan_id,))
        conn.commit()
        conn.close()


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
        self.table.delete(*self.table.get_children())  # Hapus data lama dari tabel
        for row in data:
            # Format harga dan dp dengan "Rp" di depan
            row = list(row)
            row[3] = f"Rp {row[3]:,.0f}"  # Harga
            row[4] = f"Rp {row[4]:,.0f}"  # DP
            row[5] = f"{row[5]} bulan"  # Tenor dengan keterangan bulan
            row[6] = f"{row[6]}%"  # Bunga dengan tanda persen
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
            # Format harga dan dp dengan "Rp" di depan
            row = list(row)
            row[3] = f"Rp {row[3]:,.0f}"  # Harga
            row[4] = f"Rp {row[4]:,.0f}"  # DP
            row[5] = f"{row[5]} bulan"  # Tenor dengan keterangan bulan
            row[6] = f"{row[6]}%"  # Bunga dengan tanda persen
            row[7] = f"Rp {row[7]:,.0f}"  # Cicilan
            self.table.insert("", tk.END, values=row)

    def open_add_cicilan_window(self):
        """Buka jendela untuk menambah data cicilan."""
        from add_cicilan_gui import AddCicilanWindow  # Impor dilakukan di sini untuk menghindari circular import
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
