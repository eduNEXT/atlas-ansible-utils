# STORAGE BACKUPS ROLE

This role is used to store backup files in cloud storage services, supporting both AWS S3 and Azure Blobs.

## AWS S3

The task responsible for storing backups in AWS S3 performs the following steps:

1. **Install AWS CLI:**
   - Uses the `pip` Ansible module to install the `awscli` package.

2. **Copy Files to S3:**
   - Executes the `aws s3 cp` command to copy backup files to the specified S3 bucket.
   - Uses the parameters provided in `STORAGE_BACKUPS_AWS_EXTRA_PARAMS`.
   - Sets AWS credentials using the variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

## Azure Blobs

The task responsible for storing backups in Azure Blobs performs the following steps:

1. **Check and Install AzCopy:**
    - Checks if AzCopy is installed by running `azcopy --version`.
    - If not installed, downloads the latest version from AzCopy v10, extracts the archive, and moves the AzCopy executable to `/usr/bin/`.

2. **Upload Files to Azure Storage:**
    - Executes the `azcopy cp` to copy backup files to the Azure Blobs container.

> **Note:** For the installation and execution of AzCopy, we are utilizing AzCopy version 10. You can find more information about AzCopy v10 [here](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10#download-azcopy).
