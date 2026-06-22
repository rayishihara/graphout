variable "region" {
  type        = string
  description = "AWS Region to deploy resources"
  default     = "ap-southeast-2" # Sydney
}

variable "availability_zone" {
  description = "AZ for the public subnet"
  type        = string
  default     = "ap-southeast-2a"
}

variable "project" {
  type        = string
  description = "Prefix for resource names and AWS tags"
  default     = "graphout"

  validation {
    condition     = var.project == lower(var.project)
    error_message = "Invalid project name: must all be lowercase"
  }
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/28"
}

variable "public_subnet_cidr" {
  type        = string
  description = "CIDR block for the public subnet"
  default     = "10.0.0.0/29"
}