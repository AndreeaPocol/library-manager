import csv
from os import path
import pandas as pd
from datetime import date, datetime

# TODO:
# * improve search by adding support for partial string matches
# * automatically check for loan dates more than x days in the past to follow up with
# * add user interface

FILE_NAME = "library.csv"
TITLE_IDX = 0
AUTH_IDX = 1
YEAR_IDX = 2
AVAIL_IDX = 3
LOANER_NAME_IDX = 4
LOAN_DATE_IDX = 5


def addBook():
    title = input("Please enter the title of the book:\n")
    author = input("Please enter the author of the book:\n")
    publicationYear = input("Please enter the publication year of the book:\n")
    points = [title, author, publicationYear, "True", "", ""]
    with open(FILE_NAME, "r+") as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        for row in rows:
            if (
                (row[TITLE_IDX] == title)
                and (row[AUTH_IDX] == author)
                and (row[YEAR_IDX] == publicationYear)
            ):
                print("This book already exists in the library.")
                return
        filewriter = csv.writer(csvfile, delimiter=",")
        filewriter.writerow(points)
    print("Book added successfully!")


def deleteBook():
    title = input("Please enter the title of the book you'd like to delete:\n")
    author = input("Please enter the author of the book you'd like to delete:\n")
    publicationYear = input(
        "Please enter the publication year of the book you'd like to delete:\n"
    )
    idx = -1
    found = False
    with open(FILE_NAME, "r+") as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        for row in rows:
            if (
                (row[TITLE_IDX] == title)
                and (row[AUTH_IDX] == author)
                and (row[YEAR_IDX] == publicationYear)
            ):
                found = True
                break
            else:
                idx = idx + 1
    if found:
        data = pd.read_csv(FILE_NAME)
        data.drop(index=idx, inplace=True)
        data.to_csv(FILE_NAME, index=False)
        print("Book deleted successfully!")
    else:
        print("No such book exists in the library.")


def loanOutBook():
    title = input("Please enter the title of the book you'd like to sign out:\n")
    author = input("Please enter the author of the book you'd like to sign out:\n")
    publicationYear = input(
        "Please enter the publication year of the book you'd like to sign out:\n"
    )
    idx = -1
    with open(FILE_NAME, "r+") as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        for row in rows:
            if (
                (row[TITLE_IDX] == title)
                and (row[AUTH_IDX] == author)
                and (row[YEAR_IDX] == publicationYear)
            ):
                if row[LOANER_NAME_IDX]:
                    print("Sorry, this book is already loaned out.")
                    return
                loaner = input("Please enter the name of the loaner:\n")
                df = pd.read_csv(FILE_NAME)
                df.loc[idx, "IsAvailable"] = "False"
                df.loc[idx, "Loaner"] = loaner
                df.loc[idx, "LoanDate"] = datetime.today().strftime("%Y-%m-%d")
                df.to_csv(FILE_NAME, index=False)
                print("Book signed out successfully!")
                return
            idx = idx + 1
    print("No such book exists in the library.")


def returnBook():
    title = input("Please enter the title of the book you'd like to return:\n")
    author = input("Please enter the author of the book you'd like to return:\n")
    publicationYear = input(
        "Please enter the publication year of the book you'd like to return:\n"
    )
    idx = -1
    with open(FILE_NAME, "r+") as csvfile:
        rows = csv.reader(csvfile, delimiter=",")
        for row in rows:
            if (
                (row[TITLE_IDX] == title)
                and (row[AUTH_IDX] == author)
                and (row[YEAR_IDX] == publicationYear)
            ):
                if not row[LOANER_NAME_IDX]:
                    print("This book was not loaned out.")
                    return
                df = pd.read_csv(FILE_NAME)
                df.loc[idx, "IsAvailable"] = "True"
                df.loc[idx, "Loaner"] = ""
                df.loc[idx, "LoanDate"] = ""
                df.to_csv(FILE_NAME, index=False)
                print("Book returned successfully!")
                return
            idx = idx + 1
    print("No such book exists in the library.")


def searchForBook():
    found = False
    searchField = input(
        "Please enter 'a' if you would like to searh by author and 't' if you would like to search by title':\n"
    )
    if searchField == "t":
        title = input("Please enter the title of the book you are searching for:\n")
        with open(FILE_NAME, "r") as csvfile:
            rows = csv.reader(csvfile, delimiter=",")
            for row in rows:
                if row[TITLE_IDX] == title:
                    found = True
                    print(
                        "The following book by that title exists in the library:\n"
                        + "[\n   Author = {author}\n".format(author=row[AUTH_IDX])
                        + "   Title = {title}\n".format(title=title)
                        + "   Publication year = {year}\n".format(year=row[YEAR_IDX])
                        + "   Is available = {isAvailable}\n".format(
                            isAvailable=row[AVAIL_IDX]
                        )
                        + "   Loan date = {date}\n".format(date=row[LOAN_DATE_IDX])
                        + "   Loaner = {loaner}\n]".format(loaner=row[LOANER_NAME_IDX])
                    )
    if searchField == "a":
        author = input("Please enter the author of the book you are searching for:\n")
        with open(FILE_NAME, "r") as csvfile:
            rows = csv.reader(csvfile, delimiter=",")
            for row in rows:
                if row[AUTH_IDX] == author:
                    found = True
                    print(
                        "The following book by that author exists in the library:\n"
                        + "[\n   Author = {author}\n".format(author=author)
                        + "   Title = {title}\n".format(title=row[TITLE_IDX])
                        + "   Publication year = {year}\n".format(year=row[YEAR_IDX])
                        + "   Is available = {isAvailable}\n".format(
                            isAvailable=row[AVAIL_IDX]
                        )
                        + "   Loan date = {date}\n".format(date=row[LOAN_DATE_IDX])
                        + "   Loaner = {loaner}\n]".format(loaner=row[LOANER_NAME_IDX])
                    )
    if not found:
        print("No such book exists in the library.")


def main():
    fileExists = path.exists(FILE_NAME)
    if not fileExists:
        print("No library detected.")
        header = ["Title", "Author", "PublicationYear", "IsAvailable", "Loaner"]
        with open(FILE_NAME, "w") as csvfile:
            print("Creating library...")
            filewriter = csv.writer(csvfile, delimiter=",")
            filewriter.writerow(header)
    print("Welcome to the library!")
    while True:
        cmd = input(
            "What would you like to do? \n"
            + "Press 'a' to add a book, "
            + "'d' to delete a book, "
            + "'l' to loan out a book, "
            + "'r' to return a book, "
            + "'s' to search for a book, "
            + "and 'q' to quit.\n"
        )
        if cmd == "a":
            addBook()
        elif cmd == "d":
            deleteBook()
        elif cmd == "l":
            loanOutBook()
        elif cmd == "r":
            returnBook()
        elif cmd == "s":
            searchForBook()
        elif cmd == "q":
            return


if __name__ == "__main__":
    main()
