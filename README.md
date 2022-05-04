# Couchbase Ansible Playbooks

## Explanation

It is assumed that you already have Ansible installed. For more information on Ansible, review their [installation instructions](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).

If you are interested in installing Couchbase Server quickly without any manual processes, then you can use the Ansible playbooks in this repo to help you attain a fast, stable, reliable and consistent Couchbase installation. These playbooks implement the best practices as described by Couchbase. As of this writing, this implementation works on multiple Linux distributions and has been formally tested on RHEL 7.x+ as well as Amazon Linux AMIs.

## Setup
It is recommended that you use a stand-alone host that has Ansible installed on it and use the host to promote changes to your newly provisioned Couchbase nodes.

When you are ready to use this set of playbooks, there is an ```init.yml``` file in the ```bin``` directory that will prompt you to configure your Ansible environment prior to installing Couchbase.

## Step 1:
Execute ```ansible-playbook bin/init.yml```

## Ansible Prompts:
  Prompt                | Expected Input
  ----------------------------|-----------------------------
  Would you like to begin the initialization process?         | yes / no
  Enter the full path to your ansible.cfg file | /path/where/we/will/create/your/file
  Enter the full path to your inventory file?  | /path/where/we/will/create/your/file
  Enter your SSH user name for your Couchbase Cluster  | your SSH user Name
  Enter the full path and name of your SSH key | /path/to/your/sshkey.pem

After completing the prompts, we will create two files ```ansible.cfg``` and ```inventory``` in the specified directories. If these files already exist in the specified directory, we will create a backup of the original file in the format ```ansible.cfg-<epoch-timestamp>``` etc.



## Step2:
Enter the following commands for each file paths that we created for you from the earlier Prompts to ensure your files have been created and are in the proper directory.

```ls -l /path/where/we/created/your/ansible.cfg```<br>
```ls -l /path/where/we/will/created/your/inventory file ```

Confirm your SSH key exists at the path you entered<br>
```ls -l /path/to/your/sshkey.pem```<br>
* Note: you may have to modify the permissions on your SSH file to connect to your target server(e.g. chmod 400 sshkey.pem)


Open the ```ansible.cfg``` file located in the directory we created for you at the path ```/path/where/we/created/your/ansible.cfg``` and confirm all information is correct. If you need to change any values, you can modify the file directly or re-run the init.yml again to correct any mistakes.

Open the ```inventory``` file located ```/path/where/we/created/your/inventory_file```
by entering the following command:

```vi /path/where/we/created/your/inventory_file``` (note: the file name is ```inventory```)

and ensure you have a default set of hosts created for you. It will look something like this:

```
#this is the default inventory file

#master-host will be the first node you add to the Couchbase cluster. This node must implement the data service(e.g. kv). Other services can also be co-located, but kv must exist for this node
[master-host]
host1.acme.com services=kv,fts,eventing

#other-hosts are all of the other Couchbase nodes in your cluster(do not include the master-host in this list).You can have services as needed. Each respective hosts has a services host variable in-line with the host name.
#you can add/remove services as needed from the services host variables.
[other-hosts]
host2.acme.com services=kv,fts,eventing
host3.acme.com services=kv,fts,eventing
host4.acme.com    services=n1ql,index
host5.acme.com    services=n1ql,index
host6.acme.com    services=cbas

#query-host is the node to run all n1ql query commands on for creating indexes
[query-host]
host4.acme.com

#search-host is the node to run all fts index commands on for creating indexes
[search-host]
host1.acme.com

#eventing-host is the node to run all fts index commands on for creating indexes
[eventing-host]
host1.acme.com

#cbas-host is the node to run all cbas commands on for creating datasets
[cbas-host]
host6.acme.com
```

## Step 3:
Open your inventory file and enter your hostnames/IP Address and their respective Couchbase Service(s). The inventory file uses YAML as do the playbooks, so you will have to pay attention to your spacing as required by YAML.

## Valid Services:

Host Services                | Description
----------------------------|-----------------------------
kv        | data service
n1ql | query service
index  | index service(default is plasma)
fts  | search service
eventing | eventing service  
cbas  | analytics service  
backup  | backup service(applies to CB Server 7.x+)  


## Step 4:
Run the following command:<br>
```vi playbooks/group_vars/all.yml```

The ```all.yml``` file contains all global variables that Ansible will use when running the playbooks. This file allows you to configure your Couchbase cluster, buckets, memory quotas etc. and many other settings within the product. It also specifies settings for many other linux-kernel tunings that will allow your Couchbase cluster to perform better in many situations.

