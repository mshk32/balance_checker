# Networks plan:
+ETH mainnet
+Linea
+Optimism
+Arbitrum
+zkSync Era
+Scroll
+Base
+Mode
+Blast
-Arbitrum Nova
-Polygon
-Polygon zkEVM
-Binance Smart Chain
-opBNB
-Fantom

# problems:
! code breaks if not all networks are chosen

# bright ideas:
<+> Need to make a config file where a user can choose which networks to scan
Started making a config system. Need to make a network enables system. Done it.
Now need to add more stuff to a config file, e.g. rpc links.
Also need to think where to keep some constants, like contracts.

< > Need to get to know more about git version control
Maybe move some files, like wallets.txt and work_time_logs to some other place.

<+> check if a network is not connected (in the beginning)


# vision
A closed website with a table of workers' addresses and their balances among networks.
-A user can choose what information to see and what information to hide (balances of exact networks or exact tokens in exact networks)
-It has 'last update' time to be sure that data is up-to-date
-A user can update all data or only few networks data if there is no need to update everything (it obviously will take more time to process)
-Admins can change wallets on the list.
-A user can acces data on the website, or download a csv/excel file, or make a google tables document