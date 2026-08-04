variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "s3_bucket_prefix" {
  description = "Prefix for the S3 static portfolio bucket"
  type        = string
  default     = "alex-devops-portfolio-bucket"
}

variable "lambda_function_name" {
  description = "Name of the Python Lambda function"
  type        = string
  default     = "devops_portfolio_api"
}

variable "iam_role_name" {
  description = "Name of the IAM execution role for Lambda"
  type        = string
  default     = "serverless_lambda_exec_role"
}

variable "calendar_link" {
  description = "The Google Calendar booking link injected into the Python Lambda response"
  type        = string
  sensitive   = true
}
