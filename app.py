from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Change this for production
DB_NAME = "eventlink.db"

# --- Database Helper ---
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    # Users Table
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        role TEXT DEFAULT 'user'
    )''')
    
    # Events Table with enhanced fields
    conn.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        organizer_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        location TEXT NOT NULL,
        date_time TEXT NOT NULL,
        price REAL NOT NULL,
        capacity INTEGER,
        category TEXT,
        status TEXT DEFAULT 'active',
        image_url TEXT DEFAULT 'https://images.unsplash.com/photo-1566737236500-c8ac43014a67?auto=format&fit=crop&w=800&q=80',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organizer_id) REFERENCES users (id)
    )''')

    # Tickets Table
    conn.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event_id INTEGER,
        purchase_date TEXT,
        quantity INTEGER DEFAULT 1,
        qr_code TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (event_id) REFERENCES events (id)
    )''')
    
    # Categories table for better organization
    conn.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    )''')
    
    # Insert default categories if they don't exist
    default_categories = [
        ('Concert', 'Live music performances'),
        ('Conference', 'Professional conferences and seminars'),
        ('Workshop', 'Educational workshops and training'),
        ('Sports', 'Sporting events and competitions'),
        ('Arts', 'Art exhibitions and cultural events'),
        ('Food & Drink', 'Food festivals and culinary events'),
        ('Networking', 'Business networking events'),
        ('Other', 'Other types of events')
    ]
    
    for category_name, description in default_categories:
        try:
            conn.execute('INSERT INTO categories (name, description) VALUES (?, ?)', 
                        (category_name, description))
        except sqlite3.IntegrityError:
            pass  # Category already exists
    
    conn.commit()
    conn.close()

