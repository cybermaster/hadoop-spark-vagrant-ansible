VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bill-trusty64"
  config.vm.box_url = "trusty-server-cloudimg-amd64-vagrant-disk1.box"
#  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  config.ssh.insert_key = false

  # configs for vagrant-cachier
    if Vagrant.has_plugin?("vagrant-cachier")
      config.cache.auto_detect = true
    else
      raise "ERROR Can't find vagrant-cachier! Please install it w/ vagrant plugin install vagrant-cachier"
    end

    # configs for vagrant-hostmanager
    if Vagrant.has_plugin?("HostManager")
      config.hostmanager.enabled = true
      config.hostmanager.manage_host = true
    else
      raise "ERROR can't find vagrant-hostmanager! Please install it w/ vagrant plugin install vagrant-hostmanager"
    end
  
  config.vm.define "hadoopmaster" do |c|
    c.vm.hostname = "hadoopmaster"
    c.vm.network :private_network, ip: "192.168.50.11"
    c.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--memory', 8192]
      vb.customize ['modifyvm', :id, '--cpus', 4]
    end
  end

  config.vm.define "hadoopslave1" do |c|
    c.vm.hostname = "hadoopslave1"
    c.vm.network :private_network, ip: "192.168.50.12"
    c.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--memory', 8192]
      vb.customize ['modifyvm', :id, '--cpus', 4]
    end
  end

  config.vm.define "hadoopslave2" do |c|
    c.vm.hostname = "hadoopslave2"
    c.vm.network :private_network, ip: "192.168.50.13"
    c.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--memory', 8192]
      vb.customize ['modifyvm', :id, '--cpus', 4]
    end
  end
    
  config.vm.define "hadoopslave3" do |c|
    c.vm.hostname = "hadoopslave3"
    c.vm.network :private_network, ip: "192.168.50.14"
    c.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--memory', 8192]
      vb.customize ['modifyvm', :id, '--cpus', 4]
    end
  end
  
  config.vm.define "hadoopclient1" do |c|
    c.vm.hostname = "hadoopclient1"
    c.vm.network :private_network, ip: "192.168.50.15"
    c.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--memory', 1024]
      vb.customize ['modifyvm', :id, '--cpus', 4]
    end
  end
  
end
