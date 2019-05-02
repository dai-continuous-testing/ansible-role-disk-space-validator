#!/usr/bin/python

import os
import re

from ansible.module_utils.basic import AnsibleModule

def filter_not_none(item):
    return item is not None

def get_partition_by_letter(drive_letter):
    
    def f(disk):
        for partition in disk["partitions"]:
            for access_path in partition["drive_letter"]:
                if partition["drive_letter"].lower() == drive_letter.lower():
                    return partition 
        return None

    return f

def get_free_space_in_partition(partition):
    return partition["volumes"][0]["size_remaining"]

def get_disk_space_in_partition(partition):
    return partition["volumes"][0]["size"]

def main():
    
    module_args = dict(
        disks=dict(type='list', required=True),
        drive_letter=dict(type='str', required=True)
    )
    
    module = AnsibleModule(
        argument_spec=module_args
    )

    result = {}

    disks = module.params["disks"]
    drive_letter = module.params["drive_letter"]

    matched_partitions = list(map(get_partition_by_letter(drive_letter), disks))
    filterred_matched_partitions = list(filter(filter_not_none, matched_partitions))

    if len(filterred_matched_partitions) == 0:
        result["disk_found"] = False
        module.fail_json("disk %s:\\ not found" % drive_letter, **result)
    
    elif len(filterred_matched_partitions) > 1:
        result["disk_found"] = False
        module.fail_json("more than one disk is found", **result)
    
    else:
        result["disk_found"] = True
        
        free_disk_space = get_free_space_in_partition(filterred_matched_partitions[0])
        total_disk_space = get_disk_space_in_partition(filterred_matched_partitions[0])

        result["free_disk_space"] = {
            "bytes": free_disk_space,
            "mib": round(free_disk_space / (1024 * 1024)),
            "gib": round(free_disk_space / (1024 * 1024 * 1024))
        }

        result["total_disk_space"] = {
            "bytes": total_disk_space,
            "mib": round(total_disk_space / (1024 * 1024)),
            "gib": round(total_disk_space / (1024 * 1024 * 1024))
        }

    module.exit_json(**result)

if __name__ == '__main__':
    main()
