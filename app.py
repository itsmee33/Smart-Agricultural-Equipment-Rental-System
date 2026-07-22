from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vibhas@33'
app.config['MYSQL_DB'] = 'farm_rental'

mysql = MySQL(app)

#  LANDING PAGE
@app.route('/')
def home():
    if 'loggedin' in session:
        if session['role'] == 'admin':
            return redirect(url_for('dashboard_admin'))
        if session['role'] == 'owner':
            return redirect(url_for('dashboard_owner'))
        return redirect(url_for('dashboard_farmer'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM equipment')
    equip_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'farmer'")
    farmer_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'Confirmed'")
    booking_count = cursor.fetchone()[0]
    cursor.execute('SELECT DISTINCT category FROM equipment ORDER BY category')
    categories = [row[0] for row in cursor.fetchall()]
    return render_template('index.html', equip_count=equip_count,
        farmer_count=farmer_count, booking_count=booking_count, categories=categories)

#  LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id']       = account[0]
            session['username'] = account[1]
            session['role']     = account[3]
            flash(f'Welcome back, {account[1]}!', 'success')
            if account[3] == 'admin':
                return redirect(url_for('dashboard_admin'))
            if account[3] == 'owner':
                return redirect(url_for('dashboard_owner'))
            return redirect(url_for('dashboard_farmer'))
        else:
            flash('Incorrect username or password. Please try again.', 'error')
    return render_template('login.html')

# REGISTRATION
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role     = request.form['role']
        contact  = request.form['contact']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            flash('That username is already taken. Please choose another.', 'error')
            return render_template('register.html')
        cursor.execute('INSERT INTO users (username, password, role, contact) VALUES (%s, %s, %s, %s)',
            (username, password, role, contact))
        mysql.connection.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# OWNER DASHBOARD
@app.route('/owner')
def dashboard_owner():
    if 'role' not in session or session['role'] != 'owner':
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM equipment WHERE owner_id = %s ORDER BY id DESC', (session['id'],))
    my_equip = cursor.fetchall()
    cursor.execute('''
        SELECT b.id, e.name, u.username, b.start_date, b.end_date,
               b.total_price, b.status, u.contact
        FROM bookings b
        JOIN equipment e ON b.equipment_id = e.id
        JOIN users u ON b.farmer_id = u.id
        WHERE e.owner_id = %s ORDER BY b.id DESC
    ''', (session['id'],))
    requests = cursor.fetchall()
    cursor.execute('''SELECT COALESCE(SUM(b.total_price),0) FROM bookings b
        JOIN equipment e ON b.equipment_id=e.id
        WHERE e.owner_id=%s AND b.status='Confirmed' ''', (session['id'],))
    total_earned = float(cursor.fetchone()[0])
    cursor.execute('''SELECT COALESCE(SUM(b.total_price),0) FROM bookings b
        JOIN equipment e ON b.equipment_id=e.id
        WHERE e.owner_id=%s AND b.status='Confirmed'
        AND MONTH(b.start_date)=MONTH(CURDATE()) AND YEAR(b.start_date)=YEAR(CURDATE())''', (session['id'],))
    monthly_earned = float(cursor.fetchone()[0])
    cursor.execute('''SELECT COALESCE(SUM(b.total_price),0) FROM bookings b
        JOIN equipment e ON b.equipment_id=e.id
        WHERE e.owner_id=%s AND b.status='Pending' ''', (session['id'],))
    pending_income = float(cursor.fetchone()[0])
    cursor.execute('''
        SELECT DATE_FORMAT(b.start_date,'%%b %%Y'), COALESCE(SUM(b.total_price),0)
        FROM bookings b JOIN equipment e ON b.equipment_id=e.id
        WHERE e.owner_id=%s AND b.status='Confirmed'
        AND b.start_date>=DATE_SUB(CURDATE(),INTERVAL 6 MONTH)
        GROUP BY DATE_FORMAT(b.start_date,'%%b %%Y'), YEAR(b.start_date), MONTH(b.start_date)
        ORDER BY YEAR(b.start_date), MONTH(b.start_date)
    ''', (session['id'],))
    monthly_data = cursor.fetchall()
    return render_template('dashboard_owner.html', equipment=my_equip, requests=requests,
        total_earned=total_earned, monthly_earned=monthly_earned,
        pending_income=pending_income, monthly_data=monthly_data)

# ADD EQUIPMENT
@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    if 'role' not in session or session['role'] != 'owner':
        return redirect(url_for('login'))
    if request.method == 'POST':
        name=request.form['name']; category=request.form['category']
        price=request.form['price']; desc=request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO equipment (owner_id,name,category,description,price_per_hour) VALUES (%s,%s,%s,%s,%s)',
            (session['id'],name,category,desc,price))
        mysql.connection.commit()
        flash(f'"{name}" listed successfully!', 'success')
        return redirect(url_for('dashboard_owner'))
    return render_template('add_equipment.html')

#  EDIT EQUIPMENT
@app.route('/edit_equipment/<int:equip_id>', methods=['GET', 'POST'])
def edit_equipment(equip_id):
    if 'role' not in session or session['role'] != 'owner':
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        name=request.form['name']; category=request.form['category']
        price=request.form['price']; desc=request.form['description']
        cursor.execute('UPDATE equipment SET name=%s,category=%s,price_per_hour=%s,description=%s WHERE id=%s AND owner_id=%s',
            (name,category,price,desc,equip_id,session['id']))
        mysql.connection.commit()
        flash('Equipment updated!', 'success')
        return redirect(url_for('dashboard_owner'))
    cursor.execute('SELECT * FROM equipment WHERE id=%s AND owner_id=%s', (equip_id, session['id']))
    item = cursor.fetchone()
    if not item:
        flash('Equipment not found.', 'error')
        return redirect(url_for('dashboard_owner'))
    return render_template('edit_equipment.html', item=item)

#  DELETE EQUIPMENT
@app.route('/delete_equipment/<int:equip_id>', methods=['POST'])
def delete_equipment(equip_id):
    if 'role' not in session or session['role'] != 'owner':
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE bookings SET status='Cancelled' WHERE equipment_id=%s AND status='Pending'", (equip_id,))
    cursor.execute('DELETE FROM equipment WHERE id=%s AND owner_id=%s', (equip_id, session['id']))
    mysql.connection.commit()
    flash('Equipment removed from your listings.', 'success')
    return redirect(url_for('dashboard_owner'))

#  FARMER DASHBOARD
@app.route('/farmer')
def dashboard_farmer():
    if 'role' not in session or session['role'] != 'farmer':
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    search   = request.args.get('search','').strip()
    category = request.args.get('category','').strip()
    query = '''
        SELECT e.id, e.owner_id, e.name, e.category, e.description,
               e.price_per_hour, u.username, u.contact
        FROM equipment e JOIN users u ON e.owner_id=u.id
        WHERE e.id NOT IN (SELECT equipment_id FROM bookings WHERE status='Confirmed')
    '''
    params = []
    if search:
        query += ' AND (e.name LIKE %s OR e.description LIKE %s OR e.category LIKE %s)'
        params += [f'%{search}%', f'%{search}%', f'%{search}%']
    if category:
        query += ' AND e.category=%s'
        params.append(category)
    query += ' ORDER BY e.id DESC'
    cursor.execute(query, params)
    all_equipment = cursor.fetchall()
    cursor.execute('SELECT DISTINCT category FROM equipment ORDER BY category')
    categories = [row[0] for row in cursor.fetchall()]
    cursor.execute('''
        SELECT e.name, b.start_date, b.end_date, b.total_price, b.status, b.id
        FROM bookings b JOIN equipment e ON b.equipment_id=e.id
        WHERE b.farmer_id=%s ORDER BY b.id DESC
    ''', (session['id'],))
    my_bookings = cursor.fetchall()
    return render_template('dashboard_farmer.html',
        equipment=all_equipment, my_bookings=my_bookings,
        categories=categories, search=search, active_category=category)

#  BOOK EQUIPMENT
@app.route('/book/<int:equip_id>', methods=['GET', 'POST'])
def book_equipment(equip_id):
    if 'role' not in session or session['role'] != 'farmer':
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date   = request.form['end_date']
        cursor.execute('''
            SELECT COUNT(*) FROM bookings
            WHERE equipment_id=%s AND status='Confirmed'
            AND NOT (end_date < %s OR start_date > %s)
        ''', (equip_id, start_date, end_date))
        if cursor.fetchone()[0] > 0:
            flash('Those dates conflict with an existing confirmed booking. Please choose other dates.', 'error')
            cursor.execute('SELECT e.*,u.username,u.contact FROM equipment e JOIN users u ON e.owner_id=u.id WHERE e.id=%s', (equip_id,))
            item = cursor.fetchone()
            cursor.execute("SELECT start_date,end_date FROM bookings WHERE equipment_id=%s AND status='Confirmed'", (equip_id,))
            return render_template('book_equipment.html', item=item, booked_ranges=cursor.fetchall())
        days  = (datetime.strptime(end_date,'%Y-%m-%d') - datetime.strptime(start_date,'%Y-%m-%d')).days + 1
        cursor.execute('SELECT price_per_hour FROM equipment WHERE id=%s', (equip_id,))
        rate        = float(cursor.fetchone()[0])
        total_price = rate * 8 * days
        cursor.execute('INSERT INTO bookings (equipment_id,farmer_id,start_date,end_date,total_price) VALUES (%s,%s,%s,%s,%s)',
            (equip_id, session['id'], start_date, end_date, total_price))
        mysql.connection.commit()
        flash('Booking request sent! The owner will review it shortly.', 'success')
        return redirect(url_for('dashboard_farmer'))
    cursor.execute('SELECT e.*,u.username,u.contact FROM equipment e JOIN users u ON e.owner_id=u.id WHERE e.id=%s', (equip_id,))
    item = cursor.fetchone()
    cursor.execute("SELECT start_date,end_date FROM bookings WHERE equipment_id=%s AND status='Confirmed'", (equip_id,))
    booked_ranges = cursor.fetchall()
    return render_template('book_equipment.html', item=item, booked_ranges=booked_ranges)

# ACCEPT / REJECT
@app.route('/accept/<int:booking_id>')
def accept_booking(booking_id):
    if 'role' not in session or session['role'] != 'owner':
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE bookings SET status="Confirmed" WHERE id=%s', (booking_id,))
    mysql.connection.commit()
    flash('Booking confirmed!', 'success')
    return redirect(url_for('dashboard_owner'))

@app.route('/reject/<int:booking_id>')
def reject_booking(booking_id):
    if 'role' not in session or session['role'] != 'owner':
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE bookings SET status="Cancelled" WHERE id=%s', (booking_id,))
    mysql.connection.commit()
    flash('Booking rejected.', 'success')
    return redirect(url_for('dashboard_owner'))

# CANCEL BOOKING (farmer)
@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'role' not in session or session['role'] != 'farmer':
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE bookings SET status='Cancelled' WHERE id=%s AND farmer_id=%s AND status='Pending'",
        (booking_id, session['id']))
    mysql.connection.commit()
    flash('Booking cancelled.', 'success')
    return redirect(url_for('dashboard_farmer'))

