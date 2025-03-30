from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox, ttk
import unittest
from datetime import datetime, timedelta
from typing import List, Optional, Dict

# Class Member - คลาสสำหรับจัดการข้อมูลสมาชิก

class Member:
    def __init__(self, member_id: str, name: str, contact_info: str):
        # เก็บข้อมูลพื้นฐานของสมาชิก
        self.member_id = member_id
        self.name = name
        self.contact_info = contact_info
        # เพิ่มประวัติการเปลี่ยนแปลงข้อมูล
        self.update_history: List[str] = []

    def display_info(self) -> str:
        # แสดงข้อมูลสมาชิกในรูปแบบข้อความ
        return f"Member ID: {self.member_id}, Name: {self.name}, Contact: {self.contact_info}"
    
    def update_info(self, name: str, contact_info: str) -> None:
        # บันทึกประวัติการเปลี่ยนแปลง
        changes = []
        if self.name != name:
            changes.append(f"Name: {self.name} -> {name}")
            self.name = name
        if self.contact_info != contact_info:
            changes.append(f"Contact: {self.contact_info} -> {contact_info}")
            self.contact_info = contact_info
        
        if changes:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.update_history.append(f"[{timestamp}] " + ", ".join(changes))


# Abstract Class Publication - คลาสแม่สำหรับสิ่งพิมพ์ทุกประเภท

class Publication(ABC):
    def __init__(self, title: str, author: str, year: int):
        # ข้อมูลพื้นฐานของสิ่งพิมพ์
        self.title = title
        self.author = author
        self.year = year
    
    @abstractmethod
    def display(self) -> str:
        # Method ที่ต้องถูก implement โดย child class
        pass

    @abstractmethod
    def get_type(self) -> str:
        # Method สำหรับระบุประเภทของสิ่งพิมพ์
        pass


# Class Book - คลาสสำหรับจัดการหนังสือ (สืบทอดจาก Publication)

class Book(Publication):
    def __init__(self, title: str, author: str, year: int, ISBN: str, genre: str):
        # เรียกใช้ constructor ของ parent class
        super().__init__(title, author, year)
        # เพิ่มข้อมูลเฉพาะของหนังสือ
        self.ISBN = ISBN
        self.genre = genre
    
    def display(self) -> str:
        # แสดงข้อมูลหนังสือ (override method จาก Publication)
        return f"Book: {self.title} by {self.author} ({self.year}), Genre: {self.genre}, ISBN: {self.ISBN}"
    
    def get_type(self) -> str:
        return "Book"


# Class Loan - คลาสสำหรับจัดการการยืม-คืน

class Loan:
    def __init__(self, member: Member, publication: Publication, loan_date: str, due_date: str):
        # เก็บข้อมูลการยืม
        self.member = member
        self.publication = publication
        self.loan_date = loan_date
        self.due_date = due_date
        self.returned = False  # สถานะการคืน
    
    def display_loan(self) -> str:
        # แสดงข้อมูลการยืมพร้อมสถานะ
        status = "Returned" if self.returned else "Active"
        return f"{self.publication.display()} loaned to {self.member.name} from {self.loan_date} to {self.due_date} - {status}"


# Class Library - คลาสหลักสำหรับจัดการระบบห้องสมุด

