# terraform-academy

## Criação feita utilizando o AWS Academy da FIAP

### Considerações do AWS Academy

1 - A sessão dura 4h, ao fim dessa sessão os recursos não serão excluídos, crie uma nova sessão e aplique o `terraform destroy` para evitar gastos;

2 - Assim como a sessão, as credenciais: AccessKey, SecretKey e SessionToken, também duram 4h, depois desse tempo, precisa entrar no Academy novamente e pegar os novos valores e atualizar o arquivo de credenciais da aws local;

3 - Temos disponíveis 50 dólares, administre com sabedoria esse valor, sempre que finalizar, destrua a infra criada para para com os gastos desnecessários;

## eks-cluster

Neste exemplo, utilizamos o tipo de conexão via LoadBalancer em nosso Service, e ele cria um Network Load Balance que fornece um único endereço IP para encaminhar todo tráfego para nosso serviço (NGINX)

## Comandos utilizados

### Terraform

- `terraform init` = comando responsável por inicializar o terraform em nosso diretório local;
- `terraform fmt` = comando responsável por formatar nossos arquivos .tf corrigindo a identação;
- `terraform plan` = comando responsável por gerar um inventário do que será criado/alterado/deletado na infra;
- `terraform apply` = comando responsável por executar a ação criação/alteração/exclusão de recursos na cloud;
- `terraform destroy` = comando responsável por deletar todo recurso criado que foi definido nos arquivos .tf

### k8s

- `aws eks update-kubeconfig --name <nome-cluster> --region <region> --profile <profile-credential>` = responsável por atualizar o kubeconfig no Bastion Node;
- `kubectl get nodes` = responsável por listar todos nodes criados no eks;
- `kubectl apply -f k8s/eks-deployment.yaml` = responsável por aplicar o arquivo de deployment no cluster criado;
- kubectl apply -f k8s/eks-deployment.yaml` = responsável por aplicar a configuração e criar o service no cluster;
- `kubectl get svc` = responável por listar os services criados;