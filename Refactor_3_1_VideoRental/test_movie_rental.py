import pytest
from customer import Customer
from rental import Rental
from movie import Movie


def test_return_new_customer():
    customer = Customer('NAME_NOT_IMPORTANT')
    assert customer.get_name() == 'NAME_NOT_IMPORTANT'


def test_statement_for_no_rental():
    customer = Customer('NAME_NOT_IMPORTANT')
    statement = customer.statement()
    assert statement == (
        'Rental Record for NAME_NOT_IMPORTANT\n'
        'Amount owed is 0\n'
        'You earned 0 frequent renter points'
    )


def test_statement_for_regular_movie_rental_for_less_than_3_days():
    customer = Customer('NAME_NOT_IMPORTANT')
    movie = Movie('TITLE_NOT_IMPORTANT', Movie.REGULAR)
    days_rented = 2
    rental = Rental(movie, days_rented)
    customer.add_rental(rental)

    statement = customer.statement()

    assert statement == (
        'Rental Record for NAME_NOT_IMPORTANT\n'
        '\tTITLE_NOT_IMPORTANT\t2.0\n'
        'Amount owed is 2.0\n'
        'You earned 1 frequent renter points'
    )


def test_statement_for_new_release_movie():
    customer = Customer('NAME_NOT_IMPORTANT')
    movie = Movie('TITLE_NOT_IMPORTANT', Movie.NEW_RELEASE)
    days_rented = 1
    rental = Rental(movie, days_rented)
    customer.add_rental(rental)

    statement = customer.statement()

    assert statement == (
        'Rental Record for NAME_NOT_IMPORTANT\n'
        '\tTITLE_NOT_IMPORTANT\t3.0\n'
        'Amount owed is 3.0\n'
        'You earned 1 frequent renter points'
    )


def test_statement_for_children_movie_rental_more_than_2_days():
    customer = Customer('NAME_NOT_IMPORTANT')
    movie = Movie('TITLE_NOT_IMPORTANT', Movie.CHILDREN)
    days_rented = 3
    rental = Rental(movie, days_rented)
    customer.add_rental(rental)

    statement = customer.statement()

    assert statement == (
        'Rental Record for NAME_NOT_IMPORTANT\n'
        '\tTITLE_NOT_IMPORTANT\t1.5\n'
        'Amount owed is 1.5\n'
        'You earned 1 frequent renter points'
    )


def test_statement_for_children_movie_rental_more_than_3_days():
    customer = Customer('NAME_NOT_IMPORTANT')
    movie = Movie('TITLE_NOT_IMPORTANT', Movie.CHILDREN)
    days_rented = 4
    rental = Rental(movie, days_rented)
    customer.add_rental(rental)

    statement = customer.statement()

    assert statement == (
        'Rental Record for NAME_NOT_IMPORTANT\n'
        '\tTITLE_NOT_IMPORTANT\t3.0\n'
        'Amount owed is 3.0\n'
        'You earned 1 frequent renter points'
    )


def test_statement_for_new_release_movie_rental_more_than_1_day():
    customer = Customer('NAME_NOT_IMPORTANT')
    movie = Movie('TITLE_NOT_IMPORTANT', Movie.NEW_RELEASE)
    days_rented = 2
    rental = Rental(movie, days_rented)
    customer.add_rental(rental)

    statement = customer.statement()

    assert statement == (
        'Rental Record for NAME_NOT_IMPORTANT\n'
        '\tTITLE_NOT_IMPORTANT\t6.0\n'
        'Amount owed is 6.0\n'
        'You earned 2 frequent renter points'
    )


def test_statement_for_few_movie_rentals():
    # arrange
    customer = Customer('NAME_NOT_IMPORTANT')
    regular_movie = Movie('TITLE_NOT_IMPORTANT', Movie.REGULAR)
    new_release_movie = Movie('TITLE_NOT_IMPORTANT', Movie.NEW_RELEASE)
    children_movie = Movie('TITLE_NOT_IMPORTANT', Movie.CHILDREN)
    customer.add_rental(Rental(regular_movie, 1))
    customer.add_rental(Rental(new_release_movie, 4))
    customer.add_rental(Rental(children_movie, 4))

    # act
    statement = customer.statement()

    # assert
    assert statement == (
        'Rental Record for NAME_NOT_IMPORTANT\n'
        '\tTITLE_NOT_IMPORTANT\t2.0\n'
        '\tTITLE_NOT_IMPORTANT\t12.0\n'
        '\tTITLE_NOT_IMPORTANT\t3.0\n'
        'Amount owed is 17.0\n'
        'You earned 4 frequent renter points'
    )