def populate_sample_events():
    """Populate database with realistic club and bar events"""
    conn = get_db()
    
    # Check if events already exist
    event_count = conn.execute('SELECT COUNT(*) FROM events').fetchone()[0]
    if event_count > 0:
        conn.close()
        return
    
    # Create a dummy organizer user if none exists
    user_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if user_count == 0:
        # Create dummy organizer
        from werkzeug.security import generate_password_hash
        dummy_password = generate_password_hash('dummy123')
        conn.execute('''
            INSERT INTO users (email, password, full_name, role)
            VALUES (?, ?, ?, ?)
        ''', ('organizer@eventlink.com', dummy_password, 'Event Organizer', 'organizer'))
        organizer_id = conn.execute('SELECT id FROM users WHERE email = ?', ('organizer@eventlink.com',)).fetchone()[0]
    else:
        # Use first user as organizer
        organizer_id = conn.execute('SELECT id FROM users LIMIT 1').fetchone()[0]
    
    # Realistic club/bar events with diverse images
    sample_events = [
        {
            'title': 'Midnight Jazz Sessions',
            'description': 'Intimate jazz night featuring local musicians. Cocktails and small plates served throughout the evening.',
            'location': 'Blue Note Lounge, Downtown District',
            'date_time': '2026-01-15 21:00',
            'price': 25.00,
            'capacity': 80,
            'category': 'Music',
            'image_url': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Electro Night Festival',
            'description': 'All-night electronic dance music festival with top DJs. Open bar until midnight.',
            'location': 'Club Pulse, Entertainment Quarter',
            'date_time': '2026-01-18 22:00',
            'price': 45.00,
            'capacity': 300,
            'category': 'Music',
            'image_url': 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Craft Beer Tasting',
            'description': 'Sample 20+ local craft beers with food pairings. Meet the brewers and learn about brewing techniques.',
            'location': 'Hop House Brewery, Industrial District',
            'date_time': '2026-01-20 18:30',
            'price': 35.00,
            'capacity': 60,
            'category': 'Food & Drink',
            'image_url': 'https://images.unsplash.com/photo-1585345242804-9c0f1b4a2c4d?auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Rooftop Sunset Cocktails',
            'description': 'Elegant rooftop party with signature cocktails and panoramic city views. Dress code: smart casual.',
            'location': 'Sky Lounge Hotel, Financial District',
            'date_time': '2026-01-22 17:00',
            'price': 60.00,
            'capacity': 120,
            'category': 'Food & Drink',
            'image_url': 'https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Live Acoustic Evening',
            'description': 'Relaxed acoustic performances in an intimate setting. Wine and cheese platters available.',
            'location': 'The Wooden Spoon, Arts District',
            'date_time': '2026-01-25 19:30',
            'price': 20.00,
            'capacity': 50,
            'category': 'Music',
            'image_url': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Whiskey Wednesday',
            'description': 'Premium whiskey tasting with master distiller. Learn about different whiskey varieties and aging processes.',
            'location': 'The Oak Barrel, Heritage Street',
            'date_time': '2026-01-29 19:00',
            'price': 40.00,
            'capacity': 40,
            'category': 'Food & Drink',
            'image_url': 'https://images.unsplash.com/photo-1609833055954-5c1e3dc20973?auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Latin Night Fiesta',
            'description': 'Vibrant Latin music and dance night. Professional instructors for salsa and bachata lessons.',
            'location': 'Casa Latina Club, Cultural Quarter',
            'date_time': '2026-02-01 20:30',
            'price': 30.00,
            'capacity': 150,
            'category': 'Music',
            'image_url': 'https://images.unsplash.com/photo-1509670811598-834b6d3be3b3?auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Champagne & Caviar Brunch',
            'description': 'Luxury brunch experience with premium champagne and caviar service. Live piano accompaniment.',
            'location': 'Grand Royale Hotel, Luxury District',
            'date_time': '2026-02-05 11:00',
            'price': 85.00,
            'capacity': 80,
            'category': 'Food & Drink',
            'image_url': 'https://images.unsplash.com/photo-1559847844-d8a8bf309bc8?auto=format&fit=crop&w=800&q=80'
        }
    ]
    
    # Insert sample events with proper organizer ID
    for event in sample_events:
        try:
            conn.execute('''
                INSERT INTO events (organizer_id, title, description, location, date_time, 
                                  price, capacity, category, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                organizer_id,
                event['title'],
                event['description'],
                event['location'],
                event['date_time'],
                event['price'],
                event['capacity'],
                event['category'],
                event['image_url']
            ))
        except sqlite3.Error as e:
            print(f"Error inserting event {event['title']}: {e}")
    
    conn.commit()
    conn.close()
    print(f"Added {len(sample_events)} sample events to database")

# Initialize DB immediately
with app.app_context():
    init_db()
    populate_sample_events()

# --- Routes ---

@app.route('/my_tickets')
def my_tickets():
    """Display user's purchased tickets with QR codes"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    
    # Get user's tickets with event details
    tickets = conn.execute('''
        SELECT t.*, e.title, e.date_time, e.location, e.price, e.image_url, u.full_name as organizer_name
        FROM tickets t
        JOIN events e ON t.event_id = e.id
        JOIN users u ON e.organizer_id = u.id
        WHERE t.user_id = ?
        ORDER BY e.date_time DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    return render_template('my_tickets.html', tickets=tickets)

@app.route('/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    # Get user's ticket statistics
    stats = conn.execute('''
        SELECT 
            COUNT(*) as total_tickets,
            SUM(e.price) as total_spent
        FROM tickets t
        JOIN events e ON t.event_id = e.id
        WHERE t.user_id = ?
    ''', (session['user_id'],)).fetchone()
    
    conn.close()
    
    return render_template('profile.html', user=user, stats=stats)

@app.route('/payments')
def payments():
    """Organizer payments dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') != 'organizer':
        flash('Access denied. Organizers only.')
        return redirect(url_for('dashboard'))
    
    conn = get_db()
    
    # Get organizer's events and payment data
    events_with_payments = conn.execute('''
        SELECT e.*, 
               COUNT(t.id) as ticket_count,
               SUM(t.quantity) as total_tickets_sold,
               SUM(e.price * t.quantity) as gross_revenue,
               SUM(e.price * t.quantity * 0.9) as net_revenue  -- 10% service fee
        FROM events e
        LEFT JOIN tickets t ON e.id = t.event_id
        WHERE e.organizer_id = ?
        GROUP BY e.id
        ORDER BY e.date_time DESC
    ''', (session['user_id'],)).fetchall()
    
    # Calculate totals
    total_gross = sum([event['gross_revenue'] or 0 for event in events_with_payments])
    total_net = sum([event['net_revenue'] or 0 for event in events_with_payments])
    total_fees = total_gross - total_net
    
    conn.close()
    
    return render_template('payments.html', 
                         events=events_with_payments,
                         total_gross=total_gross,
                         total_net=total_net,
                         total_fees=total_fees)

@app.route('/organizer_checkout', methods=['POST'])
def organizer_checkout():
    """Process organizer payout request"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session.get('role') != 'organizer':
        flash('Access denied. Organizers only.')
        return redirect(url_for('dashboard'))
    
    amount = float(request.form.get('amount', 0))
    destination = request.form.get('destination')
    
    if amount <= 0:
        flash('Invalid payout amount')
        return redirect(url_for('payments'))
    
    if amount < 10.00:
        flash('Minimum payout amount is $10.00')
        return redirect(url_for('payments'))
    
    # Simulate payout processing
    flash(f'Payout request for ${amount:.2f} to {destination} submitted successfully! Funds will be transferred within 3-5 business days.')
    return redirect(url_for('payments'))

@app.route('/settings')
def settings():
    """User settings page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('settings.html', user=user)

@app.route('/events')
def events_list():
    """Display all active events with filtering options"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    
    # Get filter parameters
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    
    # Build query with filters
    query = 'SELECT e.*, u.full_name as organizer_name FROM events e JOIN users u ON e.organizer_id = u.id WHERE e.status = ?'
    params = ['active']
    
    if category_filter:
        query += ' AND e.category = ?'
        params.append(category_filter)
    
    if search_query:
        query += ' AND (e.title LIKE ? OR e.description LIKE ? OR e.location LIKE ?)'
        search_term = f'%{search_query}%'
        params.extend([search_term, search_term, search_term])
    
    query += ' ORDER BY e.date_time ASC'
    
    events = conn.execute(query, params).fetchall()
    
    # Get all categories for filter dropdown
    categories = conn.execute('SELECT DISTINCT category FROM events WHERE status = ? AND category IS NOT NULL', ['active']).fetchall()
    
    conn.close()
    
    return render_template('events_list.html', events=events, categories=categories, 
                          current_category=category_filter, current_search=search_query)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    """Display detailed information about a specific event"""
    conn = get_db()
    
    # Get event with organizer info
    event = conn.execute('''
        SELECT e.*, u.full_name as organizer_name 
        FROM events e 
        JOIN users u ON e.organizer_id = u.id 
        WHERE e.id = ?
    ''', (event_id,)).fetchone()
    
    if not event:
        flash('Event not found')
        return redirect(url_for('events_list'))
    
    # Check if user has purchased ticket for this event
    has_ticket = False
    if 'user_id' in session:
        ticket = conn.execute('SELECT * FROM tickets WHERE user_id = ? AND event_id = ?', 
                             (session['user_id'], event_id)).fetchone()
        has_ticket = ticket is not None
    
    # Get ticket count for this event
    ticket_count = conn.execute('SELECT COUNT(*) as count FROM tickets WHERE event_id = ?', 
                               (event_id,)).fetchone()['count']
    
    conn.close()
    
    return render_template('event_detail.html', event=event, has_ticket=has_ticket, ticket_count=ticket_count)

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    """Edit an existing event (organizer only)"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    
    # Check if event exists and belongs to current user
    event = conn.execute('SELECT * FROM events WHERE id = ? AND organizer_id = ?', 
                        (event_id, session['user_id'])).fetchone()
    
    if not event:
        flash('Event not found or unauthorized')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Update event
        conn.execute('''
            UPDATE events 
            SET title = ?, description = ?, location = ?, date_time = ?, 
                price = ?, capacity = ?, category = ?, status = ?
            WHERE id = ? AND organizer_id = ?
        ''', (
            request.form['title'],
            request.form.get('description', ''),
            request.form['location'],
            request.form['date_time'],
            float(request.form['price']),
            int(request.form.get('capacity', 0)) if request.form.get('capacity') else None,
            request.form.get('category', ''),
            request.form.get('status', 'active'),
            event_id,
            session['user_id']
        ))
        conn.commit()
        conn.close()
        flash('Event updated successfully!')
        return redirect(url_for('dashboard'))
    
    # Get categories for dropdown
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    
    return render_template('edit_event.html', event=event, categories=categories)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    """Delete an event (organizer only)"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    
    # Check if event belongs to current user
    event = conn.execute('SELECT * FROM events WHERE id = ? AND organizer_id = ?', 
                        (event_id, session['user_id'])).fetchone()
    
    if not event:
        flash('Event not found or unauthorized')
        return redirect(url_for('dashboard'))
    
    # Delete event (this will cascade delete tickets due to foreign key constraint)
    conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    
    flash('Event deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = None
        try:
            conn = get_db()
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        finally:
            if conn:
                conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['full_name']
            session.modified = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            
    return render_template('login.html', mode='login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        full_name = request.form['full_name']
        
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, password, full_name) VALUES (?, ?, ?)',
                         (email, password, full_name))
            conn.commit()
            user_id = cursor.lastrowid
            print(f"DEBUG: User created with ID: {user_id}")
        except sqlite3.IntegrityError:
            if conn:
                conn.close()
            flash('Email already exists')
            return render_template('login.html', mode='signup')
        except Exception as e:
            if conn:
                conn.close()
            print(f"DEBUG: Database error: {e}")
            flash('An error occurred. Please try again.')
            return render_template('login.html', mode='signup')
        finally:
            if conn:
                conn.close()
        
        # Auto-login to set role
        session['user_id'] = user_id
        session['name'] = full_name
        session['role'] = 'pending'  # Temporary role until selection
        session.modified = True  # Explicitly mark session as modified
        print(f"DEBUG: User signed up with ID: {user_id}, Session: {dict(session)}")  # Debug line
        return redirect(url_for('select_role'))
            
    return render_template('login.html', mode='signup')

@app.route('/select_role', methods=['GET', 'POST'])
def select_role():
    print(f"DEBUG: Accessing select_role. Session: {dict(session)}")  # Debug line
    print(f"DEBUG: Request method: {request.method}")
    
    if 'user_id' not in session:
        print("DEBUG: No user_id in session, redirecting to login")
        flash('Please sign up first')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        role = request.form['role']
        print(f"DEBUG: Setting role to: {role} for user_id: {session['user_id']}")
        
        conn = None
        try:
            conn = get_db()
            conn.execute('UPDATE users SET role = ? WHERE id = ?', (role, session['user_id']))
            conn.commit()
        finally:
            if conn:
                conn.close()
        
        session['role'] = role
        session.modified = True  # Explicitly mark session as modified
        flash(f'Welcome! You are now registered as a {role}.')
        print(f"DEBUG: Role set successfully, session now: {dict(session)}")
        print(f"DEBUG: Redirecting to dashboard")
        return redirect(url_for('dashboard'))
        
    print("DEBUG: Rendering role selection form")
    return render_template('role_selection.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    conn = get_db()
    
    if session['role'] == 'organizer':
        events = conn.execute('SELECT * FROM events WHERE organizer_id = ?', (session['user_id'],)).fetchall()
        # Mock analytics
        revenue = sum([e['price'] for e in events]) * 15 
        attendees = len(events) * 15
        conn.close()
        return render_template('dashboard_org.html', events=events, revenue=revenue, attendees=attendees)
    
    else:
        # Show all events
        all_events = conn.execute('SELECT * FROM events').fetchall()
        # Show my tickets
        my_tickets = conn.execute('''
            SELECT t.*, e.title, e.date_time, e.location, e.price 
            FROM tickets t
            JOIN events e ON t.event_id = e.id
            WHERE t.user_id = ?
        ''', (session['user_id'],)).fetchall()
        conn.close()
        return render_template('dashboard_user.html', events=all_events, my_tickets=my_tickets)

@app.route('/create_event', methods=['POST'])
def create_event():
    if session.get('role') != 'organizer': return redirect(url_for('dashboard'))
    
    conn = get_db()
    conn.execute('''INSERT INTO events (organizer_id, title, description, location, date_time, price, capacity, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (session['user_id'], request.form['title'], request.form.get('description', ''), 
                  request.form['location'], request.form['date_time'], 
                  float(request.form['price']), 
                  int(request.form.get('capacity', 0)) if request.form.get('capacity') else None,
                  request.form.get('category', '')))
    conn.commit()
    conn.close()
    flash('Event created successfully!')
    return redirect(url_for('dashboard'))

@app.route('/checkout/<int:event_id>')
def checkout(event_id):
    """Display checkout page for event ticket purchase"""
    if 'user_id' not in session: return redirect(url_for('login'))
    
    conn = get_db()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    conn.close()
    
    if not event:
        flash('Event not found')
        return redirect(url_for('events_list'))
    
    return render_template('checkout.html', event=event)

@app.route('/save_payment_method', methods=['POST'])
def save_payment_method():
    """Save payment method in user settings"""
    if 'user_id' not in session: return redirect(url_for('login'))
    
    card_number = request.form.get('card_number')
    expiry_date = request.form.get('expiry_date')
    cvv = request.form.get('cvv')
    cardholder_name = request.form.get('cardholder_name')
    
    # Validate payment details
    if not all([card_number, expiry_date, cvv, cardholder_name]):
        flash('Please fill in all card details')
        return redirect(url_for('settings'))
    
    if len(card_number.replace(' ', '')) != 16:
        flash('Invalid card number')
        return redirect(url_for('settings'))
    
    # Store masked card info (in real app, this would be tokenized)
    masked_card = f"**** **** **** {card_number[-4:]}"
    
    conn = get_db()
    conn.execute('''
        UPDATE users SET 
        payment_method = ?,
        card_last_four = ?
        WHERE id = ?
    ''', (masked_card, card_number[-4:], session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Payment method saved successfully!')
    return redirect(url_for('settings'))

@app.route('/process_payment', methods=['POST'])
def process_payment():
    """Process card payment for event ticket"""
    if 'user_id' not in session: return redirect(url_for('login'))
    
    event_id = request.form.get('event_id')
    card_number = request.form.get('card_number')
    expiry_date = request.form.get('expiry_date')
    cvv = request.form.get('cvv')
    
    # Validate payment details (basic validation)
    if not all([event_id, card_number, expiry_date, cvv]):
        flash('Please fill in all payment details')
        return redirect(url_for('checkout', event_id=event_id))
    
    # Simulate payment processing
    if len(card_number.replace(' ', '')) != 16:
        flash('Invalid card number')
        return redirect(url_for('checkout', event_id=event_id))
    
    conn = get_db()
    
    # Generate QR code content
    import uuid
    qr_content = f"EVENTLINK-TICKET-{uuid.uuid4().hex[:8]}-{session['user_id']}-{event_id}"
    
    # Insert ticket
    conn.execute('INSERT INTO tickets (user_id, event_id, purchase_date, qr_code) VALUES (?, ?, ?, ?)',
                 (session['user_id'], event_id, datetime.now().strftime("%Y-%m-%d %H:%M"), qr_content))
    conn.commit()
    conn.close()
    
    flash('Payment successful! Ticket purchased.')
    return redirect(url_for('my_tickets'))

@app.route('/buy_ticket/<int:event_id>')
def buy_ticket(event_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    
    conn = get_db()
    # Generate QR code content (ticket ID + user ID + event ID)
    import uuid
    qr_content = f"EVENTLINK-TICKET-{uuid.uuid4().hex[:8]}-{session['user_id']}-{event_id}"
    
    conn.execute('INSERT INTO tickets (user_id, event_id, purchase_date, qr_code) VALUES (?, ?, ?, ?)',
                 (session['user_id'], event_id, datetime.now().strftime("%Y-%m-%d %H:%M"), qr_content))
    conn.commit()
    flash('Ticket purchased successfully!')
    return redirect(url_for('my_tickets'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5011))
    app.run(debug=True, host='0.0.0.0', port=port)