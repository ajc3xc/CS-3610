# Container
This repository offers an easy-to-use docker container for programming assignments.
It can be used in conjunction with `assigner`, https://git-classes.mst.edu, and `grade.sh`.

## Install Docker/Podman/Signularity
If you are on Mac, or Windows, see the instructions here:
https://docs.docker.com/get-docker/

If you are on Linux/Unix, you don't really need Docker.
However if you want to use it,
you should probably use whatever docker is in the system repos.

Note: depending on your shell, you may need to exclued `sudo` from the below commands.

## Testing docker works
After installing docker, run:

`sudo docker run -it fedora`

Confirm that it worked, and you're in a Fedora container.

Then, to leave the container, type:

`exit`

## Running the remote pre-built image
If you are on an x86-64 architecture,
you can just pull a pre-built image.
Run the following command from the root directory of your Git repository,
where `<shell>` is your choice of shell (nu/fish/zsh/bash/etc.):

`sudo docker run --interactive --tty --rm --mount type=bind,source="$(pwd)"/,target=/your_code git-docker-classes.mst.edu/containers/container <shell>`

Your repository files are mounted inside the following directory:

`cd your_code`

## Building and running the image locally (optional)
If you are not on an x86-64 architecture,
or are curious, or are security-conscious,
you may want to build the image yourself.
From within the `container` repository directory 
(usually a Git submodule of your assignment), execute:

`sudo docker build --tag container .`

Then, you can run the image you built locally.
From the root directory of your assignment Git repository,
or any directory you would like to mount in a container, execute,
where `<shell>` is your choice of shell (nu/fish/zsh/bash/etc.):

`sudo docker run --interactive --tty --rm --mount type=bind,source="$(pwd)"/,target=/your_code container <shell>`

Your files will be mounted inside the container,
in the following directory:

`cd your_code/`

## Campus Linux Machines (rootless docker)
If you use `ssh` (via putty or otherwise) to access the campus Linux machines,
then you will need to run a rootless container option.
First type `cd` to head to your home directory, then type:

`singularity shell docker://git-docker-classes.mst.edu/containers/container`

or:

`apptainer shell docker://git-docker-classes.mst.edu/containers/container`

After that, your entire home directory should be accessible from the container.

## Exposing ports
To expose a port, for example 80,
where `<shell>` is your choice of shell (nu/fish/zsh/bash/etc.):

`sudo docker run --interactive --tty --rm -p 80:80 --mount type=bind,source="$(pwd)"/,target=/your_code container <shell>`

Or, more verbosely, when exposing port 6789

`sudo docker run --interactive --tty --publish target=6789,published=127.0.0.1:6789,protocol=tcp --mount type=bind,source="$(pwd)"/,target=/your_code container <shell>`

Or, the pre-built version

`sudo docker run --interactive --tty --publish target=6789,published=127.0.0.1:6789,protocol=tcp --mount type=bind,source="$(pwd)"/,target=/your_code git-docker-classes.mst.edu/containers/container <shell>`

This allows you to access network programs or services running within the container,
from your host.
For example, you could connect a web browser in the host,
to a web server in the container.

## Maintenance
If you maintain or update this container:

### Adding this submodule to your repo
If you, as an assignment developer or repository owner,
want to add this submodule to your repo, then:

`git submodule add https://git-classes.mst.edu/containers/container/`

### Adding software
Where <login> is your username,
and you have created a token in the gitlab web interface,
which will be required to copy-past via std-in:

```sh
sudo docker login git-docker-classes.mst.edu -u <login> --password-stdin
sudo docker build -t git-docker-classes.mst.edu/containers/container .
sudo docker push git-docker-classes.mst.edu/containers/container
```