## Step 5:
Edit the following files to make sure the bucket names and file paths are complete and correct.

-	cbas.json - Contains the Analytics commands for creating the datasets
-	fts.json - Contains information about the FTS indexes to create and the json files containing each index
-	functions.json - Contains information about the Eventing functions to create, and where to find the export files containing each function
-	indexes.json - Contains the list of GSI indexes to be created
-	engagement\_stats\_qa2.json - Eventing function export file
-	sesssion\_update\_qa2.json - Eventing function export file

## Step 6:
To use the default ```all.yml``` configurations, you may leave the file in tact and execute the playbooks without making any additional changes. If you want/need specific configuration, you may change those at anytime.

To install Couchbase to your target nodes, execute the following:<br>
```ansible-playbook _RunAllPlaybooks.yml```

NOTE: This will install Couchbase Server on the specified target nodes and it is recommended that you test this a few times in a lower environment to ensure you have your cluster set up as expected.

## Uninstall Couchbase
To uninstall Couchbase from the specified target nodes, execute the following:
```ansible-playbook playbooks/uninstall/___Uninstall-Couchbase-Server.yml```

NOTE: This will uninstall Couchbase Server from any target node(s) you specify in your ```inventory``` file, so you should pay close attention if you decide to run this playbook! This is handy if you are testing these playbooks and want to modify your configuration without having to uninstall manually.

## Global Variable Definitions:
Host Services                | Description
----------------------------|-----------------------------
operating\_system.update\_packages        | yum updates
operating\_system.ping\_nodes | runs ping command
ntp_server.install  | installs NTP Server
ntp_server.time_zone  |  sets timezone locale
ntp_server.ntp_host  |  NTP host
couchbase_version.build  | Couchbase version
couchbase_version.url  |  URL to RPM
couchbase_version.dest_dir  | directory to store downloaded RPM file  
couchbase_cluster.name | name of your cluster  
couchbase\_cluster.index\_storage  | index storage(default: plasma)  
couchbase\_cluster.memory\_quota.data  | data service memory quota
couchbase\_cluster.memory\_quota.index | index service memory quotas  
couchbase\_cluster.memory\_quota.search  | search service memory quotas  
couchbase\_cluster.memory\_quota.analytics  | analytics service memory quotas  
couchbase\_cluster.memory\_quota.eventing  | eventing memory quotas  
couchbase\_cluster.security.admin\_user  | admin user name for Cluster  
couchbase\_cluster.security.admin\_pwd  |  admin password for Cluster
couchbase_cluster.security.port  | Couchbase port(default: 8091)  
couchbase\_cluster.security.http\_protocol  | http string  
couchbase_cluster.paths.data  | directory path for data Service  
couchbase_cluster.paths.index  | directory path for index Service  
couchbase_cluster.paths.analytics  | directory path for analytics Service  
couchbase_cluster.paths.eventing  | directory path for eventing Service  
couchbase\_cluster.auto\_failover.enabled  | enable/disable auto_failover  
couchbase\_cluster.auto\_failover.timeout  | autofailover timeout(default: 120 seconds)
couchbase_cluster.buckets.name  | name of bucket to created
couchbase_cluster.buckets.type  |  type of Couchbase buckets
couchbase_cluster.buckets.mem_quota  | bucket memory quota
couchbase_cluster.buckets.replicas  |  number of bucket replicas
couchbase_cluster.buckets.compression_mode  | compression mode setting(default: passive)
couchbase_cluster.buckets.flush_enabled  |  enable/disable flushing
couchbase\_cluster.buckets.num\_replicas  |  number of bucket replicas
couchbase\_cluster.buckets.eviction\_policy  | eviction eviction_policy
couchbase\_cluster.buckets.conflict\_resolution  | conflict resolution strategy(default: lww[last-write-wins])  
couchbase\_cluster.kernel\_tuning.is\_enabled  | enable/disable linux kernel tunings
couchbase\_cluster.kernel\_tuning.disable\_THP  |  enable/disable disable_THP
couchbase\_cluster.kernel\_tuning.vm\_swappiness  | set vm.vm_swappiness  
couchbase\_cluster.kernel\_tuning.ulimits  | set ulimits
couchbase\_cluster.kernel\_tuning.network\_and\_memory  | set network/memory tunings per best practices
