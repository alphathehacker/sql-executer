from flask import Flask, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///balu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def home():
    # Get table names to display on the page
    table_names = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    table_names = [row[0] for row in table_names]
    # Retrieve history from session
    history = session.get('history', [])
    return render_template('index.html', table_names=table_names, history=history)

@app.route('/execute', methods=['POST'])
def execute():
    sql_query = request.form['sql_query']
    queries = [q.strip() for q in sql_query.split(';') if q.strip()]
    results = []
    error_message = None

    for query in queries:
        try:
            result = db.session.execute(text(query))
            db.session.commit()
            if result.returns_rows:
                result_data = result.fetchall()
                column_names = result.keys()
                results.append({
                    'data': result_data,
                    'columns': column_names
                })
            else:
                results.append({
                    'message': "Query executed successfully."
                })
        except Exception as e:
            error_message = str(e)
            break  # Stop executing on the first error

    # Get history from session and add the current queries
    history = session.get('history', [])
    history.extend(queries)
    session['history'] = history

    return render_template('index.html', results=results, error_message=error_message, sql_query=sql_query, history=history)

@app.route('/reset', methods=['POST'])
def reset():
    try:
        tables = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
        for table in tables:
            db.session.execute(text(f"DROP TABLE IF EXISTS {table[0]}"))
        db.session.commit()
        message = "All tables have been reset."
    except Exception as e:
        message = f"An error occurred: {str(e)}"
    
    return render_template('index.html', result_message=message)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
