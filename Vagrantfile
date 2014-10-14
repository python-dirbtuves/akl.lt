# Intended to work with Vagrant 1.6.*
Vagrant.configure('2') do |config|
  config.vm.define 'akl' do |akl|
    akl.vm.box = 'ubuntu1404'
    # This image uses US mirrors, feel free to change to something more sensible
    akl.vm.box_url = 'https://oss-binaries.phusionpassenger.com/vagrant/boxes/latest/ubuntu-14.04-amd64-vbox.box'
    akl.vm.network "forwarded_port", guest: 8000, host: 8000
    akl.vm.provision :shell, path: './scripts/vagrant-bootstrap.sh'
    akl.vm.synced_folder '.', '/vagrant', disabled: true
    # Default mount is slow on Linux/OSX, use NFS if it's not windows
    # Caveat: will ask for password during vagrant up
    # Taken from https://coderwall.com/p/ffy3uq
    if (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) == nil
      nfs = true
      akl.vm.network 'private_network', ip: '192.168.33.10'
    else
      nfs = false
    end
    akl.vm.synced_folder '.', '/home/vagrant/akl.lt', nfs: nfs
  end
end
