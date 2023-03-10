for file in ~/.{path,exports,aliases,functions,extra,platform}; do
	[ -r "$file" ] && [ -f "$file" ] && source "$file";
done;