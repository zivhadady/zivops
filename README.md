# ZivOps — DevOps & Cloud Architect Portfolio

A professional, high-performance static website architected for modern DevOps hosting, automated via Terraform, and deployed continuously with GitHub Actions.

---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
Ensure you have the following installed on your machine:
*   **Git**
*   **Ruby** (3.0 or higher)
*   **Bundler** (`gem install bundler`)
*   **Terraform** (for infrastructure management)

### 2. Auto Setup
Run the setup script from the root of the project to check prerequisites, configure the local Ruby environment, and install all dependencies:
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Run Locally
Start the Jekyll local development server:
```bash
bundle exec jekyll serve --baseurl ""
```
Once started, open your web browser and navigate to:
👉 **[http://127.0.0.1:4000/](http://127.0.0.1:4000/)**

---

## 🛠️ Deploying to GitHub Pages (Production)

This project features a fully automated CI/CD pipeline using GitHub Actions. 

### 1. First-Time Repository Setup
Ensure your GitHub repository is configured to use GitHub Actions for deployment:
1. Go to your repository on GitHub.
2. Navigate to **Settings** -> **Pages**.
3. Under **Build and deployment** -> **Source**, select **GitHub Actions** (instead of Deploy from a branch).

### 2. Deployment Workflow
To deploy updates to production, push or merge your changes into the `main` branch:

```bash
# Push your develop branch updates to remote
git push origin develop

# Merge develop into main and push to deploy
git checkout main
git pull origin main
git merge develop
git push origin main

# Switch back to develop to continue working
git checkout develop
```

As soon as changes are pushed to `main`, GitHub Actions will build and deploy the site automatically. You can track progress in the **Actions** tab of your repository.
