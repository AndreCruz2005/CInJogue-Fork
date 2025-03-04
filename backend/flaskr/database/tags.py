from database.database import db

UserTags = db.Table(
    'user_tags',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('user_id', db.Integer, nullable=False),  
    db.Column('text', db.String, nullable=False),
    db.Column('type', db.String, nullable=False)
)

def add_user_tag(user_id, text, tag_type):
    try:
        new_tag = UserTags.insert().values(user_id=user_id, text=text, type=tag_type)
        db.session.execute(new_tag)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error adding tag: {e}")
        return False
    
def remove_user_tag(user_id, text):
    try:
        entry_to_delete = UserTags.delete().where(UserTags.c.user_id == user_id, UserTags.c.text == text)
        db.session.execute(entry_to_delete)
        db.session.commit()
        print(f"Tag deleted successfully.")
        return True
        
    except Exception as e:
        db.session.rollback()
        print("Failed to remove game: " + str(e))
        return False

def get_tags(user_id):
    tags = db.session.query(UserTags).filter_by(user_id=user_id).all()
    return tags 

def remove_all_user_tags(user_id):
    try:
        tags_to_delete = UserTags.delete().where(UserTags.c.user_id == user_id)
        db.session.execute(tags_to_delete)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Failed to remove all tags for user_id {user_id}: {e}")
        return False
