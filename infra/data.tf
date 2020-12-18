
data "archive_file" "source" {
  type        = "zip"
  source_dir  = "${path.module}/code"
  output_path = "${path.module}/lambda.zip"
  excludes    = []
}