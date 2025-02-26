# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket


resource "aws_s3_bucket" "ingestion_bucket" {
  bucket = "lullymore-west-ingested"
  tags = {
    Name = "BucketForDataIngestion"
  }
}


resource "aws_s3_bucket" "transform_bucket" {

  bucket = "lullymore-west-transformed"
  tags = {
    Name = "BucketForDataTransformation"
  }
}
