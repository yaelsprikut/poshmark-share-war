usernames=(
# not comma seperated string vals
)

for i in "${usernames[@]}"
do python3 share_war.py  -a $i  -b True -r 2 -n 1
done