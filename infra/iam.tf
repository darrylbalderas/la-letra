resource "aws_iam_role" "lambda_exec_role" {
  name        = "lambda-exec-${local.name}"
  path        = "/"
  description = "Allows Lambda Function to call AWS services on your behalf"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}


resource "aws_iam_role_policy" "cloudwatch_lambda_policy" {
  name   = "${local.name}-lambda-role-policy"
  role   = aws_iam_role.lambda_exec_role.id
  policy = file("${path.module}/files/cloudwatch.json")
}