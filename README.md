# CAPSTONE PROJECT 491 - CSUF

- Team :

# Inspirations

# Purpose

# How to run the Project in Development

## On Windows:

### Install Chocolately Package Manager

- Install Chocolately Package Manager :

- Run Powershell in Adminstrator Mode. Then run this command :

```
Get-ExecutionPolicy
```

- If it returned `Restricted`, the run this :

```
Set-ExecutionPolicy Bypass -Scope Process
```

- Install Chocolately:

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Install Packages:

- Make sure that you run these commands in Powershell Adminstrator mode:

```
choco install fzf git wget curl httpie nodejs python yarn pnpm docker-cli docker-compose
```

- Download and Install docker software from docker website: https://www.docker.com/

### Run project:

- Docker should be up and running at this point, try running the project.

# Deployment Plan

-

# Lisences

- MIT
