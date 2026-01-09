# EventLink System Manual

## 📋 Overview
EventLink is a complete event management platform that allows users to browse, purchase tickets, and organizers to create and manage events. The system includes modern payment processing, QR code ticketing, and comprehensive user management.

## ⚙️ Required Tools & Applications

### Essential Software:
- **Python 3.8+** - Core programming language
- **Git** - Version control system
- **Text Editor/IDE** - VS Code, PyCharm, or Sublime Text recommended
- **Web Browser** - Chrome, Firefox, or Safari for testing

### Python Packages (Automatically installed):
- Flask - Web framework
- Jinja2 - Template engine
- SQLite3 - Database engine
- Bootstrap 5 - Frontend framework
- Werkzeug - WSGI utility library

## 🚀 Quick Setup Guide

### 1. Initial Setup
```bash
# Clone or download the project files
# Navigate to project directory
cd eventlink

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Mac/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install required packages
pip install flask
```

### 2. Running the Application
```bash
# Make sure virtual environment is activated
# Run the application
python3 app.py

# Open browser and go to:
http://localhost:5011
```

## 🎯 System Features

### For Regular Users:
- **Browse Events** - View all available events
- **Purchase Tickets** - Buy tickets with credit/debit card
- **View Tickets** - Access purchased tickets with QR codes
- **Profile Management** - Update personal information
- **Settings** - Manage preferences and payment methods

### For Event Organizers:
- **Create Events** - Add new events with details
- **Manage Events** - Edit/delete existing events
- **View Payments** - Track revenue and request payouts
- **Profile & Settings** - All user features plus organizer options

## 📱 Step-by-Step Usage

### Getting Started:
1. **Sign Up/Log In**
   - Visit the homepage
   - Click "Sign Up" to create account
   - Choose "User" or "Organizer" role
   - Log in with your credentials

2. **Browsing Events**
   - Click "Events" in navigation
   - View event cards with images and details
   - Filter by categories (Music, Food, Sports, etc.)

3. **Purchasing Tickets**
   - Click on any event to view details
   - Click "Checkout" button
   - Enter card details (mandatory)
   - Confirm purchase
   - View ticket with QR code in "My Tickets"

4. **Managing Profile**
   - Click "Profile" in sidebar
   - View personal information and stats
   - Update details as needed

5. **Configuring Settings**
   - Click "Settings" in sidebar
   - Navigate through different tabs:
     - Account Settings
     - Notifications
     - Privacy & Security
     - Preferences
     - Payment Methods
     - Organizer Settings (organizers only)

### For Organizers:

1. **Creating Events**
   - From dashboard, click "Create Event"
   - Fill in event details:
     - Title and description
     - Location and date/time
     - Price and capacity
     - Category and image
   - Click "Publish"

2. **Managing Events**
   - Go to "My Events" section
   - View all created events
   - Edit or delete events as needed

3. **Tracking Payments**
   - Click "Payments" in sidebar
   - View revenue breakdown by event
   - Request payouts to bank account/PayPal
   - Track financial performance

## 💳 Payment System

### Adding Payment Methods:
1. Go to Settings → Payment Methods
2. Enter card details:
   - Cardholder name
   - Card number (16 digits)
   - Expiry date (MM/YY)
   - CVV (3-4 digits)
3. Click "Save Payment Method"

### Purchasing Tickets:
1. Card details are **mandatory** for all purchases
2. System validates card format automatically
3. 10% service fee added to ticket price
4. Successful purchase generates QR code ticket

## 🎫 Ticket Management

### Viewing Tickets:
- Access "My Tickets" from sidebar
- Each ticket shows:
  - Event details
  - Purchase information
  - QR code for scanning
  - Ticket ID

### Using Tickets:
- Present QR code at event entrance
- Tickets are linked to your account
- Cannot be transferred to others

## 🔧 Technical Information

### Database Structure:
- **users** - User accounts and profiles
- **events** - Event listings and details
- **tickets** - Ticket purchases with QR codes
- **categories** - Event categories

### Key Routes:
- `/` - Homepage/Dashboard
- `/login` - User authentication
- `/events` - Browse all events
- `/event/<id>` - Event details
- `/checkout/<id>` - Purchase tickets
- `/my_tickets` - View purchased tickets
- `/profile` - User profile
- `/settings` - Account settings
- `/payments` - Organizer payments (organizers only)

### Security Features:
- Password hashing
- Session management
- Card data masking
- Role-based access control
- SQL injection prevention

## 🛠️ Troubleshooting

### Common Issues:

**Database Locked Error:**
- Solution: Restart the application
- Prevention: Close all database connections properly

**Payment Processing Failures:**
- Ensure card number is 16 digits
- Check expiry date format (MM/YY)
- Verify all fields are filled

**Login Problems:**
- Check username/password combination
- Ensure account is activated
- Clear browser cache/cookies

### Development Tips:
- Always activate virtual environment before running
- Check terminal for error messages
- Use browser developer tools for frontend debugging
- Test both user and organizer flows

## 📞 Support Information

For issues or questions:
1. Check this manual first
2. Review error messages in terminal
3. Verify all required tools are installed
4. Ensure proper file permissions

## 🔄 Updates & Maintenance

### Keeping the System Updated:
- Regularly pull latest code changes
- Update Python packages when notified
- Backup database before major changes
- Test all features after updates

### Database Management:
- Database file: `eventlink.db`
- Automatically created on first run
- Contains all user and event data
- Should be backed up regularly

---

**Happy Event Managing!** 🎉

*This manual covers all essential aspects of using the EventLink system. For advanced customization or development questions, please consult the source code documentation.*