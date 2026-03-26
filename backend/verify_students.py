"""
Verify student database after update
"""


from config import config
from db.mysql import get_db
from db.mysql import get_db

def verify_students():
    """Verify student database"""
    
    print("="*60)
    print("VERIFYING STUDENT DATABASE")
    print("="*60)
    
    
    db = get_db()
    
    # Check counts
    print("\n📊 Database Counts:")
    print(f"   Total Users: {db.execute_query('SELECT COUNT(*) as count FROM users')[0]['count']}")
    print(f"   - Admins: {db.execute_query('SELECT COUNT(*) as count FROM users WHERE role = "admin"')[0]['count']}")
    print(f"   - Instructors: {db.execute_query('SELECT COUNT(*) as count FROM users WHERE role = "instructor"')[0]['count']}")
    print(f"   - Students: {db.execute_query('SELECT COUNT(*) as count FROM users WHERE role = "student"')[0]['count']}")
    print(f"   Student Records: {db.execute_query('SELECT COUNT(*) as count FROM students')[0]['count']}")
    
    # Check sections
    print("\n📚 Section Breakdown:")
    section_a = db.execute_query('SELECT COUNT(*) as count FROM students WHERE section = "A"')[0]['count']
    section_b = db.execute_query('SELECT COUNT(*) as count FROM students WHERE section = "B"')[0]['count']
    section_c = db.execute_query('SELECT COUNT(*) as count FROM students WHERE section = "C"')[0]['count']
    
    print(f"   Section A: {section_a} students")
    print(f"   Section B: {section_b} students")
    print(f"   Section C: {section_c} students")
    
    # List all students
    print("\n👥 All Students:")
    print("-" * 60)
    
    students = db.execute_query('SELECT * FROM students ORDER BY student_id')
    
    current_section = None
    for student in students:
        section = student.get('section', 'Unknown')
        if section != current_section:
            print(f"\n   Section {section}:")
            current_section = section
        
        student_id = student['student_id']
        name = student['name']
        face_registered = student.get('face_registered', False)
        status = "✅ Face Registered" if face_registered else "⚠️  No Face"
        
        print(f"      {student_id}: {name:25} {status}")
    
    # Check for missing student IDs
    print("\n🔍 Checking for gaps in student IDs...")
    expected_ids = [
        'STU001', 'STU002', 'STU003', 'STU004', 'STU005', 'STU006',
        'STU008', 'STU009', 'STU010', 'STU011', 'STU012', 'STU013', 'STU014',
        'STU015', 'STU016', 'STU017', 'STU018', 'STU019', 'STU021'
    ]
    
    actual_ids = [s['student_id'] for s in students]
    missing = [sid for sid in expected_ids if sid not in actual_ids]
    extra = [sid for sid in actual_ids if sid not in expected_ids]
    
    if missing:
        print(f"   ⚠️  Missing IDs: {', '.join(missing)}")
    else:
        print(f"   ✅ All expected student IDs present")
    
    if extra:
        print(f"   ⚠️  Extra IDs: {', '.join(extra)}")
    else:
        print(f"   ✅ No unexpected student IDs")
    
    # Verify user accounts
    print("\n🔐 Verifying User Accounts...")
    missing_count = 0
    mismatch_count = 0
    
    for student in students:
        
        try:
            user = db.execute_query('SELECT * FROM users WHERE id = %s', (student['user_id'],))
            if not user:
                print(f"   ❌ Missing user account for {student['student_id']}")
                missing_count += 1
            elif user['username'] != student['student_id']:
                print(f"   ⚠️  Username mismatch for {student['student_id']}")
                mismatch_count += 1
        except:
            print(f"   ❌ Invalid user_id for {student['student_id']}")
            missing_count += 1
    
    if missing_count == 0 and mismatch_count == 0:
        print(f"   ✅ All student user accounts verified")
    
    # Summary
    print("\n" + "="*60)
    print("✅ VERIFICATION COMPLETE")
    print("="*60)
    
    print(f"\n📊 Summary:")
    print(f"   Total Students: {len(students)}")
    print(f"   Section A: {section_a}")
    print(f"   Section B: {section_b}")
    print(f"   Section C: {section_c}")
    print(f"   Face Registered: {sum(1 for s in students if s.get('face_registered', False))}")
    print(f"   Pending Registration: {sum(1 for s in students if not s.get('face_registered', False))}")
    
    client.close()

if __name__ == '__main__':
    try:
        verify_students()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
