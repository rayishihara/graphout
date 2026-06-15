FROM ubuntu:24.04

WORKDIR /app

EXPOSE 5000
EXPOSE 8888

# Install basic tools
RUN apt-get update &&\
    apt-get install -y curl fish wget gpg &&\
    rm -rf /var/lib/apt/lists/*

# Install Terraform CLI
RUN wget -O - https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg &&\
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list &&\
    apt-get update &&\
    apt-get install -y terraform &&\
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Set up dependencies
COPY pyproject.toml uv.lock ./
RUN uv python install 3.13 &&\
    uv sync --frozen

# Copy files
COPY src/ ./src/
COPY docs/ ./docs/

# Just so we can run commands without prefixing them with uv run
ENV PATH="/app/.venv/bin:$PATH"

# Start Jupyter Lab server by default when container starts
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--IdentityProvider.token=''", "--ServerApp.password=''"]