from app import create_app, db

# Expose app at module level so Vercel's WSGI server can find it
app = create_app()

# Create all DB tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()