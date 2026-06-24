output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "instance_ip" {
  value       = aws_instance.test.public_ip
  description = "EC2 instance public IP — use with: ssh -i ~/.ssh/deployer-key ubuntu@<public-ip>"
}

output "my_ip_cidr" {
  value       = local.my_ip_cidr
  description = "Public IP (CIDR) used for the SSH ingress rule"
}