#!/bin/bash

# Configuration
INSTALL_DIR="$HOME/.local/share/lumina"
BIN_DIR="$HOME/.local/bin"

echo "Installing Lumina..."

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Copy project files
cp -r . "$INSTALL_DIR"

# Install python dependencies
pip install prompt_toolkit --user

# Create the executable wrapper
cat <<EOF > "$BIN_DIR/lumina"
#!/bin/bash
python3 "$INSTALL_DIR/main.py" "\$@"
EOF

# Set permissions
chmod +x "$BIN_DIR/lumina"
chmod +x "$INSTALL_DIR/main.py"

echo "Installation complete!"
echo "Run 'lumina' to start. (Ensure $BIN_DIR is in your PATH)"