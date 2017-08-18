Vagrant.configure('2') do |config|
  config.vm.box = 'debian/stretch64'

  if File.exist?('tmp/ethernet-device.txt')
    ethernet_device = File.read('tmp/ethernet-device.txt').chomp
  else
    ethernet_device = 'eth0'
  end

  config.vm.network :public_network, bridge: ethernet_device

  config.vm.network :public_network, ip: '192.168.42.3'
  config.vm.synced_folder '.', '/vagrant', type: 'nfs'

  config.vm.provider :virtualbox do |v|
    v.cpus = 1
    v.memory = 1024
  end

  config.vm.provision :shell, path: 'update-system.sh'
  config.vm.provision :shell, path: 'provision.sh'
end

# vim: ft=ruby