#  ADMIN MODULE 
def admin_required():
    return 'role' in session and session['role'] == 'admin'

#  ADMIN DASHBOARD
@app.route('/admin')
def dashboard_admin():
    if not admin_required():
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()

    # Platform stats
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='farmer'")
    total_farmers = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='owner'")
    total_owners = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM equipment")
    total_equipment = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]
    cursor.execute("SELECT COALESCE(SUM(total_price),0) FROM bookings WHERE status='Confirmed'")
    total_revenue = float(cursor.fetchone()[0])
    cursor.execute("SELECT COUNT(*) FROM bookings WHERE status='Pending'")
    pending_bookings = cursor.fetchone()[0]

    # All users
    cursor.execute("SELECT id, username, role, contact FROM users ORDER BY id DESC")
    all_users = cursor.fetchall()

    # All equipment
    cursor.execute("""
        SELECT e.id, e.name, e.category, e.price_per_hour, e.description, u.username
        FROM equipment e JOIN users u ON e.owner_id=u.id ORDER BY e.id DESC
    """)
    all_equipment = cursor.fetchall()

    # All bookings
    cursor.execute("""
        SELECT b.id, e.name, u_farmer.username, u_owner.username,
               b.start_date, b.end_date, b.total_price, b.status
        FROM bookings b
        JOIN equipment e ON b.equipment_id=e.id
        JOIN users u_farmer ON b.farmer_id=u_farmer.id
        JOIN users u_owner ON e.owner_id=u_owner.id
        ORDER BY b.id DESC
    """)
    all_bookings = cursor.fetchall()

    # Monthly revenue last 6 months
    cursor.execute("""
        SELECT DATE_FORMAT(start_date,'%%b %%Y'), COALESCE(SUM(total_price),0)
        FROM bookings WHERE status='Confirmed'
        AND start_date>=DATE_SUB(CURDATE(),INTERVAL 6 MONTH)
        GROUP BY DATE_FORMAT(start_date,'%%b %%Y'), YEAR(start_date), MONTH(start_date)
        ORDER BY YEAR(start_date), MONTH(start_date)
    """)
    monthly_data = cursor.fetchall()

    return render_template('dashboard_admin.html',
        total_farmers=total_farmers, total_owners=total_owners,
        total_equipment=total_equipment, total_bookings=total_bookings,
        total_revenue=total_revenue, pending_bookings=pending_bookings,
        all_users=all_users, all_equipment=all_equipment,
        all_bookings=all_bookings, monthly_data=monthly_data)

