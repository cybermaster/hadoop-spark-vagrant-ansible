# Hadoop-Spark-vagrant-ansible

hadoop-vagrant-ansible implements the script that deploy Hadoop with ansible on Vagrant environment and Amazon ec2 using CloudFormation.
The playbook script is base on [ansible-examples/hadoop](https://github.com/ansible/ansible-examples/tree/master/hadoop)


## Preface
The playbooks in this example are designed to deploy a Hadoop cluster on a
Ubuntu 14.04 LTS environment using Ansible and Vagrant. The playbooks can:

- Deploy a fully functional Hadoop cluster with HA and automatic failover.

- Deploy a fully functional Hadoop cluster with no HA.

- Deploy additional nodes to scale the cluster

These playbooks require [Ansible](https://github.com/ansible/ansible), [Ubuntu 14.04 LTS](https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box) target machines, and install
the open-source [Cloudera Hadoop Distribution (CDH) version 5](http://archive.cloudera.com/cdh5/ubuntu/trusty/amd64/cdh).

As for [Ansible version](http://docs.ansible.com/intro_installation.html), because it runs easily from source and does not require any installation of software on remote machines, many users will actually track the development version.  Ansible’s release cycles are usually about two months long.  Due to this short release cycle, minor bugs will generally be fixed in the next release versus maintaining backports on the stable branch.  Major bugs will still have maintenance releases when needed, though these are infrequent.

## Hadoop Components

Hadoop is framework that allows processing of large datasets across large
clusters. The two main components that make up a Hadoop cluster are the HDFS
Filesystem and the MapReduce framework. Briefly, the HDFS filesystem is responsible 
for storing data across the cluster nodes on its local disks. The MapReduce
jobs are the tasks that would run on these nodes to get a meaningful result
using the data stored on the HDFS filesystem.


## Installing the Ansible Control Machine

Usually the Ansible control machine is your laptop.  This machine is where you run your Ansible script.  The root permissions are not required to use it and there is no software to actually install for Ansible itself. No daemons or database setup are required.  Ansible is communicating with remote machines over SSH.

To install from source:

    $ git clone git://github.com/ansible/ansible.git
    $ cd ./ansible
    $ source ./hacking/env-setup

OR install from home brew (Mac OS X):

    $ brew install ansible

If you don’t have pip installed in your version of Python, install pip:

    $ sudo easy_install pip

Ansible also uses the following Python modules that need to be installed:

    $ sudo pip install paramiko PyYAML jinja2 httplib2 markupsafe


### Installing the Git Large File Sotrage
Install from home brew (Mac OS X):

    $ brew install git-lfs

Fetch the large files:

    $ git lfs fetch

## Running the Ansible script on Vagrant

#### Vagrant and VirtrualBox setup:

You will need [Vagrant](http://www.vagrantup.com/downloads) installed on your box before continue.  In addition, you will need [VirtualBox](https://www.virtualbox.org/wiki/Downloads) to host the virtual machines, please install that as well.

After Vagrant setup you need to install vagrant-cachier and vagrant-hostmanager

    $ vagrant plugin install vagrant-cachier
    $ vagrant plugin install vagrant-hostmanager
#### Running the Ansible script:

Clone `hadoop-spark-vagrant-ansible`:

    git clone git@github.com:cybermaster/hadoop-spark-vagrant-ansible.git
    cd hadoop-spark-vagrant-ansible
 
##### For faster OS install:
Download the [Ubuntu Vagrant OS file](https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box) and edit the `hadoop-spark-vagrant-ansible/Vagrantfile` with the local copy of the file i.e. `config.vm.box_url = "/Users/bill/Downloads/trusty-server-cloudimg-amd64-vagrant-disk1.box"`
 
Run the script in `hadoop-spark-vagrant-ansible/` directory:

    vagrant up
Pay attention to the console. It will ask for your shell password to add the hostname and IP address to your /etc/hosts file.

After the last command, vagrant will bring up a single Hadoop master server and few Hadoop data nodes.

Now you can run the ansible playbook script with ansible command.

##### Copy Spark binary to here:
In order to speedup the install, please copy [spark-1.6.0-bin-hadoop2.6.tgz](http://www.us.apache.org/dist/spark/spark-1.6.0/spark-1.6.0-bin-hadoop2.6.tgz ) to `roles/spark_common/files`

    $ curl -o roles/spark_common/files/spark-1.6.0-bin-hadoop2.6.tgz http://www.us.apache.org/dist/spark/spark-1.6.0/spark-1.6.0-bin-hadoop2.6.tgz

Run ansible script:

    ansible-playbook -i inventory/vagrant-4hosts.inv site.yml

The `-i inventory/vagrant-4hosts.inv` tells ansible where you defined all the hosts.  The `-u vagrant` tells ansible the username to run the script on the target hosts is vagrant.

However, if you still see error message or the script doesn't complete fully.  You can try to run ansible in verbose mode.

Run ansible in verbose mode:

    ansible-playbook -i inventory/vagrant-4hosts.inv site.yml -vvvv

#### Running few simple Hadoop jobs:

Run a very simple job to count occurrence of a word:

    ansible-playbook -i inventory/vagrant-4hosts.inv playbooks/job.yml

This job will test the basic function of Hadoop File System and MapReduce framework.  If it run to completion, then the hadoop cluster is working.


Run a simple Quasi Monte Carlo Pi estimation:

    ansible-playbook -i inventory/vagrant-4hosts.inv playbooks/pi.yml

This job will run a simple Monte Carlo Pi estimation using 10 maps.  The pi should be around 3.2.


Run a basic hadoop job with Python:

    ansible-playbook -i inventory/vagrant-4hosts.inv playbooks/python-wc/wc.yml

This will run the Python wordcount program with Hadoop Streaming

## Hadoop Web Interface
Hadoop comes with several web interfaces which are by default available at these locations:

[http://hadoopmaster:50070/](http://hadoopmaster:50070/) – web UI of the NameNode daemon

[http://hadoopmaster:50030/](http://hadoopmaster:50030/) – web UI of the JobTracker daemon

[http://hadoopslave1:50060/](http://hadoopslave1:50060/) – web UI of the TaskTracker daemon

#### NameNode Web Interface (HDFS layer)
The namenode web UI shows you a cluster summary including information about total/remaining capacity, live and dead nodes. Additionally, it allows you to browse the HDFS namespace and view the contents of its files in the web browser. It also gives access to the local machine’s Hadoop log files.

By default, it’s available at [http://hadoopmaster:50070/](http://hadoopmaster:50070/).

#### JobTracker Web Interface (MapReduce layer)
The JobTracker web UI provides information about general job statistics of the Hadoop cluster, running/completed/failed jobs and a job history log file. It also gives access to the ‘‘local machine’s’’ Hadoop log files (the machine on which the web UI is running on).

By default, it’s available at [http://hadoopmaster:50030/](http://hadoopmaster:50030/).

#### TaskTracker Web Interface (MapReduce layer)
The task tracker web UI shows you running and non-running tasks. It also gives access to the ‘‘local machine’s’’ Hadoop log files.

By default, it’s available at [http://hadoopslave1:50060/](http://hadoopslave1:50060/).

## Spark Web Interface
[http://hadoopmaster:8080](http://hadoopmaster:8080) - web UI of the Spark

## Tachyon Web Interface
[http://hadoopmaster:19999](http://hadoopmaster:19999) - web UI of the Tachyon

## Setting up Hadoop on Amazon ec2 with CloudFormation

AWS CloudFormation enables you to create and provision AWS infrastructure deployments predictably and repeatedly. It helps you leverage AWS products such as Amazon EC2, Amazon Elastic Block Store, Amazon SNS, Elastic Load Balancing, and Auto Scaling to build highly reliable, highly scalable, cost-effective applications without worrying about creating and configuring the underlying AWS infrastructure. AWS CloudFormation enables you to use a template file to create and delete a collection of resources together as a single unit (a stack).

#### Creating the Stack:

There are few things that you need for CloudFormation to work.
 * Install [boto](http://boto.readthedocs.org/en/latest/getting_started.html) 
 * Install [awscli](http://aws.amazon.com/cli/)
 * Setup Amazon aws account and download the ssh key

1. Create a virutal environment and install the python dependencies.
   Assuming you have virtualenv and virtualenvwrapper setup, you can run:

        mkvirtualenv hadoop_ec2
        pip install -r playbooks/create_hadoop_stack/requirements.txt

2. Setup the boto AWS Python library authentication. Create a file ~/.boto
   and fill it in with your AWS credentials using the following format:

        [Credentials]
        aws_access_key_id = <AWS_ACCESS_KEY_ID>
        aws_secret_access_key = <AWS_SECRET_ACCESS_KEY>

3. Check the inventory/create-ec2 file; make sure it points to the correct python env.

        [localhost]
        127.0.0.1 ansible_python_interpreter=/Users/john.doe/.virtualenvs/hadoop_ec2_deploy/bin/python 

4. To spawn a new Hadoop deployment using CloudFormation, invoke the following:

        ansible-playbook -i inventory/create-ec2 playbooks/create_hadoop_stack/create_hadoop_stack.yml -vvv

    This can take a while to run, you can check for the status by visiting the AWS Console page.

5. Once the stack is up and running, you can view the inventory by using the dynamic inventory script:

        inventory_plugins/hadoop_ec2.py --list

6. To use the newly created stack, you can specify the dynamic inventory script
   as the -i <inventory> argument for the ansible-playbook when running hadoop_ansible, e.g:

       ansible-playbook -i ./inventory_plugins/hadoop_ec2.py site.yml -vvv
