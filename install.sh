# Switches to the src directory and builds the Docker image.
echo "Building the Docker image..."
cd src/container  # Switch to the src directory.
docker build -t bm-linux_game .  # Build the Docker image.

