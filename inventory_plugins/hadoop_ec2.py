#!/usr/bin/env python
"""
Hadoop EC2 Ansible Dynamic Invetory Script.

Based on the Ansible ec2.py dynamic inventory script.
"""
from json import loads


from ec2 import Ec2Inventory


# The Ansible groups we'd like to map EC2 hosts into
HADOOP_EC2_HOST_GROUPS = [
    "hadoop_masters",
    "hadoop_slaves",
    "hadoop_clients",
]


# Mapping from EC2 Host Groups to Ansible groups in the site.yml file. Only needs
# entries where the two differ.
HADOOP_HOST_GROUP_MAPPINGS = {
    "hadoop_masters": "hadoop_master_primary",
}


class HadoopEc2Inventory(Ec2Inventory):

    def __init__(self):
        ''' Main execution path '''

        # Inventory grouped by instance IDs, tags, security groups, regions,
        # and availability zones
        self.inventory = self._empty_inventory()

        # Index of hostname (address) to instance ID
        self.index = {}

        # Read settings and parse CLI arguments
        self.read_settings()
        self.parse_cli_args()

        # Cache
        if self.args.refresh_cache:
            self.do_api_calls_update_cache()
        elif not self.is_cache_valid():
            self.do_api_calls_update_cache()
        # Data to print
        if self.args.host:
            data_to_print = self.get_host_info()

        elif self.args.list:
            # Display list of instances for inventory
            if self.inventory == self._empty_inventory():
                data_to_print = self.get_inventory_from_cache()
            else:
                data_to_print = self.json_format_dict(self.postprocess_inventory(self.inventory),
                                                      True)

        print data_to_print

    def get_inventory_from_cache(self):
        json_inventory = super(HadoopEc2Inventory, self).get_inventory_from_cache()

        return self.json_format_dict(self.postprocess_inventory(loads(json_inventory)), True)

    def postprocess_inventory(self, inventory):
        """
        Perform any post-processing on inventory dictionary to bring it into
        format we use with the Hadoop deployment scheme.

        """
        ec2_vars = inventory['_meta']['hostvars']
        out = {}
        for host_group_name in HADOOP_EC2_HOST_GROUPS:
            host_group_key = u"tag_HostGroup_{}".format(host_group_name)
            try:
                host_group_hosts = inventory[host_group_key]
            except KeyError:
                # host group was not found in inventory
                continue
            else:
                key = HADOOP_HOST_GROUP_MAPPINGS.get(host_group_name, host_group_name)
                out[key] = {
                    'hosts': host_group_hosts,
                }

                out[key]['vars'] = self.create_hadoop_group_vars(key, host_group_hosts, ec2_vars)

        out['_meta'] = {'hostvars': self.create_hadoop_host_vars(out, ec2_vars)}
        out['hadoop_all'] = self.create_hadoop_all_group_vars(out, ec2_vars)
        out['hadoop_masters'] = self.create_hadoop_masters_group_vars(out, ec2_vars)

        return out

    def create_hadoop_host_vars(self, inventory, ec2_vars):
        """
        Construct the host vars for the Hadoop ec2 inventory.
        """
        host_vars = {}

        return host_vars

    def create_hadoop_group_vars(self, group_name, hosts, ec2_vars):
        """
        Construct the group vars for a specific host group.

        """
        group_vars = {
            'ansible_ssh_user': 'ubuntu'
        }

        return group_vars


    def create_hadoop_all_group_vars(self, inventory, ec2_vars):

        return {
            'children': map(lambda g: HADOOP_HOST_GROUP_MAPPINGS.get(g, g), HADOOP_EC2_HOST_GROUPS),
            'vars': {
                "ansible_ssh_user": "ubuntu"
            }
        }

    def create_hadoop_masters_group_vars(self, inventory, ec2_vars):

        return {
            'children': ["hadoop_master_primary"],
            'vars': {
                "ansible_ssh_user": "ubuntu"
            }
        }

if __name__ == "__main__":
    HadoopEc2Inventory()
