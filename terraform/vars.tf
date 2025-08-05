variable "regionDefault" {
  default = "us-east-1"
}

variable "projectName" {
  default = "fiap-eks"
}

variable "ecr_name_app" {
  default = "app-python"
}

variable "accessConfig" {
  default = "API_AND_CONFIG_MAP"
}

variable "nodeGroup" {
  default = "fiap"
}

variable "instanceType" {
  default = "t3.medium"
}

variable "policyArn" {
  default = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
}