#  ADMIN – DELETE USER
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    if not admin_required():
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    # Cancel their bookings
    cursor.execute("UPDATE bookings SET status='Cancelled' WHERE farmer_id=%s AND status='Pending'", (user_id,))
    # Remove their equipment listings
    cursor.execute("DELETE FROM equipment WHERE owner_id=%s", (user_id,))
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    mysql.connection.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('dashboard_admin'))

#  ADMIN – DELETE EQUIPMENT
@app.route('/admin/delete_equipment/<int:equip_id>', methods=['POST'])
def admin_delete_equipment(equip_id):
    if not admin_required():
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE bookings SET status='Cancelled' WHERE equipment_id=%s AND status='Pending'", (equip_id,))
    cursor.execute("DELETE FROM equipment WHERE id=%s", (equip_id,))
    mysql.connection.commit()
    flash('Equipment removed from platform.', 'success')
    return redirect(url_for('dashboard_admin'))

#  ADMIN – CANCEL ANY BOOKING
@app.route('/admin/cancel_booking/<int:booking_id>', methods=['POST'])
def admin_cancel_booking(booking_id):
    if not admin_required():
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE bookings SET status='Cancelled' WHERE id=%s", (booking_id,))
    mysql.connection.commit()
    flash('Booking cancelled by admin.', 'success')
    return redirect(url_for('dashboard_admin'))

#  ADMIN – CONFIRM ANY BOOKING
@app.route('/admin/confirm_booking/<int:booking_id>', methods=['POST'])
def admin_confirm_booking(booking_id):
    if not admin_required():
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE bookings SET status='Confirmed' WHERE id=%s", (booking_id,))
    mysql.connection.commit()
    flash('Booking confirmed by admin.', 'success')
    return redirect(url_for('dashboard_admin'))


#  LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
