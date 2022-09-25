# AWS-Terraform


# Terraform advanced commands 

1. ``` terraform apply -target=aws_instance.app ```

to create only specific resource, in terraform code where we have to many resources to be created.

2. ``` terraform destroy -target=aws_instance.app ```

to delete specific resource, we can use above command 

3. In projects terraform code will be applied using any cicd pipelines, ideally 3 stages will be there terraform init, terraform plan and terraform apply.
But not many times code will be changed in such cases ideal soultion will be executing plan command and check if any changes are there if no changes then stop the pipeline.

below commands might help in that 
```
terraform plan -out=tfplan
terraform show -json tfplan | jq .resource_changes[].change.actions
```