class Library:
    def __init__(self):
        # สร้าง lists สำหรับเก็บข้อมูล
        self.members: List[Member] = []
        self.publications: List[Publication] = []
        self.loans: List[Loan] = []

    def add_member(self, member: Member) -> None:
        # เพิ่มสมาชิกใหม่
        self.members.append(member)
        messagebox.showinfo("Success", f"Member {member.name} added successfully.")
    
    def remove_member(self, member_id: str) -> None:
        self.members = [m for m in self.members if m.member_id != member_id]
        messagebox.showinfo("Success", f"Member removed successfully.")
    
    def update_member(self, member_id: str, name: str, contact_info: str) -> None:
        member = self.find_member(member_id)
        if member:
            member.update_info(name, contact_info)
            messagebox.showinfo("Success", f"Member information updated successfully.")
        else:
            messagebox.showerror("Error", "Member not found!")
    
    def add_publication(self, publication: Publication) -> None:
        self.publications.append(publication)
        messagebox.showinfo("Success", f"Publication '{publication.title}' added successfully.")
    
    def find_publications(self, search_term: str, search_type: str = "title") -> List[Publication]:
        # ค้นหาสิ่งพิมพ์ตามเงื่อนไขต่างๆ โดยใช้ list comprehension
        if search_type == "title":
            # หาหนังสือที่มีชื่อคล้ายกับ search_term (ไม่สนใจตัวพิมพ์เล็ก/ใหญ่)
            return [p for p in self.publications if search_term.lower() in p.title.lower()]
        elif search_type == "author":
            # หาหนังสือที่มีชื่อผู้แต่งคล้ายกับ search_term
            return [p for p in self.publications if search_term.lower() in p.author.lower()]
        elif search_type == "genre":
            # หาหนังสือที่มีประเภทคล้ายกับ search_term
            # isinstance(p, Book) ใช้ตรวจสอบว่า p เป็น object ของ class Book หรือไม่
            return [p for p in self.publications if isinstance(p, Book) and search_term.lower() in p.genre.lower()]
        return []
    
    def find_member(self, member_id: str) -> Optional[Member]:
        # ใช้ next() และ generator expression เพื่อหาสมาชิกที่มี ID ตรงกับที่ต้องการ
        # ถ้าไม่เจอจะคืนค่า None (เพราะใช้ Optional ใน type hint)
        return next((m for m in self.members if m.member_id == member_id), None)
    
    def borrow_publication(self, member_id: str, publication_title: str, loan_date: str, due_date: str) -> None:
        # ค้นหาสมาชิกและหนังสือที่ต้องการยืม
        member = self.find_member(member_id)
        publication = next((p for p in self.publications if p.title == publication_title), None)
        
        if member and publication:
            # ตรวจสอบว่าหนังสือถูกยืมไปแล้วหรือไม่
            # กรองเฉพาะรายการยืมที่ยังไม่ได้คืน (returned = False)
            active_loans = [l for l in self.loans if l.publication.title == publication_title and not l.returned]
            if active_loans:
                messagebox.showerror("Error", "Publication is already loaned!")
                return
            
            # สร้างรายการยืมใหม่และเพิ่มเข้าไปในระบบ
            loan = Loan(member, publication, loan_date, due_date)
            self.loans.append(loan)
            messagebox.showinfo("Success", f"{member.name} borrowed '{publication.title}'.")
        else:
            messagebox.showerror("Error", "Member or publication not found!")
    
    def return_publication(self, publication_title: str) -> None:
        loan = next((l for l in self.loans if l.publication.title == publication_title and not l.returned), None)
        if loan:
            loan.returned = True
            messagebox.showinfo("Success", f"'{publication_title}' returned successfully.")
        else:
            messagebox.showerror("Error", "No active loan found for this publication!")
    
    def generate_overdue_report(self) -> str:
        today = datetime.now()  # วันที่ปัจจุบัน
        # กรองรายการยืมที่เกินกำหนด:
        # 1. ยังไม่ได้คืน (not loan.returned)
        # 2. วันที่กำหนดคืนน้อยกว่าวันที่ปัจจุบัน
        overdue_loans = [
            loan for loan in self.loans 
            if not loan.returned and datetime.strptime(loan.due_date, "%Y-%m-%d") < today
        ]
        # แสดงผลในรูปแบบข้อความ ถ้าไม่มีรายการเกินกำหนดจะแสดง "No overdue loans."
        return "\n".join([loan.display_loan() for loan in overdue_loans]) if overdue_loans else "No overdue loans."
    
    def generate_loan_report(self) -> str:
        active_loans = [loan for loan in self.loans if not loan.returned]
        return "\n".join([loan.display_loan() for loan in active_loans]) if active_loans else "No active loans."

    def get_member_history(self, member_id: str) -> Dict:
        """รับประวัติทั้งหมดของสมาชิก"""
        member = self.find_member(member_id)
        if not member:
            return None
        
        # รวบรวมประวัติการยืม-คืน
        loan_history = [
            loan for loan in self.loans 
            if loan.member.member_id == member_id
        ]
        
        # แยกเป็นรายการที่ยังไม่คืนและคืนแล้ว
        active_loans = [loan for loan in loan_history if not loan.returned]
        returned_loans = [loan for loan in loan_history if loan.returned]
        
        return {
            "member": member,
            "active_loans": active_loans,
            "returned_loans": returned_loans,
            "update_history": member.update_history
        }


