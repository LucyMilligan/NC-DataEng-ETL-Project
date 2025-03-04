# Lambda IAM Role

# Define
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Create
resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Lambda IAM Policy for S3 Write

# Define
data "aws_iam_policy_document" "s3_document" {
  statement {
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      "${aws_s3_bucket.ingestion_bucket.arn}/*",
      "${aws_s3_bucket.transform_bucket.arn}/*",
    ]
  }
}


# Create
resource "aws_iam_policy" "s3_policy" {
  name_prefix = "s3-policy-terrific-totes-lambda-"
  policy      = data.aws_iam_policy_document.s3_document.json
}


# Attach
resource "aws_iam_role_policy_attachment" "lambda_s3_attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.s3_policy.arn
}



