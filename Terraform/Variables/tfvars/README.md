# 1.  Terraform tfvars file - terraform.tfvars

- create terraform.tfvars, insert below data. to run simple simple-tfvars.tf
```
instance_type="t2.micro"
```
- Then execute, below commands respectively 

```
terraform init
terraform plan
terraform apply
```

- once done destroy all the aws resources 

```
terraform destroy
```

# 2. Terraform multiple tfvars file

- create your stage.tfvars for staging,  insert below data.
```
instance_type="t2.micro"
environment_name ="stage" 
```

- Then execute below command 
```
terraform init
terraform plan -var-file="stage.tfvars"
terraform apply -var-file="stage.tfvars"
terraform destroy -var-file="stage.tfvars"
```

# 3. Terraform setting variable using command line var

- Lets assume you want to run simple-tfvars.tf, then we can use below commands 

```
terraform init
terraform plan -var="instance_type=t2.micro"
terraform apply -var="instance_type=t2.micro"
terraform destroy -var="instance_type=t2.micro"
```
