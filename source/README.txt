--- You can run inference models in llama by running the following command:

/workspace/source/./entrypoint.sh ./models/llama-2-7b.Q4_K_M.gguf "Hello, world!"

--- You can get unique sha number of a docker image by:

docker pull ubuntu:22.04
docker inspect --format='{{index .RepoDigests 0}}' ubuntu:22.04

--- Generate a lock file for apt packages:
apt list --installed > apt-lock.txt

Currently, I use the command below to get apt packages, check which one is better:

dpkg-query -W --showformat='${Package}=${Version}\n' > /workspace/dependency_versions/apt_snapshot_dev.txt

--- Get pip package snapshot:
pip freeze > requirements_dev.txt

--- For Git-based libs (like llama.cpp):
git rev-parse HEAD > llama_commit.txt

--- generate hashes for pip packages:
pip-compile --generate-hashes dependency_versions/requirements.in \
            -o dependency_versions/requirements_prod.txt