# GUI Application - ส่วนติดต่อผู้ใช้

class LibraryApp:
    def __init__(self, root):
        self.library = Library()  # สร้าง instance ของระบบห้องสมุด
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        
        # สร้าง notebook สำหรับแท็บต่างๆ
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # สร้างแท็บสำหรับแต่ละฟังก์ชัน
        self.create_member_tab()
        self.create_publication_tab()
        self.create_loan_tab()
        self.create_report_tab()
    
    def create_member_tab(self):
        member_frame = ttk.Frame(self.notebook)
        self.notebook.add(member_frame, text='Member Management')
        
        # แบ่งเป็น 2 ส่วน: ซ้ายสำหรับจัดการข้อมูล, ขวาสำหรับแสดงประวัติ
        left_frame = ttk.Frame(member_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        right_frame = ttk.Frame(member_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # ส่วนซ้าย - จัดการข้อมูลสมาชิก
        ttk.Label(left_frame, text="Member Management", font=("Arial", 14)).pack(pady=10)
        
        # Member ID
        ttk.Label(left_frame, text="Member ID:").pack()
        self.member_id_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.member_id_var).pack()
        
        # Name
        ttk.Label(left_frame, text="Name:").pack()
        self.member_name_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.member_name_var).pack()
        
        # Contact
        ttk.Label(left_frame, text="Contact:").pack()
        self.member_contact_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.member_contact_var).pack()
        
        # Buttons
        ttk.Button(left_frame, text="Add Member", command=self.add_member).pack(pady=5)
        ttk.Button(left_frame, text="Update Member", command=self.update_member).pack(pady=5)
        ttk.Button(left_frame, text="Remove Member", command=self.remove_member).pack(pady=5)
        ttk.Button(left_frame, text="Show Member History", command=self.show_member_history).pack(pady=5)
        
        # ส่วนขวา - แสดงประวัติ
        ttk.Label(right_frame, text="Member History", font=("Arial", 14)).pack(pady=10)
        
        # สร้าง Treeview สำหรับแสดงประวัติ
        self.history_tree = ttk.Treeview(right_frame, show='headings')
        self.history_tree["columns"] = ("date", "action", "details")
        
        # กำหนดหัวคอลัมน์
        self.history_tree.heading("date", text="Date")
        self.history_tree.heading("action", text="Action")
        self.history_tree.heading("details", text="Details")
        
        # กำหนดความกว้างคอลัมน์
        self.history_tree.column("date", width=100)
        self.history_tree.column("action", width=100)
        self.history_tree.column("details", width=200)
        
        # เพิ่ม scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # จัดวาง Treeview และ scrollbar
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_publication_tab(self):
        pub_frame = ttk.Frame(self.notebook)
        self.notebook.add(pub_frame, text='Publication Management')
        
        # Publication management controls
        ttk.Label(pub_frame, text="Publication Management", font=("Arial", 14)).pack(pady=10)
        
        # Add publication section
        ttk.Label(pub_frame, text="Title:").pack()
        self.title_var = tk.StringVar()
        ttk.Entry(pub_frame, textvariable=self.title_var).pack()
        
        ttk.Label(pub_frame, text="Author:").pack()
        self.author_var = tk.StringVar()
        ttk.Entry(pub_frame, textvariable=self.author_var).pack()
        
        ttk.Label(pub_frame, text="Year:").pack()
        self.year_var = tk.StringVar()
        ttk.Entry(pub_frame, textvariable=self.year_var).pack()
        
        ttk.Label(pub_frame, text="ISBN:").pack()
        self.isbn_var = tk.StringVar()
        ttk.Entry(pub_frame, textvariable=self.isbn_var).pack()
        
        ttk.Label(pub_frame, text="Genre:").pack()
        self.genre_var = tk.StringVar()
        ttk.Entry(pub_frame, textvariable=self.genre_var).pack()
        
        ttk.Button(pub_frame, text="Add Book", command=self.add_book).pack(pady=5)
        
        # Search section
        ttk.Label(pub_frame, text="Search Publications").pack(pady=10)
        self.search_var = tk.StringVar()
        ttk.Entry(pub_frame, textvariable=self.search_var).pack()
        
        self.search_type_var = tk.StringVar(value="title")
        ttk.Radiobutton(pub_frame, text="By Title", variable=self.search_type_var, value="title").pack()
        ttk.Radiobutton(pub_frame, text="By Author", variable=self.search_type_var, value="author").pack()
        ttk.Radiobutton(pub_frame, text="By Genre", variable=self.search_type_var, value="genre").pack()
        ttk.Button(pub_frame, text="Search", command=self.search_publications).pack(pady=5)
    
    def create_loan_tab(self):
        loan_frame = ttk.Frame(self.notebook)
        self.notebook.add(loan_frame, text='Loan Management')
        
        # Loan management controls
        ttk.Label(loan_frame, text="Loan Management", font=("Arial", 14)).pack(pady=10)
        
        ttk.Label(loan_frame, text="Member ID:").pack()
        self.loan_member_id_var = tk.StringVar()
        ttk.Entry(loan_frame, textvariable=self.loan_member_id_var).pack()
        
        ttk.Label(loan_frame, text="Publication Title:").pack()
        self.loan_title_var = tk.StringVar()
        ttk.Entry(loan_frame, textvariable=self.loan_title_var).pack()
        
        ttk.Button(loan_frame, text="Borrow", command=self.borrow_publication).pack(pady=5)
        ttk.Button(loan_frame, text="Return", command=self.return_publication).pack(pady=5)
    
    def create_report_tab(self):
        report_frame = ttk.Frame(self.notebook)
        self.notebook.add(report_frame, text='Reports')
        
        # Report controls
        ttk.Label(report_frame, text="Reports", font=("Arial", 14)).pack(pady=10)
        ttk.Button(report_frame, text="Show Active Loans", command=self.show_loan_report).pack(pady=5)
        ttk.Button(report_frame, text="Show Overdue Items", command=self.show_overdue_report).pack(pady=5)
    
    # Implementation of callback methods
    def add_member(self):
        member = Member(self.member_id_var.get(), self.member_name_var.get(), self.member_contact_var.get())
        self.library.add_member(member)
    
    def update_member(self):
        self.library.update_member(
            self.member_id_var.get(),
            self.member_name_var.get(),
            self.member_contact_var.get()
        )
        # อัพเดทการแสดงผลประวัติ
        self.show_member_history()
    
    def remove_member(self):
        self.library.remove_member(self.member_id_var.get())
    
    def add_book(self):
        try:
            # แปลงปีเป็นตัวเลข ถ้าแปลงไม่ได้จะเกิด ValueError
            book = Book(
                self.title_var.get(),  # ดึงค่าจาก StringVar
                self.author_var.get(),
                int(self.year_var.get()),  # แปลงเป็นตัวเลข
                self.isbn_var.get(),
                self.genre_var.get()
            )
            self.library.add_publication(book)
        except ValueError:
            # ถ้าแปลงปีเป็นตัวเลขไม่ได้ จะแสดง error
            messagebox.showerror("Error", "Invalid year format!")
    
    def search_publications(self):
        results = self.library.find_publications(self.search_var.get(), self.search_type_var.get())
        if results:
            messagebox.showinfo("Search Results", "\n".join([p.display() for p in results]))
        else:
            messagebox.showinfo("Search Results", "No publications found.")
    
    def borrow_publication(self):
        # ทำการยืมหนังสือโดยกำหนดวันคืนเป็น 14 วันนับจากวันที่ยืม
        self.library.borrow_publication(
            self.loan_member_id_var.get(),
            self.loan_title_var.get(),
            datetime.now().strftime("%Y-%m-%d"),  # วันที่ยืม (วันนี้)
            (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")  # วันกำหนดคืน (อีก 14 วัน)
        )
    
    def return_publication(self):
        self.library.return_publication(self.loan_title_var.get())
    
    def show_loan_report(self):
        messagebox.showinfo("Loan Report", self.library.generate_loan_report())
    
    def show_overdue_report(self):
        messagebox.showinfo("Overdue Report", self.library.generate_overdue_report())

    def show_member_history(self):
        # ล้างข้อมูลเก่าใน Treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        member_id = self.member_id_var.get()
        if not member_id:
            messagebox.showerror("Error", "Please enter Member ID")
            return
        
        # ดึงประวัติของสมาชิก
        history = self.library.get_member_history(member_id)
        if not history:
            messagebox.showerror("Error", "Member not found")
            return
        
        member = history["member"]
        
        # แสดงข้อมูลพื้นฐานของสมาชิก
        self.history_tree.insert("", tk.END, values=(
            datetime.now().strftime("%Y-%m-%d"),
            "Info",
            f"ID: {member.member_id}, Name: {member.name}, Contact: {member.contact_info}"
        ))
        
        # แสดงประวัติการเปลี่ยนแปลงข้อมูล
        for update in history["update_history"]:
            self.history_tree.insert("", tk.END, values=(
                "Update",
                update
            ))
        
        # แสดงรายการที่ยังไม่คืน
        for loan in history["active_loans"]:
            self.history_tree.insert("", tk.END, values=(
                loan.loan_date,
                "Active Loan",
                f"{loan.publication.title} (Due: {loan.due_date})"
            ))
        
        # แสดงรายการที่คืนแล้ว
        for loan in history["returned_loans"]:
            self.history_tree.insert("", tk.END, values=(
                loan.loan_date,
                "Returned",
                loan.publication.title
            ))


# Unit Tests - การทดสอบการทำงาน

class LibraryTests(unittest.TestCase):
    def setUp(self):
        # เตรียมข้อมูลสำหรับการทดสอบ
        self.library = Library()
        self.member = Member("M001", "Test User", "test@email.com")
        self.book = Book("Test Book", "Test Author", 2024, "1234567890", "Test Genre")
    
    def test_add_member(self):
        # ทดสอบการเพิ่มสมาชิก
        self.library.add_member(self.member)
        self.assertEqual(len(self.library.members), 1)
        self.assertEqual(self.library.members[0].name, "Test User")
    
    def test_add_publication(self):
        self.library.add_publication(self.book)
        self.assertEqual(len(self.library.publications), 1)
        self.assertEqual(self.library.publications[0].title, "Test Book")
    
    def test_borrow_publication(self):
        self.library.add_member(self.member)
        self.library.add_publication(self.book)
        self.library.borrow_publication("M001", "Test Book", "2024-03-30", "2024-04-13")
        self.assertEqual(len(self.library.loans), 1)
        self.assertFalse(self.library.loans[0].returned)


# Run Application - เริ่มการทำงานของโปรแกรม

if __name__ == "__main__":
    # รัน unit tests ก่อน
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    # เริ่มการทำงานของ GUI
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
