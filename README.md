# Telus - Technical Challenge

## Table of Contents

- [Architecture](#architecture)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Architecture

![alt text](image.png)

## Technologies

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js

## Installation

- Clone the repo

- Set .env file in the root. Set this variables:
    - SFTP_USER= {SFTP user, it will configure this user in the server}
    - SFTP_PASSWORD= {SFTP passwords , it will configure this password in the server}
    - SFTP_PORT= {it has to match with the SFTP port, in this case 22}

- Located at the root of the project, run:

    `docker compose up`

- In the docker desktop, you will see all of this containers up and running

![image](https://github.com/lucasmfunes/ti-challenge/assets/17455330/c460d89c-a6ca-4d19-a886-465b8784ff01)

## Usage

This process is intended to run every day at 00:00hs. For testing purposes, you can modify the file 'scheduler.py' inside the path extraction-app/core/ with the following line: 

`schedule.every(5).minutes.do(fetch_and_save_data)`

To connect to the db, you can access the data.db file located in the "Files" tab in the loader-app and api-1 (shared volume) containers.

![alt text](image-1.png)

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.
