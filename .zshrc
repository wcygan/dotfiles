# Load dotfiles with status reporting
loaded_files=()
failed_files=()

for file in ~/.{path.sh,exports.sh,aliases.sh,functions.sh,extra.sh,platform.sh}; do
	if [ -r "$file" ] && [ -f "$file" ]; then
		if source "$file" 2>/dev/null; then
			loaded_files+=("$(basename "$file")")
		else
			failed_files+=("$(basename "$file")")
		fi
	fi
done

# Report results
if [ ${#loaded_files[@]} -gt 0 ]; then
	echo "✓ Loaded dotfiles: ${loaded_files[*]}"
fi

if [ ${#failed_files[@]} -gt 0 ]; then
	echo "✗ Failed to load: ${failed_files[*]}" >&2
else
	echo "🎉 All dotfiles loaded successfully!"
fi