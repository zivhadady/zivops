variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "calendar_link" {
  description = "The Google Calendar booking link injected into the Python Lambda response"
  type        = string
  sensitive   = true
}
