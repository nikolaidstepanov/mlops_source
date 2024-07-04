1. Create VM from console
    - Connect via ssh
    - Install python for VM: `sudo apt update && sudo apt install python3 && sudo apt install python3-pip`
    - To add alias use  `vim /.bashrc` and `alias python='python3' alias pip='pip3'` and `source ~/.bashrc`
2. Create VM using Yandex CLI:
    1. [Install CLI](https://yandex.cloud/ru/docs/cli/operations/install-cli#macos_1)
    2. [Create Profile](https://yandex.cloud/ru/docs/cli/operations/profile/profile-create)
    3. Create VM:
        - ```bash yc compute instance create --name otus-mlops --zone ru-central1-a --ssh-key ~/.ssh/id_rsa.pub --cores 32 --public-ip --create-boot-disk size=64GB,image-folder-id=standard-images,image-family=ubuntu-2204-lts --memory 32GB```
        - To check all OS use: `yc compute image list --folder-id standard-images`
    4. Connect to the server via ssh: `ssh yc-user@{network_interfaces.primary_v4_address.one_to_one_nat.address}`
    5. Delete VMs:
        - Get VM id: `yc compute instance list`
        - Delete VM: `yc compute instance delete {id}`
        - Delete VM in async mode: `yc compute instance delete {id} --async`
            - Check async mode by id: `yc operation get {id}`
3. Create S3 bucket from console
    - [Create service account](https://console.yandex.cloud/folders/b1gjei7e2r1040805iqq?section=service-accounts)
    - Generate static key
4. Create S3 bucket using Yandex CLI:
    - Create bucket command: `yc storage bucket create --name mlops-bucket-otus --default-storage-class cold --max-size 10 --public-read --public-list --public-config-read`
    - Check bucket: `aws s3 ls s3://mlops-bucket-otus --endpoint-url=https://storage.yandexcloud.net/`
    - Put file to bucket via console: `aws s3 cp file.txt s3://mlops-bucket-otus --endpoint-url=https://storage.yandexcloud.net/`
    - Delete bucket command: `yc storage bucket delete mlops-bucket-otus`
5. Create Hadoop cluster from Console
    - Set up network:
        - NAT
        - Routing Tables
        - Security Groups
    - Connect to the master node via ssh: `ssh -L 8888:localhost:8888 ubuntu@{master_node.public_ip}`
    - Run Jupyter Hub: `jupyter notebook --port 8888 --ip=* --no-browser`
    - Run notebooks `train_dummy_model.ipynb` and `inference_dummy_model.ipynb`
    - Delete cluster via console
