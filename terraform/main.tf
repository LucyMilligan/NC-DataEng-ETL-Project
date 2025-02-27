# Configure the AWS Provider

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.7.0"
    }
  }
  # backend "s3" {
  #   bucket = "terrific-totes-lullymore-backend"
  #   key = "nc-dataeng-etl-project/terraform.tfstate"
  #   region = "eu-west-2"
  # }
}


provider "aws" {
  region = "eu-west-2"

  default_tags {
    tags = { ProjectName = "De-terrific-totes-lullymore-west"
      DeployedFrom = "terraform"
      Repository   = "NC-DATAENG-ETL-PROJECT"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}