# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "wheezy64"
  config.vm.box_url = "https://dl.dropboxusercontent.com/u/197673519/debian-7.2.0.box"

  config.vm.network :forwarded_port, guest: 22, host: 2202
  config.vm.network :forwarded_port, guest: 2222, host: 2203

  config.vm.provision "shell", inline: "usermod -p `openssl passwd lel`  root"
end
