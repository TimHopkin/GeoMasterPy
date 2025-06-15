# 🌐 Netlify Deployment Guide

## 🚀 **Quick Deploy Options**

### **Option 1: One-Click Deploy (Easiest)**
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/TimHopkin/GeoMasterPy)

### **Option 2: Manual GitHub Deploy**

1. **Go to** [netlify.com](https://netlify.com)
2. **Sign up/Login** with GitHub
3. **Click** "New site from Git"
4. **Choose** "GitHub" 
5. **Select** repository: `TimHopkin/GeoMasterPy`
6. **Configure:**
   - **Build command:** (leave empty)
   - **Publish directory:** `src/web`
   - **Branch:** `main`
7. **Deploy!**

### **Option 3: Drag & Drop Deploy**

1. **Download** the HTML file from your repo
2. **Go to** [netlify.com](https://netlify.com) 
3. **Drag the file** to the deploy area
4. **Instant deployment!**

## 🎯 **What You Get**

- **Lightning fast** static hosting
- **Free HTTPS** with custom domain support
- **Global CDN** for worldwide access
- **Automatic deploys** from GitHub
- **Perfect rendering** of the Land App

## 🌟 **Alternative Hosting Options**

### **Vercel**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repo
3. Set **Framework**: Other
4. Set **Root Directory**: `src/web`  
5. Deploy!

### **GitHub Pages**
1. Go to your repo settings
2. Enable GitHub Pages
3. Set source to `src/web` folder
4. Access at: `timhopkin.github.io/GeoMasterPy`

### **Firebase Hosting**
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login and init
firebase login
firebase init hosting

# Set public directory to: src/web
# Deploy
firebase deploy
```

## 📋 **Benefits Over Streamlit**

- ✅ **Native HTML performance** - no iframe limitations
- ✅ **Perfect responsive design** - mobile friendly  
- ✅ **Instant loading** - no Python backend needed
- ✅ **Offline capable** - works without internet
- ✅ **Better UX** - designed for web browsers
- ✅ **Free hosting** - no server costs
- ✅ **Custom domains** - professional URLs

## 🔧 **Custom Domain Setup**

Once deployed on Netlify:
1. **Buy domain** (e.g., `yourlandapp.com`)
2. **Add custom domain** in Netlify settings
3. **Update DNS** to point to Netlify
4. **Free SSL** automatically enabled

## 🎪 **Demo URLs**

After deployment, your Land App will be available at URLs like:
- `https://your-land-app.netlify.app`
- `https://landapp.yourname.com` (custom domain)

**Recommended:** Use Netlify for the best user experience! 🚀