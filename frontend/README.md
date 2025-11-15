# Social Media Management Agent - Frontend

Modern React-based frontend interface for the AI-powered social media management agent system.

## Features

- 🤖 AI-powered content generation with Google Gemini
- 📊 Dashboard with performance metrics
- ✍️ Multi-platform content creator (Instagram, Facebook, Twitter, LinkedIn, TikTok)
- 📅 Content calendar and scheduling
- 📈 Analytics and insights dashboard
- 🎯 Brand management
- 🔗 Social account connections
- 🎨 Beautiful UI with Tailwind CSS

## Tech Stack

- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **Routing:** React Router v6
- **HTTP Client:** Axios
- **Icons:** React Icons
- **Notifications:** React Hot Toast

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable components
│   │   └── Layout.jsx  # Main layout with sidebar
│   ├── pages/          # Page components
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── ContentGenerator.jsx
│   │   ├── BrandManagement.jsx
│   │   ├── ContentCalendar.jsx
│   │   ├── Analytics.jsx
│   │   └── SocialAccounts.jsx
│   ├── services/       # API services
│   │   └── api.js      # Axios instance and API methods
│   ├── stores/         # Zustand stores
│   │   └── authStore.js
│   ├── App.jsx         # Main app component
│   ├── main.jsx        # Entry point
│   └── index.css       # Global styles
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Features Overview

### Authentication
- Login and registration
- JWT token-based authentication
- Protected routes
- Auto-redirect on session expiry

### Content Generation
- Select brand and platform
- Enter topic and content type
- Generate multiple variations
- Copy generated content
- AI-powered by Gemini

### Brand Management
- Create and manage multiple brands
- Set brand voice and target audience
- Define brand goals and niche
- Edit and delete brands

### Dashboard
- Overview of key metrics
- Quick actions
- Recent content preview
- Statistics cards

## API Integration

The frontend integrates with the backend API endpoints:

- `POST /auth/login` - User authentication
- `POST /auth/register` - User registration
- `GET /brands` - Get all brands
- `POST /content/generate` - Generate content with AI
- `GET /analytics/*` - Analytics data
- And more...

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License - see LICENSE file for details
