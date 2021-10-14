terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "3.61.0"
    }
  }
}



provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_instance" "rca_mediagrab_server" {
  ami           = "ami-02e136e904f3da870"
  instance_type = "t2.micro"
  key_name= "aws_key"
  vpc_security_group_ids = [aws_security_group.main.id]

  tags = {
    Name = "MediaGrab"
  }




  provisioner "remote-exec" {
    inline = [
	"sudo yum update -y",
	"sudo yum install -y git",
        "pip3 install youtube_dl",

        "sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl",
        "sudo chmod a+rx /usr/local/bin/youtube-dl",
	  
	"[ -d bin ] || mkdir bin",
	"cd bin",
	"git clone https://github.com/rcanzlovar/flash-hoarder.git"
	"[ -f mediagrab/install.sh ] && mediagrab/install.sh",
        "cp flash-hoarder/mediagrab/ytsearch.py  .",
        "cp flash-hoarder/mediagrab/settings.json .",

    ]
  }
  connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file("/home/rca/Projects/terraform/aws_key")
      timeout     = "4m"
   }
}

resource "aws_security_group" "main" {
  egress = [
    {
      cidr_blocks      = [ "0.0.0.0/0", ]
      description      = ""
      from_port        = 0
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "-1"
      security_groups  = []
      self             = false
      to_port          = 0
    }
  ]
  ingress                = [
    {
      cidr_blocks      = [ "0.0.0.0/0", ]
      description      = ""
      from_port        = 22
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "tcp"
      security_groups  = []
      self             = false
      to_port          = 22
    }
  ]
}


resource "aws_key_pair" "deployer" {
  key_name   = "aws_key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCR8L5FWO900YSt0Ff2gTyFRiDoSOfeS5PYfBvaFwVGPPEGFr1Bc+3ICkYF92X5mBvjG6JG8+ELXCdpB0Pom77vDUa93Zy3ASwMNrsptHYlDtvoMdlbNE79XwQ+Qyxq1wPHD+1j7Ijn+Cwna6mNgBLmbuAre/xaDTmBy9Hor8AMyWmXUtJmLA7hZIdJVBT9UA7mLBFoNGQg1kPqmo4pyEu5mxR60u8Ox85RDiSAxIqUfmsD9yeKtLR7CewGnnIcbvXnu/ILbQmDdV4MbA4YmCKAc73hB3SuVrDvkEnF9i6h1tMthwzbUK0u7U3e/t+mIJWoHxbF7OzJImOwRCA8elHn rca@wall-e"
}
