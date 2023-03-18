# pg_stage

A utility for generating a database dump, the data in which will be obfuscated. This dump can be used in development and 
stage servers without fear of their theft.

## Content

- [How does it work?](#how-does-it-work)
- [Usage example](#usage-example)
- [Supported types of obfuscation](#supported-types-of-obfuscation)
- [Why did I write my utility?](#why-did-i-write-my-utility)
- [Thanks for the inspiration](#thanks-for-the-inspiration)

## How does it work?

The utility processes the output of the pg_dump command line by line and decides whether to obfuscate data at the level 
of comments to a table or column.

## Usage example

1. You need to create a file with approximately the following contents:

```python
# main.py
from pg_stage.obfuscator import Obfuscator


obfuscator = Obfuscator(locale='ru_RU')
obfuscator.run()
```

2. Add comments to a column or table:

```sql
COMMENT ON COLUMN table_1.first_name IS 'anon: [{"mutation_name": "first_name"}]';
```

3. Run pg_dump and redirect the stream to the running script process:

```bash
pg_dump -d database | python3 main.py > dump.sql
```

4. After that you will get the obfuscated data in the table

## Supported types of obfuscation

You can see the current list [here](https://github.com/froOzzy/pg_stage/blob/main/src/pg_stage/mutator.py).

## Why did I write my utility?

I also adhere to the rule that you do not need to place third-party plugins in the working database for its security 
(most utilities are in the form of database extensions).

Also, in similar utilities, I could not find the functionality for uniform obfuscation of data in related tables. 
This prompted me to write my own utility that will be able to obfuscate data in related tables with the same result 
by a foreign key.

Example:

```sql
COMMENT ON COLUMN table_1.first_name IS 'anon: [{"mutation_name": "first_name", "relations": [{"table_name": "table_1", "column_name": "last_name", "from_column_name": "id", "to_column_name": "id"}]}]';
```

where `relations` - links on tables where it is necessary to obfuscate fields according to the current field.

## Thanks for the inspiration

- [triki](https://github.com/josacar/triki)
- [fake_pipe](https://github.com/ddrscott/fake_pipe)
