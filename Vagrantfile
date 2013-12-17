# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "wheezy64"
  config.vm.box_url = "https://dl.dropboxusercontent.com/u/197673519/debian-7.2.0.box"

  config.vm.network :forwarded_port, guest: 22023, host: 22023
  config.vm.network :forwarded_port, guest: 443, host: 443

  config.vm.provision "shell", inline: "usermod -p `openssl passwd lel`  root"
  config.vm.provision "shell", inline: "cp /vagrant/config/sources.list /etc/apt/sources.list"
  config.vm.provision "shell", inline: "apt-get update"
end
