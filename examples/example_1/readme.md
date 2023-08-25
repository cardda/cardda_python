# Example 01
## Use case
Creation of payments/wire transfers from an internal data source using the Cardda platform
## Behavior
The script assumes the existance of environmental variables that define the origin bank_account and the bank_key used for creating the transactions.

First the script collects the the information of each payment to be done from an internal SQL database. Then It takes care of verifying that each recipient for the payments already exists in Cardda, and has the proper status to begin doing transactions with it. If any particular recipient doesnt exists or has a status different from the ideal case, the script will try to create or update it properly (if possible).
Once that is done, the script will try to enroll each transaction to the respective recipient. If they fail in a async manner, the script will re attempt to enroll the transaction, and if they fail in a sync manner, the transactions will be marked as invalid.

At the end the script will do a report of the transactions enrolled with their given states and also the failed ones.

The script does everything in sequence, and waits for the Cardda platform to update the statues of the elements in an iterative manner (create, wait, check, repeat). If you need to boost performance, you could try and paralelize this tasks, as long as you are careful to only perform tasks that cardda allows to do unordered.