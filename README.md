[![Status][status-badge]][status-url]


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

# gpyt-openai

## About

## Getting started
Clone the repository, run `poetry install` in the repository root directory.

## Prerequisites
Python 3.11, pip, poetry.

## Installation
Installation of gpyt-openai is handled by poetry during development.

## Usage

Serve the application with `waitress-serve gpyt_openai.injection.injector:app`.

### Environment variables
| Variable               | Description               | Default                 |
|------------------------|---------------------------|-------------------------|
| `LOG_LEVEL`            | Log level                 | `INFO`                  |
| `GPYT_COMMAND_BUS_URL` | URL to the command bus    | `http://localhost:8080` |
| `GPYT_OPENAI_URL`      | URL to the OpenAI service | `http://localhost:8082` |
| `GPYT_EVENT_BUS_URL`   | URL to the event bus      | `http://localhost:8081` |


[contributors-shield]: https://img.shields.io/github/contributors/ocellicode/gpyt-openai.svg?style=for-the-badge
[contributors-url]: https://github.com/ocellicode/gpyt-openai/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ocellicode/gpyt-openai.svg?style=for-the-badge
[forks-url]: https://github.com/ocellicode/gpyt-openai/network/members
[stars-shield]: https://img.shields.io/github/stars/ocellicode/gpyt-openai.svg?style=for-the-badge
[stars-url]: https://github.com/ocellicode/gpyt-openai/stargazers
[issues-shield]: https://img.shields.io/github/issues/ocellicode/gpyt-openai.svg?style=for-the-badge
[issues-url]: https://github.com/ocellicode/gpyt-openai/issues
[license-shield]: https://img.shields.io/github/license/ocellicode/gpyt-openai.svg?style=for-the-badge
[license-url]: https://github.com/ocellicode/gpyt-openai/blob/master/LICENSE
[status-badge]: https://github.com/ocellicode/gpyt-openai/actions/workflows/main.yml/badge.svg
[status-url]: https://github.com/ocellicode/gpyt-openai/actions/workflows/main.yml
