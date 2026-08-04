output "s3_bucket_name" {
  description = "The name of the S3 static portfolio bucket"
  value       = aws_s3_bucket.portfolio_bucket.id
}

output "s3_website_endpoint" {
  description = "The website endpoint of the S3 bucket"
  value       = aws_s3_bucket_website_configuration.portfolio_website.website_endpoint
}

output "lambda_function_name" {
  description = "The name of the deployed Python Lambda function"
  value       = aws_lambda_function.api_backend.function_name
}

output "lambda_url" {
  description = "The public URL endpoint for the Python Lambda function"
  value       = aws_lambda_function_url.api_url.function_url
}
