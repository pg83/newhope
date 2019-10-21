ls | grep 'py' | grep -v '\.pyc' | grep -v '~' | sort | sed -e 's/\.py// '|  while read l; do echo "        \"$l\","; done | grep -v '__'
