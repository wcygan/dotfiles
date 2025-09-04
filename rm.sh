for i in $(seq 1 32); do
  sudo dscl . -delete /Users/_nixbld$i 2>/dev/null
done

sudo dscl . -delete /Groups/nixbld 2>/dev/null