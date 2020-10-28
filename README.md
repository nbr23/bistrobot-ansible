# Ansible Collection - nbr23.bistrobot

Ansible collection for using [bistrobot](https://github.com/nbr23/bistrobot) to
control modified Pet feeding robots embedding Raspberry Pi Zero.

# Installation

`ansible-galaxy collection install git+https://github.com/nbr23/bistrobot-ansible.git`

# Roles

## bistrobot

Use the bistrobot role to set the bistrobot python package up on the target:

```
---
- hosts: raspizero
  gather_facts: false

  collections:
    - nbr23.bistrobot

  roles:
    - bistrobot
```
