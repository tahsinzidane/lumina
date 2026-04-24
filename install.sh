#!/bin/bash

# Configuration
INSTALL_DIR="$HOME/.local/share/lumina"
BIN_DIR="$HOME/.local/bin"
AUTO_START=false

# Flag detection
for arg in "$@"; do
    if [ "$arg" == "--auto-start" ]; then
        AUTO_START=true
    fi
done

echo "Installing Lumina..."

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Copy project files
cp -r . "$INSTALL_DIR"

# Install python dependencies
pip install prompt_toolkit --user --break-system-packages 2>/dev/null || pip install prompt_toolkit --user

# Create the executable wrapper
cat <<EOF > "$BIN_DIR/lumina"
#!/bin/bash
python3 "$INSTALL_DIR/main.py" "\$@"
EOF

# Set permissions
chmod +x "$BIN_DIR/lumina"
chmod +x "$INSTALL_DIR/main.py"

# Auto-start logic
if [ "$AUTO_START" = true ]; then
    echo "Configuring auto-start for Lumina..."
    
    # Function to add to shell config
    setup_auto_start() {
        local config_file=$1
        if [ -f "$config_file" ]; then
            # Check if already added to avoid duplicates
            if ! grep -q "lumina" "$config_file"; then
                echo -e "\n# Start Lumina Shell automatically\nif [[ \$- == *i* ]]; then\n  exec lumina\nfi" >> "$config_file"
                echo "✅ Added auto-start to $config_file"
            else
                echo "ℹ️ Lumina is already in $config_file"
            fi
        fi
    }

    setup_auto_start "$HOME/.bashrc"
    setup_auto_start "$HOME/.zshrc"
fi

echo "--------------------------------------------------"
echo "Installation complete!"
echo "Run 'lumina' to start."
if [ "$AUTO_START" = true ]; then
    echo "Terminal restart korle Lumina auto-start hobe."
fi
echo "Ensure $BIN_DIR is in your PATH."