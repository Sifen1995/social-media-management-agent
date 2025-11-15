# Deployment Guide - Render

This guide will help you deploy the Social Media Management Agent to Render.

## Prerequisites

- GitHub account with this repository
- Render account (sign up at https://render.com)
- Gemini API key from Google AI Studio

## Deployment Steps

### Option 1: Automatic Deployment with render.yaml (Recommended)

1. **Fork/Push this repository to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Sign in to Render**
   - Go to https://dashboard.render.com
   - Sign in with GitHub

3. **Create New Blueprint**
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select this repository
   - Render will automatically detect `render.yaml`

4. **Configure Environment Variables**
   - In the Render dashboard, go to your backend service
   - Add environment variable:
     - `GEMINI_API_KEY`: Your Google Gemini API key

5. **Deploy**
   - Click "Apply" to deploy both services
   - Wait for deployment to complete (5-10 minutes)

6. **Access Your App**
   - Frontend URL: `https://social-media-agent-frontend.onrender.com`
   - Backend API: `https://social-media-agent-api.onrender.com`

### Option 2: Manual Deployment

#### Deploy Backend API

1. **Create Web Service**
   - Go to Render Dashboard
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `social-media-agent-api`
     - **Region**: Oregon (or closest)
     - **Branch**: `main`
     - **Root Directory**: `agent`
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements-render.txt`
     - **Start Command**: `python simple_api.py`

2. **Add Environment Variables**
   - `GEMINI_API_KEY`: Your Gemini API key
   - `LLM_PROVIDER`: `gemini`
   - `DEFAULT_MODEL`: `gemini-flash-latest`
   - `LLM_MAX_TOKENS`: `8192`

3. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment

#### Deploy Frontend

1. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect the same repository
   - Configure:
     - **Name**: `social-media-agent-frontend`
     - **Region**: Same as backend
     - **Branch**: `main`
     - **Root Directory**: `frontend`
     - **Runtime**: Node
     - **Build Command**: `npm install && npm run build`
     - **Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`

2. **Add Environment Variables**
   - `VITE_API_URL`: `https://social-media-agent-api.onrender.com/api/v1`
   - (Replace with your actual backend URL)

3. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment

## Post-Deployment

### Test Your Deployment

1. Visit your frontend URL
2. Login with any credentials (demo mode)
3. Generate AI content to verify Gemini integration

### Update Frontend API URL

If you deployed manually, you need to update the frontend's API URL:

1. Go to frontend service settings
2. Update `VITE_API_URL` to your backend URL
3. Trigger redeployment

## Important Notes

### Free Tier Limitations

- Services spin down after 15 minutes of inactivity
- First request after spin-down will be slow (~30 seconds)
- 750 hours/month free (enough for one service 24/7)

### Production Considerations

For production use, consider:

1. **Database**: Add PostgreSQL (currently using in-memory storage)
2. **Redis**: Add Redis for caching and session management
3. **Environment Variables**: Use Render's secret files for sensitive data
4. **Custom Domain**: Connect your own domain
5. **Upgrade Plan**: For always-on services and better performance

## Troubleshooting

### Build Failures

- Check build logs in Render dashboard
- Verify `requirements-render.txt` has all dependencies
- Ensure Python version compatibility

### CORS Errors

- Verify frontend URL is allowed in `simple_api.py`
- Check environment variables are set correctly

### API Connection Issues

- Ensure `VITE_API_URL` points to correct backend URL
- Verify backend service is running
- Check backend logs for errors

### Gemini API Errors

- Verify `GEMINI_API_KEY` is set correctly
- Check API key has proper permissions
- Monitor quota usage in Google AI Studio

## Monitoring

- View logs in Render dashboard
- Set up alerts for service failures
- Monitor API usage in Google AI Studio

## Updating

To update your deployment:

```bash
git add .
git commit -m "Update description"
git push origin main
```

Render will automatically redeploy on push to main branch.

## Support

- Render Documentation: https://render.com/docs
- GitHub Issues: https://github.com/Sifen1995/social-media-management-agent/issues
