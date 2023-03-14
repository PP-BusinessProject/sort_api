# SORT API

The backend powered by [SQLAlchemy][] and [FastAPI][].

## Getting Started

To get started, clone this repository and install `requirements.txt`.

Then, run the project from `lib/main.py`.

## Database Structure

The database is written with [SQLAlchemy][] ORM and is fully operational.

The full database structure can be seen in `lib/schema.png`.

## API

The requests are handled by [FastAPI][] in a single endpoint located in `lib/methods/endpoint.py`.

All requests are handled in the same way in a typical SQL fashion. Inspired by [PostgREST][].

## Reference

* [SQLAlchemy][], SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
* [FastAPI][], a modern, fast (high-performance), web framework for building APIs. 
* [PostgREST][], a standalone web server that turns your PostgreSQL database directly into a RESTful API.

[SQLAlchemy]: https://docs.sqlalchemy.org/en/20/
[FastAPI]: https://fastapi.tiangolo.com/
[PostgREST]: https://postgrest.org/en/stable/
