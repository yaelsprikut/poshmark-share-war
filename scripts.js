// get all elems with account names from a category page
const accounts = document.getElementsByClassName("tc--g m--l--1 ellipses")
// accounts from share page
const accounts = document.getElementsByClassName("wb--ww tc--g")
// get array from accounts
Array.from(accounts)
// init empty arr
const usersArr = []
// loop accounts and add to usersArr
for (let index = 0; index < accounts.length; index++) {usersArr.push(accounts[index].innerText)}
// remove duplicates from array
uniq = [...new Set(usersArr)];
// copy the uniq array

// Command to run: 
// python3 share_war.py -a jufall13 -b True -r 1 -n 1