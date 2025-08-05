resource "aws_ecr_repository" "ecr_python" {
  name                 = var.ecr_name_app
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}