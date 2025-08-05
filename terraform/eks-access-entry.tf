resource "aws_eks_access_entry" "eks-access-entry" {
  cluster_name      = aws_eks_cluster.eks-cluster.name
  principal_arn     = var.principalArn
  kubernetes_groups = ["fiap"]
  type              = "STANDARD"
}