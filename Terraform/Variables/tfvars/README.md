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
