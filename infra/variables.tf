variable region {
  description = "AWS region"
  type        = string
}

variable lambda_version {
  description = "AWS Lambda function version"
  type        = string
}

variable env {
  description = "Environment e.g. Staging, Development, or Production"
  type        = string
}

variable "function_name" {
  type        = string
  description = "AWS Lambda function name"
}

variable "handler" {
  type        = string
  default     = "lambda.handler"
  description = "AWS Lambda Handler"
}

variable "runtime" {
  type        = string
  description = "AWS Lambda Runtime"
}