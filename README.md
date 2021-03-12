# Lift Pass

This application solves the problem of calculating the pricing for ski lift passes.

## Pricing

- Day passes:
  - Passes are free for people younger than 6.
  - Mondays have a 35% discount if it’s not a holiday.
  - People younger than 15 only pay 70% of the tariff but Monday discount does not apply.
  - People older than 64 only pay 75% of the tariff.
- Night passes:
  - Passes are free for people younger than 6.
  - People older than 64 only pay a 40% of the tariff.

## Challenge

The code is difficult to unit test or extend due to bad design. The business logic is tied to the framework
and SQL.

## Resolution

All code will be refactored and created with proper Architectural patters to make it easy to maintain, upgrade and
extend any functionality.

[Swagger Documentation](http://lift-pass-prod-647842666.us-east-1.elb.amazonaws.com/.swagger)

### Changes

#### Database

The mos important change about dependencies is the removal of the active record pattern (SQLAlchemy).
Active Record patterns are great for fast development, but it comes with several cons that should be avoided on high
scalable applications. Some of this cons are:

- You need to lear about the method language definition of the ORM or Active Record tool to be able to interact with the
  database itself instead of use Regular SQL sentences.
- It's pretty hard to debug errors on the calls because all happens in background.
- Expensive data loading from relation methods (one to one, one to many, etc)
- You don't have full control about the SQL queries that are being executed on the DB because all of it are built it
  are build it on execution time.
  
To avoid this problems SQLAlchemy was removed from the project and replaced with the Repository and Model Serialization 
patterns in combination with a Native SQL Connection class as context to have full control of the DB executions and
maintain a clear structure that could be easy to maintain. 

**Resources:**

- src
  - commons
    - drivers
      - sqlite
  - models
  - repositories

#### Routing

Instead of keep all routes in the same file, this was replaced by a modular structure supported by action handlers and
the `Flask Bluprints` to have an easy way to add or remove HTTP paths and maintain a domain oriented abstraction of the
routers.

**Resources:**

- src
  - routes
  - server.py
- app.py

#### Application logic

In order to maintain a clear separation of business logic and resource operations the Hexagonal Architecture principles
were implemented on the project getting the `adapters` a new resource that encapsulate any action that is not part of
the business logic (like Database call or external rest request) and left actions that be included as part of the main
logic in the handlers.

This Hexagonal Architecture principles bring an easy way to update any component like the database without having to
modify the business logic it self, so the business logic keeps agnostic to the technologies.

**Resources:**

- src
  - adapters
  - handlers
  - libs

#### Security and Configuration

To keep the application secure a Bearer authentication pattern has been implemented to have a minimum security for 
external requests. All Authentication process happens by a Middleware pattern. This middlewares are enabled on any route
were an authentication process is required and the `API_KEY` is configured on the `src/config/config.yml` file of the
project.

About configuration, the `Twelve Factor` pattern has been implemented for this, keeping an application based on 
configuration across all the stages (dev, staging, prod). 

Local configurations are stored in the project as a YML file and the configs for deployed stages are stored on AWS 
Secrets Manager service bringing the ability to modify configurations without the need of restart the application to
take effect.

**Resources:**

- src
  - config
  - middlewares
  - routes 

## Running

### Server

```shell script
make run
```

### Tests

```shell script
make test
```

## Other available commands

Project `Makefile` have several commands to help improve the code quality to see all of it execute the help command:

```shell script
make help
```
