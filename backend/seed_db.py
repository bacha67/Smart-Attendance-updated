"""
Database seeding script for SmartAttendance
Uses real student names extracted from dataset folder
"""

from datetime import datetime, timezone
from utils.security import hash_password
from db.mysql import get_db
import json

def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

def seed_database():
    print("🌱 Seeding database...")
    db = get_db()

    # Clear existing data
    print("Clearing existing data...")
    db.execute_query("DELETE FROM attendance", fetch=False)
    db.execute_query("DELETE FROM sessions", fetch=False)
    db.execute_query("DELETE FROM students", fetch=False)
    db.execute_query("DELETE FROM users", fetch=False)

    # ─────────────────────────────────────────
    # ADMIN
    # ─────────────────────────────────────────
    db.execute_query(
        "INSERT INTO users (username, password, email, name, role, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
        ('admin', hash_password('admin123'), 'admin@smartattendance.com', 'System Administrator', 'admin', now()),
        fetch=False
    )
    print("✅ Admin created: admin / admin123")

    # ─────────────────────────────────────────
    # INSTRUCTORS
    # ─────────────────────────────────────────
    instructors = [
        {
            'username': 'dr.bekele',
            'password': 'inst123',
            'email': 'bekele@smartattendance.com',
            'name': 'Dr. Bekele Tadesse',
            'department': 'Computer Science',
            'course_name': 'Data Structures',
            'courses': ['Data Structures'],
            'class_year': '3rd Year',
            'session_types': ['lab', 'theory'],
            'sections': ['A', 'B']
        },
        {
            'username': 'dr.almaz',
            'password': 'inst123',
            'email': 'almaz@smartattendance.com',
            'name': 'Dr. Almaz Girma',
            'department': 'Computer Science',
            'course_name': 'Database Systems',
            'courses': ['Database Systems'],
            'class_year': '3rd Year',
            'session_types': ['lab', 'theory'],
            'sections': ['A', 'B']
        },
        {
            'username': 'prof.hailu',
            'password': 'inst123',
            'email': 'hailu@smartattendance.com',
            'name': 'Prof. Hailu Worku',
            'department': 'Computer Science',
            'course_name': 'Software Engineering',
            'courses': ['Software Engineering'],
            'class_year': '3rd Year',
            'session_types': ['theory'],
            'sections': ['A', 'B']
        },
        {
            'username': 'dr.tigist',
            'password': 'inst123',
            'email': 'tigist@smartattendance.com',
            'name': 'Dr. Tigist Mengistu',
            'department': 'Computer Science',
            'course_name': 'Computer Networks',
            'courses': ['Computer Networks'],
            'class_year': '3rd Year',
            'session_types': ['lab', 'theory'],
            'sections': ['A', 'B']
        },
        {
            'username': 'dr.yonas',
            'password': 'inst123',
            'email': 'yonas.inst@smartattendance.com',
            'name': 'Dr. Yonas Tesfaye',
            'department': 'Computer Science',
            'course_name': 'Operating Systems',
            'courses': ['Operating Systems'],
            'class_year': '3rd Year',
            'session_types': ['lab', 'theory'],
            'sections': ['A', 'B']
        },
    ]

    inst_query = """
        INSERT INTO users (username, password, email, name, role, department, course_name, courses, class_year, session_types, sections, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    for i in instructors:
        db.execute_query(inst_query, (
            i['username'], hash_password(i['password']), i['email'], i['name'],
            'instructor', i['department'], i['course_name'],
            json.dumps(i['courses']), i['class_year'],
            json.dumps(i['session_types']), json.dumps(i['sections']), now()
        ), fetch=False)
        print(f"✅ Instructor: {i['username']} / {i['password']} — {i['course_name']} ({i['class_year']})")

    # ─────────────────────────────────────────
    # STUDENTS — Real names from dataset
    # Format: (username, student_id, full_name, email, dept, year, section)
    # STU007 and STU020 are excluded (no face data in dataset)
    # ─────────────────────────────────────────
    students = [
        # Section A (first 10)
        ('stu.nabila',      'STU001', 'Nabila Mohammed',      'nabila.mohammed@student.edu',      'Computer Science', '3rd Year', 'A'),
        ('stu.nardi',       'STU002', 'Nardi Gemechu',        'nardi.gemechu@student.edu',        'Computer Science', '3rd Year', 'A'),
        ('stu.amanu',       'STU003', 'Amanu Bekele',         'amanu.bekele@student.edu',         'Computer Science', '3rd Year', 'A'),
        ('stu.gadisa',      'STU004', 'Gadisa Tolera',        'gadisa.tolera@student.edu',        'Computer Science', '3rd Year', 'A'),
        ('stu.yonas',       'STU005', 'Yonas Haile',          'yonas.haile@student.edu',          'Computer Science', '3rd Year', 'A'),
        ('stu.merihun',     'STU006', 'Merihun Tadesse',      'merihun.tadesse@student.edu',      'Computer Science', '3rd Year', 'A'),
        ('stu.nutoli',      'STU008', 'Nutoli Girma',         'nutoli.girma@student.edu',         'Computer Science', '3rd Year', 'A'),
        ('stu.teddy',       'STU009', 'Teddy Alemu',          'teddy.alemu@student.edu',          'Computer Science', '3rd Year', 'A'),
        ('stu.ajme',        'STU010', 'Ajme Worku',           'ajme.worku@student.edu',           'Computer Science', '3rd Year', 'A'),
        ('stu.badho',       'STU011', 'Badho Kebede',         'badho.kebede@student.edu',         'Computer Science', '3rd Year', 'A'),
        # Section B (remaining 9)
        ('stu.milkii',      'STU012', 'Milkii Dereje',        'milkii.dereje@student.edu',        'Computer Science', '3rd Year', 'B'),
        ('stu.bekam',       'STU013', 'Bekam Tesfaye',        'bekam.tesfaye@student.edu',        'Computer Science', '3rd Year', 'B'),
        ('stu.yabsira',     'STU014', 'Yabsira Solomon',      'yabsira.solomon@student.edu',      'Computer Science', '3rd Year', 'B'),
        ('stu.firansbekan', 'STU015', 'Firansbekan Hailu',    'firansbekan.hailu@student.edu',    'Computer Science', '3rd Year', 'B'),
        ('stu.bach',        'STU016', 'Bach Mengistu',        'bach.mengistu@student.edu',        'Computer Science', '3rd Year', 'B'),
        ('stu.yohannis',    'STU017', 'Yohannis Abebe',       'yohannis.abebe@student.edu',       'Computer Science', '3rd Year', 'B'),
        ('stu.bari',        'STU018', 'Bari Gemechu',         'bari.gemechu@student.edu',         'Computer Science', '3rd Year', 'B'),
        ('stu.lami',        'STU019', 'Lami Tolera',          'lami.tolera@student.edu',          'Computer Science', '3rd Year', 'B'),
        ('stu.yien',        'STU021', 'Yien Girma',           'yien.girma@student.edu',           'Computer Science', '3rd Year', 'B'),
    ]

    user_query = "INSERT INTO users (username, password, email, name, role, created_at) VALUES (%s,%s,%s,%s,%s,%s)"
    student_query = """
        INSERT INTO students (user_id, student_id, name, email, department, year, section, face_registered, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    print("\nCreating students...")
    for username, student_id, name, email, dept, year, section in students:
        user_id = db.execute_query(user_query, (
            username, hash_password('stud123'), email, name, 'student', now()
        ), fetch=False)
        db.execute_query(student_query, (
            user_id, student_id, name, email, dept, year, section, True, now()
        ), fetch=False)
        print(f"  ✅ {student_id} | {name:<22} | {year} | Section {section}")

    # ─────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────
    print("\n✅ Database seeding completed!")
    print("\n📝 Login Credentials:")
    print("=" * 55)
    print("Admin:       admin          / admin123")
    print("Instructors: dr.bekele      / inst123")
    print("             dr.almaz       / inst123")
    print("             prof.hailu     / inst123")
    print("             dr.tigist      / inst123")
    print("             dr.yonas       / inst123")
    print("Students:    stu.nabila     / stud123  (STU001)")
    print("             stu.bekam      / stud123  (STU013)")
    print("             stu.yohannis   / stud123  (STU017)")
    print("             ... (any stu.* account / stud123)")
    print("=" * 55)

    total_users       = db.execute_query("SELECT COUNT(*) as c FROM users")[0]['c']
    total_students    = db.execute_query("SELECT COUNT(*) as c FROM students")[0]['c']
    total_instructors = db.execute_query("SELECT COUNT(*) as c FROM users WHERE role='instructor'")[0]['c']
    print(f"\n📊 Total users: {total_users}  |  Instructors: {total_instructors}  |  Students: {total_students}")

if __name__ == '__main__':
    seed_database()
