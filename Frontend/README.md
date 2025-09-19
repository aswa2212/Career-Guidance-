# Student Guidance Platform

A modern, production-ready React.js application for student guidance and educational resources. Built with React, Tailwind CSS, Framer Motion, and Zustand for state management.

## 🚀 Features

- **Authentication System**: Secure login with form validation
- **Interactive Dashboard**: Stats cards, charts, and personalized recommendations
- **Aptitude Testing**: Multi-question MCQ quiz with progress tracking and results analysis
- **College Directory**: Filterable and searchable college listings with detailed information
- **Course Catalog**: Comprehensive course listings with career path visualizations
- **Resource Library**: Downloadable study materials and learning resources
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Optimized for all screen sizes
- **Accessibility**: ARIA labels, keyboard navigation, and focus management

## 🛠️ Tech Stack

- **Framework**: React.js 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Charts**: Recharts
- **Routing**: React Router DOM
- **State Management**: Zustand
- **Notifications**: React Hot Toast

## 📦 Installation

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

4. **Preview Production Build**:
   ```bash
   npm run preview
   ```

## 🎨 Design System

### Color Palette
- **Primary**: #4d041c (Deep Maroon)
- **Secondary**: #fbb6ce (Soft Rose)
- **Accent**: #a7f3d0 (Mint Green)
- **Background**: #ffffff (White) / #f3f4f6 (Light Gray)

### Typography
- **Font Family**: Inter, Poppins
- **Headings**: Bold, clean typography
- **Body Text**: Legible and accessible

### UI Components
- **Cards**: Rounded corners with soft shadows
- **Buttons**: Rounded with hover effects
- **Forms**: Clean inputs with validation
- **Navigation**: Sticky navbar with responsive design

## 📱 Pages

1. **Login Page** (`/login`)
   - Email/password authentication
   - Form validation
   - Animated transitions

2. **Dashboard** (`/dashboard`)
   - Welcome section
   - Quick stats cards
   - Recommended courses and colleges
   - Search functionality

3. **Aptitude Test** (`/aptitude-test`)
   - Multi-category questions
   - Progress tracking
   - Results visualization
   - Performance analytics

4. **College List** (`/colleges`)
   - Filterable college directory
   - Search by location, course, ranking
   - Detailed college information
   - Application deadlines

5. **Course List** (`/courses`)
   - Course catalog with filters
   - Career path visualization
   - Skill requirements
   - College recommendations

6. **Resources** (`/resources`)
   - Study materials library
   - Downloadable resources
   - Category-based filtering
   - Featured content

## 🔧 Configuration

### Environment Setup
The application uses Vite for development and building. Configuration files:
- `vite.config.js` - Vite configuration
- `tailwind.config.js` - Tailwind CSS configuration
- `postcss.config.js` - PostCSS configuration

### State Management
Zustand store (`src/store/useAppStore.js`) manages:
- User authentication
- Theme preferences (dark/light mode)
- Notifications
- Test results
- Search and filter states

## 🎯 Key Features

### Authentication
- Protected routes
- Persistent login state
- Demo credentials available

### Dark Mode
- System-wide theme toggle
- Persistent preference storage
- Smooth transitions

### Responsive Design
- Mobile-first approach
- Breakpoints: sm (480px), md (768px), lg (1024px), xl (1280px)
- Flexible grid layouts

### Accessibility
- ARIA labels and roles
- Keyboard navigation
- Focus management
- Screen reader support

## 🚀 Deployment

The application is ready for deployment to any static hosting service:
- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront

Build the project with `npm run build` and deploy the `dist` folder.

## 📝 Demo Credentials

For testing purposes, use:
- **Email**: demo@studyguide.com
- **Password**: demo123

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please contact the development team or create an issue in the repository.

---

Built with ❤️ for students worldwide
