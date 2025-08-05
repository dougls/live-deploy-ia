terraform {
  backend "s3" {
    bucket = "fiap-live-ia"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}