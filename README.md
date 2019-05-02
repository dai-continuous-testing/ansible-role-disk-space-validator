Experitest - Disk space validator ansible role
=========

[![Build Status](https://travis-ci.org/ExperitestOfficial/ansible-role-disk-space-validator.svg?branch=master)](https://travis-ci.org/ExperitestOfficial/ansible-role-disk-space-validator)

This role will install \ uninstall disk-space-validator (or alternatives) in all platforms. \
The role will fail if the free space is less the required mb.

Requirements
------------

Supports windows, linux, and osx

Role Variables
--------------

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| required_space_mb | the required free space in mb | number |  | yes |
| drive_letter | the letter of the disk to test | string |  | for windows only |
