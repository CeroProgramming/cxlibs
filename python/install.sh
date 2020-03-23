#!/bin/bash

if [[ $EUID != 0 ]]; then
	echo "Please run as root.."
	exit 1
fi

mkdir -p '/usr/local/lib/cxlibs/'

echo "Installing all libs to /usr/local/lib/cxlibs/"
cp -rv * '/usr/local/lib/cxlibs/'

if ! grep -q 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' '/root/.bashrc'; then
	echo 'Installing PYTHONPATH for root..'
	echo 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' >> '/root/.bashrc'
fi

if ! grep -q 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' '/etc/skel/.bashrc'; then
	echo 'Installing PYTHONPATH into default user files..'
	echo 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' >> '/etc/skel/.bashrc'
fi

IFS=$'\n'
for user in $(getent passwd | cut -d: -f1-6) ; do
	if [ "$(echo $user | cut -d: -f3)" -ge 1000 ] ; then
		file=$(echo $user | cut -d: -f6)
		if [[ "$file" != "/" ]] ; then
			if [ -f "$file/.bashrc" ] ; then
				if ! grep -q 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' "$file/.bashrc"; then
					echo "Installing PYTHONPATH for $(echo $user | cut -d: -f1).."
					echo 'export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/cxlibs"' >> "$file/.bashrc"
				fi
			fi
		fi
	fi
done

exit 0
