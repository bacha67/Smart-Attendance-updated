"""
Add all students from training dataset to MongoDB
"""

from db.mongo import get_db, init_db
from utils.security import hash_password
from pathlib import Path

def add_all_students():
    """Add all students from dataset/processed to database"""
    
    print("🔍 Scanning training dataset...")
    
    # Get all student folders
    dataset_path = Path('dataset/processed')
    if not dataset_path.exists():
        print(f"❌ Dataset path not found: {dataset_path}")
        return
    
    student_dirs = sorted([d for d in dataset_path.iterdir() if d.is_dir()])
    student_ids = [d.name for d in student_dirs]
    
    print(f"✅ Found {len(student_ids)} students in training data:")
    for sid in student_ids:
        print(f"   - {sid}")
    
    print("\n🔍 Connecting to database...")
    db = get_db()
    # If script is run standalone, ensure DB connection is initialized
    if db is None:
        print("⚙️  No DB connection found, initializing MongoDB connection...")
        db = init_db()
    
    print("📝 Adding students to database...\n")
    
    added = 0
    existing = 0
    
    for student_id in student_ids:
        # Check if student already exists
        existing_student = db.students.find_one({'student_id': student_id})
        
        if existing_student:
            print(f"⏭️  {student_id}: Already exists")
            existing += 1
            continue
        
        # Create student document
        student_doc = {
            'student_id': student_id,
            'name': f'Student {student_id}',
            'email': f'{student_id.lower()}@example.com',
            'phone': f'+1234567{student_id[-3:]}',
            'department': 'Computer Science',
            'year': 3,
            'section': 'A'
        }
        
        # Insert student
        db.students.insert_one(student_doc)
        print(f"✅ {student_id}: Added to database")
        added += 1
        
        # Also create user account for this student
        existing_user = db.users.find_one({'username': student_id.lower()})
        
        if not existing_user:
            user_doc = {
                'username': student_id.lower(),
                'password': hash_password('student123'),  # Default password
                'role': 'student',
                'student_id': student_id,
                'name': f'Student {student_id}',
                'email': f'{student_id.lower()}@example.com'
            }
            db.users.insert_one(user_doc)
            print(f"   └─ User account created: {student_id.lower()} / student123")
    
    print("\n" + "="*60)
    print("📊 Summary:")
    print("="*60)
    print(f"Total students in training data: {len(student_ids)}")
    print(f"Added to database: {added}")
    print(f"Already existed: {existing}")
    print("="*60)
    
    # Verify
    print("\n🔍 Verifying database...")
    total_students = db.students.count_documents({})
    print(f"✅ Total students in database: {total_students}")
    
    print("\n✅ All students added successfully!")
    print("\n📝 Default credentials for all students:")
    print("   Username: <student_id in lowercase> (e.g., stu001)")
    print("   Password: student123")
    print("\n💡 You can now test face recognition with any of these students!")


if __name__ == '__main__':
    try:
        add_all_students()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
