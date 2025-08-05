resource "aws_eks_access_entry" "access_entry" {
  cluster_name      = aws_eks_cluster.cluster.name
  principal_arn     = data.aws_iam_user.principal_user.arn
  kubernetes_groups = ["group-11soat", "group-profs"]
  type              = "STANDARD"
}
