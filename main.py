from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from flask import redirect, url_for


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS accounts (username TEXT, password TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS passwords (username TEXT, website TEXT, password TEXT)')
conn.close()


@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT website, password FROM passwords WHERE username = ?', (username,))
        password_entries = cursor.fetchall()
        conn.close()

        return render_template('home.html', username=username, passwords=password_entries)
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_credentials(username, password):
            session['username'] = username
            return redirect('/')
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')


def verify_credentials(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if user_exists(username):
           error = 'Username already exists. Please choose a different username.'
           return render_template('create_account.html', error=error)
        else:
             # Save the new user to the database
            save_account_details(username, password)
            flash('Account created successfully!', 'success')
            return redirect('/registration_success')

    return render_template('create_account.html',)

def user_exists(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_account_details(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()
    return True


@app.route('/registration_success')
def registration_success():
    return render_template('registration_success.html')


@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' in session:
        username = session['username']
        # Delete the account from the database
        delete_user(username)
        # Clear the session
        session.pop('username', None)
        # Redirect to the account deletion success page
        return redirect('/account_deleted')
    else:
        return redirect('/login')

@app.route('/account_deleted')
def account_deleted():
    return render_template('account_deleted.html')


def delete_user(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM accounts WHERE username = ?', (username,))
    conn.commit()
    conn.close()



@app.route('/add_password', methods=['GET', 'POST'])
def add_password():
    if 'username' in session:
        if request.method == 'POST':
            website = request.form['website']
            password = request.form['password']
            username = session['username']

            if password_exists(username, website):
                flash(f"Website '{website}' already exists in the database.", 'error')
            else:
                # Save the password to the database
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO passwords (username, website, password) VALUES (?, ?, ?)',
                               (username, website, password))
                conn.commit()
                conn.close()
                flash('Password saved successfully!', 'success')
                return redirect('/')

        return render_template('add_password.html')
    else:
        return redirect('/login')


def password_exists(username, website):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM passwords WHERE username = ? AND website = ?', (username, website))
    result = cursor.fetchone()
    conn.close()
    return result is not None


@app.route('/retrieve_password', methods=['GET', 'POST'])
def retrieve_password():
    if 'username' in session:
        if request.method == 'POST':
            website = request.form['website']
            username, password = retrieve_password_from_db(session['username'], website)
            if password:
                return render_template('retrieve_password.html', website=website, username=username, password=password)
            else:
                flash(f"No password found for {website}.", 'error')
 #               return redirect('/retrieve_password')
        return render_template('retrieve_password.html', website=None, username=None, password=None)
    return redirect('/login')


def retrieve_password_from_db(username, website):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM passwords WHERE username = ? AND website = ?', (username, website))
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)


@app.route('/edit_password', methods=['GET', 'POST'])
def edit_password():
    if 'username' in session:
        if request.method == 'POST':
            website = request.form['website']
            new_password = request.form['new_password']
            username = session['username']

            if password_exists(username, website):
                update_password_in_db(username, website, new_password)
                flash(f"Password for {website} updated successfully!", 'success')
                return redirect('/')
            else:
                flash(f"No password found for {website}", 'error')
                return redirect('/edit_password')
        return render_template('edit_password.html')
    else:
        return redirect('/login')

def update_password_in_db(username, website, new_password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE passwords SET password = ? WHERE username = ? AND website = ?',
                   (new_password, username, website))
    conn.commit()
    conn.close()


@app.route('/delete_password', methods=['GET', 'POST'])
def delete_password():
    if 'username' in session:
        if request.method == 'POST':
            website = request.form['website']
            username = session['username']
            if password_exists(username, website):
                delete_password_from_db(username, website,)
                flash(f"Password for {website} has been deleted.", 'success')
                return redirect('/')
            else:
                flash(f"No password found for {website}", 'error')
                return redirect('/delete_password')
        return render_template('delete_password.html')
    return redirect('/login')

def delete_password_from_db(username, website):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE username = ? AND website = ?', (username, website))
    conn.commit()
    conn.close()






if __name__ == '__main__':
    app.run(debug=True)





