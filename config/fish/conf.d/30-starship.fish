# Enable starship prompt if present
if type -q starship
  starship init fish | source
end
