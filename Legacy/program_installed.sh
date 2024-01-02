# Check if a program name was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <program_name>"
    exit 1
fi

# Use the which command to find the program
program_path=$(which $1 2>/dev/null)

# Check if the program is installed
if [ -z "$program_path" ]; then
    echo "please install $1"
else
    echo "$program_path"
fi
