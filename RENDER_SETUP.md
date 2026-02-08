# Render Configuration for Deployment

## Environment Variables to Set in Render Dashboard:

1. **SECRET_KEY** (Required)
   - Value: A random secret key for Flask sessions
   - Example: `your-random-secret-key-here`

## How to set environment variables in Render:

1. Go to your Render service dashboard
2. Click "Settings" → "Environment"
3. Add these variables:
   - **Key:** SECRET_KEY
   - **Value:** (generate a random string)
4. Click "Save changes"
5. The app will auto-redeploy

## Database Note:

SQLite database (users.db) is stored on the instance's disk. 
It persists between restarts but will be reset if the service is restarted or destroyed.

For production, consider using PostgreSQL instead. Let me know if you need help setting that up!
