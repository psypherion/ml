#!/bin/bash

# Directory where the run.sh script is located
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get the path of the autoGIT.py file
python_path="$(find "$script_dir" -name 'autoGIT.py' -type f)"

# Check if autoGIT.py exists
if [ -z "$python_path" ]; then
  echo "Error: autoGIT.py file not found in the current directory or its subdirectories."
  exit 1
fi

# Create the bin directory if it doesn't exist
mkdir -p ~/bin

# Create the autoGIT script inside bin directory
cat > ~/bin/autoGIT <<EOF
#!/bin/bash

# Run autoGIT.py using Python
python3 "$python_path" "\$@"
EOF

# Make autoGIT executable
chmod +x ~/bin/autoGIT

# Add alias to ~/.bashrc for running autoGIT as autoGIT
echo "alias autoGIT='~/bin/autoGIT'" >> ~/.bashrc
source ~/.bashrc

echo "autoGIT script created successfully in the ~/bin directory."
echo "Alias 'autoGIT' added to your shell configuration. You can now run 'autoGIT' from anywhere."
