# Simple Relational Database
#### [Challenge description](https://www.thumbtack.com/challenges/simple-database)

## Usage
### Interactive mode
  * `python database.py`

### Fileread mode
  * `python database.py test1.txt`

### Or send text from file into standard input
  * `python database.py < test1.txt`
  * `cat test1.txt | python database.py`

### Valid commands
  * `SET a b` : stores variable a with value b
  * `GET a` : gets value of variable a
  * `UNSET a` : removes variable a
  * `NUMEQUALTO b` : retreives count of variables with value b
  * `BEGIN` : begins a transaction
  * `ROLLBACK` : resets changes since the start of the last transactions
  * `COMMIT` : saves all open transactions to
