# Fair Queuing and Weighted Fair Queuing implementation

## Usage

You can see the options with:
```
$ python main.py -h
```

But you'll probably want the "normal" execution which is:
```
$ python main.py [file_name.txt] [weights]
```

## File format
The file format is the following (each field is split by spaces )

| Time Arrival | Length | Stream Id |
|--------------|--------|-----------|
|       0      |  1000  |     1     |
|       0      |   20   |     2     |
|   .......    |  ....  |    ...    |

## Package Id's
The packet id (not stream id) is assigned by the line of the file, this means that the packet you define on line 3 has id 3, and go on.

For example, if you have the following file:

| Time Arrival | Length | Stream Id |
|--------------|--------|-----------|
|       0      |   100  |     1     |
|      20      |   95   |     2     |
|      30      |   50   |     2     |
|      35      |   75   |     3     |
|      40      |  100   |     1     |
|       0      |   60   |     3     |
|   .......    |  ....  |    ...    |

Be aware that the package

| Time Arrival | Length | Stream Id |
|--------------|--------|-----------|
|   .......    |  ....  |    ...    |
|       0      |   60   |     3     |
|   .......    |  ....  |    ...    |

Will have the id: 6, which can be "not intuitive", since it is received in second 0.

## Test the algorithm
I've added some tests (for fair queueing and weighted fair queueing). All the datasets live inside the "/data" folder.

If you want to run all the tests execute:

```
$ pytest .
```

