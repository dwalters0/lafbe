FROM docker.io/library/python:3.12-slim

# Avoid interactive package prompts and unbuffer Python logs.
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        openssh-server \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /run/sshd

RUN printf '%s\n' \
    'PermitRootLogin no' \
    'PasswordAuthentication no' \
    'PubkeyAuthentication yes' \
    'UsePAM no' \
    'X11Forwarding no' \
    'AllowTcpForwarding no' \
    '' \
    >> /etc/ssh/sshd_config

#Optional force command for above
#    'Match User dan' \
#    '    ForceCommand /usr/local/bin/python3 /opt/app/tutor_frog.py' \
#    '    PermitTTY yes' \



# Copy initial config to mount points and start SSH.

RUN useradd --create-home --shell /bin/bash dan
RUN echo 'dan:dan' | chpasswd

USER dan

RUN curl --fail --show-error --silent --location \
        https://chatgpt.com/codex/install.sh \
        --output /tmp/install.sh \
    && chmod +x /tmp/install.sh \
    && /tmp/install.sh \
    && rm /tmp/install.sh

RUN mkdir ~/.ssh
RUN echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEfUatTsSQ3F0aXyLTT5t97gqkT2Hr38F69EQgU7si+A' >> ~/.ssh/authorized_keys

RUN mkdir -p /home/dan/app
WORKDIR /home/dan/app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 22

USER root
CMD ["/usr/sbin/sshd", "-D"]