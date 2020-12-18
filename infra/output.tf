output "base_url" {
  value = aws_api_gateway_deployment.letra.invoke_url
}