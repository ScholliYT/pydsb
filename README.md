# pydsb

Unofficial DSBmobile API written in Python. Because the official API of DSBmobile is very complicated and hard to use, I wrote an API wrapper for Python.

## Installation

```sh
$ pip3 install pydsb
```

## Usage

```python
>>> import pydsb
>>> vertretungsplan = pydsb.PyDSB("username", "password")
```

## Methods

### Summary

- vertretungsplan.get_entries()
- vertretungsplan.query_date(day, month, year)
- vertretungsplan.query_class(class_)

### get_entries()

Returns a list containing dictionaries with information about the concerned lesson.

```python
>>> vertretungsplan = pydsb.PyDSB("username", "password")
>>> vertretungsplan.get_entries()
[
    {
        'class': '9aR',
        'date': '9.10.2017',
        'day': 'Montag',
        'period': '1',
        'room': '314',
        'subject': 'E',
        'text': '',
        'type': 'Enfall'
    },
    {
        'class': '10cG',
        'date': '9.10.2017',
        'day': 'Montag',
        'period': '9 - 10',
        'room': '128',
        'subject': 'PHY',
        'text': '\xa0',
        'type': 'Vertretung'
    },
    {
        'class': '5aG',
        'date': '10.10.2017',
        'day': 'Dienstag',
        'period': '5',
        'room': '---',
        'subject': 'F',
        'text': 'Aufgaben',
        'type': 'Vtr. ohne Lehrer'
    },
    {
        'class': '9cG',
        'date': '10.10.2017',
        'day': 'Dienstag',
        'period': '8',
        'room': '---',
        'subject': 'M',
        'text': '',
        'type': 'Entfall'
    },
    {
        'class': '10cG',
        'date': '11.10.2017',
        'day': 'Mittwoch',
        'period': '3',
        'room': '112',
        'subject': 'NT',
        'text': '\xa0',
        'type': 'Vertretung'
    }
]
```

### query_date(day, month, year)

Filters entries for a date. Without any parameters it returns a list containing dictionaries of the current day.

```python
>>> vertretungsplan = pydsb.PyDSB("username", "password")
>>> vertretungsplan.query_date(9, 10, 2017)
[
    {
        'class': '9aR',
        'date': '9.10.2017',
        'day': 'Montag',
        'period': '1',
        'room': '314',
        'subject': 'E',
        'text': '',
        'type': 'Enfall'
    },
    {
        'class': '10cG',
        'date': '9.10.2017',
        'day': 'Montag',
        'period': '9 - 10',
        'room': '128',
        'subject': 'PHY',
        'text': '\xa0',
        'type': 'Vertretung'
    }
]
```

### query_class(class_)

Filters entries for one specific class.

```python
>>> vertretungsplan = pydsb.PyDSB("username", "password")
>>> vertretungsplan.query_class("10cG")
[
    {
        'class': '10cG',
        'date': '9.10.2017',
        'day': 'Montag',
        'period': '9 - 10',
        'room': '128',
        'subject': 'PHY',
        'text': '\xa0',
        'type': 'Vertretung'
    },
    {
        'class': '10cG',
        'date': '11.10.2017',
        'day': 'Mittwoch',
        'period': '3',
        'room': '112',
        'subject': 'NT',
        'text': '\xa0',
        'type': 'Vertretung'
    }
]
```