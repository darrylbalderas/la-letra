locals {
  name      = "${var.function_name}-${var.region}-${var.env}"
  accountId = data.aws_caller_identity.current.account_id
  region    = var.region
}


resource "aws_lambda_function" "lambda_function" {
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = var.handler
  runtime       = var.runtime
  function_name = local.name
  s3_bucket     = local.name
  s3_key        = "${var.lambda_version}/lambda.zip"
  // filename      = "lambda.zip"
  // source_code_hash = data.archive_file.source.output_base64sha256
  depends_on = [aws_cloudwatch_log_group.log_group, aws_s3_bucket_object.version]
}

resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/aws/lambda/${local.name}"
  retention_in_days = 7
}

resource "aws_s3_bucket" "lambda_versions" {
  bucket        = local.name
  acl           = "private"
  force_destroy = true
}

# Upload an object
resource "aws_s3_bucket_object" "version" {
  bucket     = aws_s3_bucket.lambda_versions.id
  key        = "${var.lambda_version}/lambda.zip"
  acl        = "private"
  source     = "lambda.zip"
  etag       = data.archive_file.source.output_md5
  depends_on = [data.archive_file.source]
}


resource "aws_lambda_permission" "allow" {
  statement_id_prefix = "AllowLambdaS3BucketNotification-"
  action              = "lambda:InvokeFunction"
  function_name       = local.name
  principal           = "s3.amazonaws.com"
  source_arn          = aws_s3_bucket.lambda_versions.arn
  depends_on          = [aws_lambda_function.lambda_function, aws_s3_bucket.lambda_versions]
}
