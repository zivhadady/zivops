# ZivOps

Personal portfolio and technical showcase maintained by **[Ziv Hadady](https://github.com/zivhadady)** — DevOps & Cloud Infrastructure Engineer (Tel Aviv-Yafo, Israel).

**Live Site:** [zivhadady.github.io/zivops](https://zivhadady.github.io/zivops/)  
**LinkedIn:** [linkedin.com/in/ziv-hadady-794aaa19a](https://www.linkedin.com/in/ziv-hadady-794aaa19a/)  
**Email:** [zhadady@gmail.com](mailto:zhadady@gmail.com) &bull; **Phone:** 050-290-3338

---

## Overview

This repository houses the source code and automation for the **ZivOps** portfolio, designed with a high-tech telemetry HUD interface and automated CI/CD:

- **Frontend**: Jekyll-based static site with responsive futuristic telemetry dashboard, tech stats, and interactive simulated terminal.
- **CI/CD Pipeline**: GitHub Actions workflows using `ruby/setup-ruby` for modern Jekyll build and zero-downtime deployment to GitHub Pages.
- **Site Integrity Gate**: Custom Python gate (`validate_links.py`) running in CI to enforce valid HTML tag balance and verify internal asset links before publishing.

---

## Core Technical Competencies

- **Cloud Platforms:** Microsoft Azure (VNets, VMs, Entra ID, Budgets, Cost Management), AWS (EC2, EKS, S3, VPC, ALB, IAM)
- **Containers & GitOps:** Docker, Kubernetes, Helm, RBAC, HPA, Argo CD, Rancher
- **CI/CD & IaC:** Jenkins, GitLab CI, Azure DevOps, Terraform, Ansible, AWX, CloudFormation, Git
- **Programming & Automation:** Python (Boto3, Requests, Automation tooling), Bash, PowerShell
- **Observability & FinOps:** Prometheus, Grafana, Elasticsearch, Kibana, CloudWatch, Datadog, RCA, Cloud Cost Optimization
- **AI & Data:** RAG Pipelines, AI Agents, LangChain, pgvector, Pinecone, Semantic Retrieval, MongoDB, Amazon RDS, SQL
- **Networking & Security:** TCP/IP, DNS, VPN, VPC Peering, Transit Gateway, Active Directory, Check Point, Cisco, Juniper, SSL/TLS

---

## Selected Technical Projects

1. **AI Agents and RAG Systems Platform:** Autonomous agent workflows and RAG architecture with LangChain, pgvector/Pinecone, and containerized runtime.
2. **Multi-Node Kubernetes and GitOps Infrastructure:** Ubuntu Kubernetes environment on VMware vSphere provisioned with Terraform, Ansible, Rancher, and Argo CD.
3. **AWS Automation and FinOps Sandboxes:** Hands-on EKS/S3 environments with Python/Boto3 automation for cost-pruning and storage lifecycles.
4. **Database Reliability Labs:** MongoDB replica sets, sharding, WiredTiger cache analysis, and Amazon RDS/SQL high availability.
5. **Secure CI/CD Delivery Pipeline:** Reference pipeline with automated testing, SBOM generation, container image scanning, and Argo CD deployment gates.
6. **AI Ticket Handler and Operations Agent:** Serverless AWS Lambda and RAG architecture to classify IT requests and draft verified operational responses.

---

## Local Development

### Prerequisites

- Ruby (>= 3.0) and Bundler (`gem install bundler`)
- Python 3.10+ (for validation scripts)

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/zivhadady/zivops.git
   cd zivops
   ```

2. Bootstrap local dependencies:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. Launch local Jekyll server:
   ```bash
   bundle exec jekyll serve --baseurl ""
   ```
   Open `http://127.0.0.1:4000/` in your browser.

---

## Quality Gates & Testing

To run link and HTML integrity checks before pushing:

```bash
python validate_links.py .
```

---

## License & Contact

Maintained by Ziv Hadady &bull; Tel Aviv-Yafo, Israel.
