# 🎓 Fun Learning Platform

A comprehensive, gamified learning platform where learners, experts, and moderators connect through live keynotes, recorded sessions, articles, and community interactions.

## 🚀 Project Overview

**Fun Learning Platform** is an interactive edtech solution that combines:
- **Live Learning Sessions** with real-time interaction
- **Community-Driven Discussions** and knowledge sharing
- **Gamification System** with points, badges, and leaderboards
- **Mentorship Programs** for personalized guidance
- **Career Development** tools and job opportunities
- **Comprehensive Notification System** for engagement

## 🏗️ Architecture

### Backend Stack
- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **JWT Authentication** - Secure user management
- **Djoser** - User registration and management

### Frontend Stack (Planned)
- **React** - Dynamic user interface
- **Material-UI/Tailwind** - Modern design system
- **WebRTC** - Real-time video communication

## 📱 Core Features

### 1. User Management & Authentication
- **Custom User Model** with email-based authentication
- **Profile Management** with academic/professional information
- **Alumni Verification** system
- **Role-based Access Control** (Speaker, Moderator, Listener)

### 2. Learning Sessions
- **Session Scheduling** and management
- **Live Video Integration** (Zoom, Google Meet)
- **Recording Management** with searchable archives
- **Feedback & Rating** system
- **Session Analytics** and insights

### 3. Community System
- **Institution-based Communities** (JKUAT, Strathmore, etc.)
- **Subject Matter Communities** (Web Dev, AI/ML, DevOps)
- **Discussion Forums** with topics and posts
- **Knowledge Articles** and blog posts
- **Community Moderation** tools

### 4. Gamification Engine
- **Points System** for various activities
- **Badge System** with rarity levels
- **Leaderboards** (community and global)
- **Achievement Tracking** and milestones
- **Progress Visualization**

### 5. Mentorship Platform
- **Mentor-Mentee Matching**
- **Session Scheduling** and tracking
- **Goal Setting** and progress monitoring
- **Feedback System** for relationships
- **Mentorship Programs** management

### 6. Career Development
- **Job Postings** and opportunities
- **Skill Management** and validation
- **Career Paths** and progression tracking
- **Professional Networking** tools
- **Portfolio Building**

### 7. Notification System
- **Multi-channel Notifications** (email, in-app)
- **Smart Scheduling** with quiet hours
- **Personalized Preferences** per user
- **Real-time Updates** for engagement

## 🗂️ Project Structure

```
backend/
├── funlearning/          # Django project settings
├── users/               # User management & profiles
├── sessions/            # Learning sessions & recordings
├── communities/         # Community management
├── mentorship/          # Mentorship programs
├── career/             # Career development tools
└── requirements.txt    # Python dependencies

frontend/               # React frontend (planned)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Node.js 16+ (for frontend)
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd learning-systen
   ```

2. **Set up virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp env.example .env
   # Edit .env with your database and email settings
   ```

5. **Database setup**
   ```bash
   # Create PostgreSQL database
   createdb funlearning_db
   
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup (Planned)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=funlearning_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Points System
POINTS_SESSION_HOSTED=50
POINTS_SESSION_ATTENDED=10
POINTS_SESSION_MODERATED=30
POINTS_ARTICLE_PUBLISHED=25
POINTS_COMMUNITY_CONTRIBUTION=5
```

## 📊 Points System

### Earning Points
- **Host a Session**: +50 points
- **Moderate a Session**: +30 points
- **Attend a Session**: +10 points
- **Publish Article**: +25 points
- **Community Contribution**: +5 points

### Badge System
- **Common**: Basic participation badges
- **Uncommon**: Achievement-based badges
- **Rare**: Milestone badges
- **Epic**: Special recognition badges
- **Legendary**: Exceptional contribution badges

## 🔐 User Roles

### Speaker
- Deliver keynote sessions and workshops
- Earn points for each session hosted
- Build credibility and reputation
- Access to speaker analytics

### Moderator
- Assist speakers during sessions
- Fact-check content and manage Q&A
- Earn points for moderation
- Help maintain community quality

### Listener
- Attend live sessions and watch recordings
- Participate in community discussions
- Earn points for engagement
- Build learning portfolio

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/me/` - Current user profile

### Sessions
- `GET /api/sessions/` - List all sessions
- `POST /api/sessions/` - Create new session
- `GET /api/sessions/{id}/` - Get session details
- `PUT /api/sessions/{id}/` - Update session
- `DELETE /api/sessions/{id}/` - Delete session

### Communities
- `GET /api/communities/` - List communities
- `POST /api/communities/` - Create community
- `GET /api/communities/{id}/` - Get community details
- `POST /api/communities/{id}/join/` - Join community

### Mentorship
- `GET /api/mentorship/programs/` - List programs
- `POST /api/mentorship/relationships/` - Create relationship
- `GET /api/mentorship/sessions/` - List sessions

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test sessions
python manage.py test communities
```

### Test Coverage
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🚧 Development Status

### Completed ✅
- [x] Django project structure
- [x] Custom user models
- [x] Database models for all apps
- [x] Authentication system
- [x] Points and gamification system
- [x] Notification system

### In Progress 🔄
- [ ] API endpoints and serializers
- [ ] Frontend React application
- [ ] Video integration
- [ ] Email notifications

### Planned 📋
- [ ] Mobile application
- [ ] Advanced analytics
- [ ] AI-powered features
- [ ] Payment integration
- [ ] Multi-language support

## 🎯 Roadmap

### Phase 1: MVP (Current)
- Core user management
- Basic session management
- Community features
- Points system

### Phase 2: Enhanced Features
- Advanced video integration
- Mobile app
- Advanced analytics
- Payment system

### Phase 3: Scale & Optimize
- Performance optimization
- Advanced AI features
- Enterprise features
- International expansion

---

**Built with ❤️ for the learning community**
