Python version of MMT software

*This software is experimental.*

## Requirements

- Python 3.12 (tested with 3.12, likely runs with older versions)
- Node.js
- ffmpeg

## Installation

Install Pytorch [according to your system,](https://pytorch.org/get-started/locally/) e.g. for Linux with only CPU support:

```shell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

Install the rest of the dependencies:

```shell
pip install git+https://github.com/m-bain/whisperx.git
pip install -r requirements.txt
npm install
```

Prepare the database and create the admin user:

```shell
python manage.py migrate
python manage.py createsuperuser
```

## Usage

Run these three servers in separate terminals: Django webserver, the task queue
cluster and the webpack dev server.

```shell
python manage.py runserver
python manage.py qcluster
npm run devserver
```

Visit 127.0.0.1:8000/ in your browser. The admin interface is located
at 127.0.0.1:8000/admin/
