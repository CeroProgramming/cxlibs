#!/bin/bash

if [[ $EUID != 0 ]]; then
	echo "Please run as root.."
	exit 1
fi

echo "Uninstalling libs from /usr/local/lib/cxlibs/"
rm -rv '/usr/local/lib/cxlibs/'

if grep -q 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' '/root/.bashrc'; then
	echo 'Uninstalling PYTHONPATH for root..'
	grep -v 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' '/root/.bashrc' > '/root/.bashrc.0'
	mv '/root/.bashrc.0' '/root/.bashrc'
fi

if grep -q 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' '/etc/skel/.bashrc'; then
	echo 'Uninstalling PYTHONPATH out of default user files..'
	grep -v 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' '/etc/skel/.bashrc' > '/etc/skel/.bashrc.0'
	mv '/etc/skel/.bashrc.0' '/etc/skel/.bashrc'
fi

IFS=$'\n'
for user in $(getent passwd | cut -d: -f1-6) ; do
	if [ "$(echo $user | cut -d: -f3)" -ge 1000 ] ; then
	file=$(echo $user | cut -d: -f6)
		if [[ "$file" != "/" ]] ; then
			if [ -f "$file" ] ; then
				if grep -q 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' "$file/.bashrc"; then
					echo "Uninstalling PYTHONPATH for $(echo $user | cut -d: -f1).."
					grep -v 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' "$file/.bashrc" > "$file/.bashrc0"
					mv $file.0 $file
				fi
			fi
		fi
	fi
done

exit 0
