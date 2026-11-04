# ZivOps

Personal portfolio, infrastructure automation, and GitOps showcase maintained by [Ziv Hadady](https://github.com/zivhadady).

Live site: [zivhadady.github.io/zivops](https://zivhadady.github.io/zivops/)

---

## Overview

This repository houses the source code and automation for the ZivOps portfolio:

- **Frontend**: Jekyll-based static site with simulated interactive terminal and responsive dark UI.
- **CI/CD Pipeline**: GitHub Actions workflows for automated building, linting, and zero-downtime deployment to GitHub Pages.
- **Site Integrity Gate**: Custom Python script (`validate_links.py`) running in CI to enforce valid HTML tag structure and prevent broken links or missing assets prior to deployment.
- **Automation & GitOps**: Infrastructure automation showcase covering Ansible configurations, Kubernetes manifests, and Argo CD workflows.

---

## Repository Structure

```
.
├── .github/workflows/       # CI/CD pipelines
│   ├── deploy-pages.yml     # GitHub Pages build, validation & deployment
│   └── validate-links.yml   # PR site integrity checks
├── _layouts/                # Jekyll layout templates
├── assets/css/              # Stylesheets
├── _config.yml              # Jekyll site configuration
├── index.html               # Main portfolio landing page
├── setup.sh                 # Local environment bootstrapping script
└── validate_links.py        # Pre-deploy site integrity validator
```

---

## Local Development

### Prerequisites

- Ruby (>= 3.0) and Bundler (`gem install bundler`)
- Python 3.10+ (for running validation scripts)

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/zivhadady/zivops.git
   cd zivops
   ```

2. Run the environment setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   *Alternatively, configure Bundler manually:*
   ```bash
   bundle config set --local path 'vendor/bundle'
   bundle install
   ```

3. Launch the local Jekyll server:
   ```bash
   bundle exec jekyll serve --baseurl ""
   ```
   Open `http://127.0.0.1:4000/` in your browser.

---

## Quality Gates & Testing

To verify internal links and HTML structure before pushing:

```bash
# Validate against source directory or built site
python validate_links.py .
```

---

## License & Security

- For responsible vulnerability disclosures, refer to [SECURITY.md](SECURITY.md).
- Maintained by Ziv Hadady.
